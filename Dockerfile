FROM python:3.9.6-slim-buster
MAINTAINER Sherry Wang <sherry.wang531@gmail.com>
WORKDIR /app
#COPY requirements.txt /app/requirements.txt
#RUN pip install --requirement /app/requirements.txt
RUN ["pip", "install", "pandas==1.2.4"]
RUN ["pip", "install", "transformers==4.9.1"]
RUN ["pip", "install", "keras==2.4.3"]
RUN ["pip", "install", "jupyter"]
RUN ["pip", "install", "tensorflow==2.5.0"]
RUN ["pip", "install", "matplotlib==3.4.2"]
RUN ["pip", "install", "wandb==0.11.2"]
RUN ["pip", "install", "flask"]
COPY . /app
#CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--port=8888", "--allow-root"]
CMD ["flask", "run", "--host=0.0.0.0"]
