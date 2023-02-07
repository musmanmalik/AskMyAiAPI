FROM python:3.7
WORKDIR /discussai_docker
COPY ../DiscussAI/requirements.txt /discussai_docker
RUN pip install -r requirements.txt
COPY . /discussai_docker