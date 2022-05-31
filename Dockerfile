FROM python:3.8-slim-buster

WORKDIR /app

COPY ./*.txt ./*.py ./*.sh ./*.onnx /app/

RUN cd /app \
    && python3 -m pip install --upgrade pip -i https://pypi.douban.com/simple/\
    && pip3 install --no-cache-dir -r requirements.txt --extra-index-url https://pypi.douban.com/simple/ \
    && rm -rf /tmp/* && rm -rf /root/.cache/* \
    && sed -i 's#http://deb.debian.org#http://mirrors.aliyun.com/#g' /etc/apt/sources.list\
    && apt-get --allow-releaseinfo-change update && apt install libgl1-mesa-glx libglib2.0-0 -y

EXPOSE 8124

CMD ["python3", "main.py", "--port", "8124"]
