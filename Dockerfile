FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 拷贝 requirements.txt 并使用国内源安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 拷贝所有代码
COPY . .

# 设置环境变量，优化 Python 运行
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 暴露 Flask 服务端口
EXPOSE 8080

# 启动应用
CMD ["python", "app.py"]
