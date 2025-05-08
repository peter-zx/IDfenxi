from flask import Flask, render_template, request, jsonify
import asyncio
import os
import glob
import csv
from datetime import datetime
from core.extractor import extract_information
from ui.links_config import STEPS, REMARK, ANNOUNCEMENT

app = Flask(__name__)

RECORDS_DIR = "records"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
async def analyze():
    data = request.get_json()
    name_address = data.get('name_address', '')
    birth_date = data.get('birth_date', '')
    ssn = data.get('ssn', '')

    if not name_address:
        return jsonify({'error': '请在“姓名地址邮码”框内输入内容。'}), 400

    try:
        results = await extract_information(name_address, birth_date, ssn)
        save_records(results)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': f'解析失败：{str(e)}'}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR)

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
        os.makedirs(RECORDS_DIR)

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

        # 检查重复
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
            print(f"保存记录 {name} 失败：{str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1575)