# 使用 Python部署Flask後端框架
FROM python:3.8
# 設定工作目錄
WORKDIR /usr/src/app
# 複製所需檔案到容器內
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# 暴露端口
EXPOSE 5000
# 啟動Flask
CMD ["python", "LinebotWithDify.py"]