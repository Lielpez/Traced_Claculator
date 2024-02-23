FROM centos:7
RUN yum install python3 python3-pip -y 
WORKDIR /app
COPY . /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000 6831
CMD ["python3","/app/website_service.py"]
