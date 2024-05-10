FROM python:3.12
RUN pip install poetry
LABEL MAINTAINER="abc@gmail.com"
WORKDIR /code
COPY . /code/
RUN poetry install
EXPOSE 8000
# CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
CMD ["python", "main.py"]

# docker build -t devcount1 .
# docker run -d -p 8000:8000 devcount1
# docker logs [containerID] -f
# docker exec -it [containerID] /bin/bash
# ctrl+p+q / exit {to exit from container terminal}
# docker commit [containerID] [imagename] {to commit changes in image}
# docker images / docker image ls {list of all images}
# docker ps {show running containers}
# docker ps -a {show list of all containers}
# docker stop [containerID] {stop container}
# docker kill [containerID] {stop container}
# docker remove [containerID]
# docker remove [containerID] -f {forcefully remove container}
# docker rmi [imageID] {remove image}

# International certification Kubernties CNCF $395|Online
# International certification Python
