FROM python:3.12
RUN pip install poetry
LABEL MAINTAINER="abc@gmail.com"
WORKDIR /code
COPY . /code/
RUN poetry install
EXPOSE 8000
#CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
CMD ["python", "main.py"]

#docker build -t devcount1 .
#docker run -d -p 8000:8000 devcount1
