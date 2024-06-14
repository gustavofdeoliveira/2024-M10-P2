# maintainer info
FROM alpine:3.18

WORKDIR /app
COPY requirements.txt ./

RUN apk update
RUN apk add python3 py3-pip
RUN pip3 install -r ./requirements.txt

COPY . ./

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

