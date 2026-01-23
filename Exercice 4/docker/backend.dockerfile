FROM python:3.11
WORKDIR /app

COPY backend/src/etc /app
COPY backend/src/etc/requirements.txt /app/requirements.txt   

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
