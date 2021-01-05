FROM python:3.7-stretch
MAINTAINER Phu Tsoi <pntsoi@ucsd.edu>

# install build utilities
RUN apt-get update && \
	apt-get install -y gcc make apt-transport-https ca-certificates build-essential
#RUN python3 --version
#RUN pip3 --version


# set the working directory for containers
WORKDIR  /app
# Installing python dependencies

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

#ADD /watev/deployment /app
EXPOSE 5000
# Copy all the files from the project’s root to the working directory
COPY . .

# Running Python Application
# RUN python3 /usr/src/prediction-deployment/main.py
CMD ["python", "/app/main.py"]
