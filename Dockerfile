FROM python:3.9
COPY . /src
COPY ./requirements.txt /src/requirements.txt
WORKDIR src
EXPOSE 80:80
RUN pip3 install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
