FROM python:3.11.10-slim

# 设置工作目录
WORKDIR /app

RUN echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    apt-get clean && apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 复制当前目录下的所有文件到容器中的 /app 目录

COPY ./api /app/api
COPY ./requirements.txt /app/requirements.txt
COPY ./service /app/service
COPY ./main.py /app/main.py

# 安装所需的 Python 包
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r /app/requirements.txt gunicorn

# 暴露应用运行的端口
EXPOSE 5006

# 设置环境变量
ENV FLASK_ENV=production
ENV FLASK_APP=main:app

# 启动 Flask 应用
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5006"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5006", "main:app"]