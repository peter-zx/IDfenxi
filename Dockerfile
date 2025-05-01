使用官方 Python 镜像作为基础镜像

FROM python:3.10-slim

设置工作目录

WORKDIR /app

复制项目文件到容器

COPY . /app

安装系统依赖（Tkinter 需要）

RUN apt-get update && apt-get install -y 
libx11-6 
libxext6 
libxrender1 
libxtst6 
libxi6 
&& rm -rf /var/lib/apt/lists/*

安装 Python 依赖

RUN pip install --no-cache-dir -r requirements.txt

暴露端口（如果需要通过网络访问 GUI，可选）

EXPOSE 8080

运行 Flask 应用

CMD ["python", "app.py"]