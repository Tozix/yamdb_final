FROM python:3.7-slim
LABEL author='Tozix' version=0.0.2Beta
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]

