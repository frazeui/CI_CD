FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

CMD ["python", "-c", "from app.calculator import add; print(add(2, 3))"]