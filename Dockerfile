FROM python:3.11-alpine3.19


WORKDIR /app
COPY requirements.txt /app/
RUN pip install --require-hashes --no-deps -r requirements.txt --upgrade pip 
COPY . /app/

WORKDIR ./src

CMD ["sh" , "-c", "alembic upgrade head && python -m uvicorn main:app --host=0.0.0.0 --port=8000"]
