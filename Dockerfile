FROM public.ecr.aws/amazonlinux/amazonlinux:2.0.20211005.0-amd64

RUN yum install -y python3
RUN pip3 install awscli boto3 requests

COPY ./processor.py /

CMD ["/processor.py"]