from flask import Flask, request, render_template, redirect, url_for
import asyncio
from core.extractor import extract_information
from ui.links_config import STEPS, REMARK
from ui.sponsor_config import SPONSOR_CONTENT

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', steps=STEPS, remark=REMARK)

@app.route('/analyze', methods=['POST'])
async def analyze():
    name_address = request.form.get('name_address')
    birth_date = request.form.get('birth_date')
    ssn = request.form.get('ssn')
    
    if not name_address:
        return render_template('index.html', steps=STEPS, remark=REMARK, error="请填写姓名地址邮码")
    
    info = await extract_information(name_address, birth_date, ssn)
    return render_template('result.html', info=info, steps=STEPS, remark=REMARK)

@app.route('/sponsor')
def sponsor():
    return render_template('sponsor.html', sponsor_content=SPONSOR_CONTENT)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)