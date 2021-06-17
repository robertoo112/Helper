FROM trow.kube-public:31000/ubuntu
ADD ./gitrepo /app
RUN apt-get update && apt-get -y install python && apt-get -y install python3-pip
WORKDIR /app
RUN pip3 install flask pymongo flask-pymongo
CMD python3 /app/app2.py