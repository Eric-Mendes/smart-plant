FROM python:3.10-slim
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "src.app.run:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
