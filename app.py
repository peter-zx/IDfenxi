from flask import Flask, render_template, request, jsonify
import os
import glob
import csv
from datetime import datetime
from core.extractor import extract_information
from ui.links_config import STEPS, REMARK, ANNOUNCEMENT

app = Flask(__name__)

RECORDS_DIR = "records"

@app.route('/')
@app.route('/idfenxi')
def index():
    return render_template('index.html')

@app.route('/idfenxi/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    name_address = data.get('name_address', '').strip()
    birth_date = data.get('birth_date', '').strip()
    ssn = data.get('ssn', '').strip()

    if not name_address:
        return jsonify({'error': '请在“姓名地址邮码”框内输入内容。'}), 400

    print(f"Raw JSON input: {data}")
    print(f"Input data - name_address: {name_address}, birth_date: {birth_date}, ssn: {ssn}")
    try:
        results = extract_information(name_address, birth_date, ssn)
        print(f"Extracted results: {results}")
        if not results or not isinstance(results, list):
            return jsonify({'error': '解析结果为空或格式错误。'}), 500
        save_records(results)
        print(f"Records saved successfully: {results}")
        return jsonify(results)
    except Exception as e:
        print(f"Analyze error: {str(e)}")
        return jsonify({'error': f'解析失败：{str(e)}'}), 500

@app.route('/idfenxi/api/history', methods=['GET'])
def get_history():
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR, 0o755)

    csv_files = glob.glob(os.path.join(RECORDS_DIR, "*.csv"))
    csv_files.sort(key=os.path.getmtime, reverse=True)
    csv_files = csv_files[:6]

    history = []
    for file_path in csv_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                record = next(reader)
                timestamp = os.path.basename(file_path).split('_')[-1].replace('.csv', '')
                name = f"{record.get('名字', '')} {record.get('姓氏', '')}".strip()
                history.append({
                    'record': record,
                    'timestamp': timestamp,
                    'name': name or 'Unknown',
                })
        except Exception:
            continue

    return jsonify(history)

def save_records(results):
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR, 0o755)

    existing_records = []
    for file_path in glob.glob(os.path.join(RECORDS_DIR, "*.csv")):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                existing_records.append(next(reader))
        except Exception:
            continue

    for info in results:
        first_name = info.get('名字', '').replace(' ', '')
        last_name = info.get('姓氏', '').replace(' ', '')
        name = (first_name + last_name) or 'Unknown'
        ssn = info.get('SSN', '')
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{name}_{timestamp}.csv"
        file_path = os.path.join(RECORDS_DIR, file_name)

        if any(
            existing.get('名字', '') == first_name and
            existing.get('姓氏', '') == last_name and
            existing.get('SSN', '') == ssn
            for existing in existing_records
        ):
            continue

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["名字", "姓氏", "州", "城市", "详细地址", "邮编", "出生日期", "英文出生日期", "年龄", "SSN"], extrasaction='ignore')
                writer.writeheader()
                writer.writerow(info)
        except Exception as e:
            print(f"Failed to save record {file_path}: {str(e)}")
            raise

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1575)