FROM python:3.10-slim
COPY ./ /app
RUN pip install -r /app/requirements.txt
WORKDIR /app/gocloud/
CMD ["python", "manage.py", "runserver", "0:8080"]