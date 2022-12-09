FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

#COPY . usr/src/app
#WORKDIR app/app

#WORKDIR /usr/src/app
COPY . /app/app/
#RUN pip install -r requirements.txt

#RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8000 --reload

#COPY ./app /code/app


#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

#ENTRYPOINT uvicorn --host 0.0.0.0 main:app --reload

