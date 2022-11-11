FROM python:3.10-slim
COPY ./ /app
RUN pip install -r /app/requirements.txt
WORKDIR /app/gocloud/
ENV SECRET_KEY '(+z7d+8_q+*o32h370iu_3)z15&5x^n=$zz^9u%th#uh)3*o_c'
CMD ["python", "manage.py", "runserver", "0:8080"]