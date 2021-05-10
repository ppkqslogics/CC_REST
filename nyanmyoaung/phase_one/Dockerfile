#pull base image from docker hub
FROM python:3.8

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#set work directory
WORKDIR /code

#install dependencies
COPY requirements.txt /code/
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

#copy project
COPY . /code/

# ssh
#ENV SSH_PASSWD "root:Docker!"
#RUN apt-get update \
#    && apt-get install -y --no-install-recommends dialog \
#    && apt-get update \
#    && apt-get install -y --no-install-recommends openssh-server \
#    && echo "$SSH_PASSWD" | chpasswd 

#COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh
#Expose ports for django and ssh
#EXPOSE 8000 2222

EXPOSE 8000

#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
#ENTRYPOINT ["init.sh"]
