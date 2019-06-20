# ================= api =================
FROM golang:1.12 as api

# Define working directory.
WORKDIR /go/src/app

# 安装动态执行的golang库
RUN go get github.com/codegangsta/gin

# 替换源
COPY ./etc/apt/sources.list /etc/apt/sources.list

# 安装软件包
RUN set -xe \
  && echo " # Install ..." \
  && apt-get update \
  && apt-get install -y \
  net-tools \
  netcat \
  && rm -rf /var/lib/apt/lists/*

# 暴露端口
EXPOSE 3000

# 启动镜像
CMD gin run main.go

# ================= job =================
FROM golang:1.12 as job

# Define working directory.
WORKDIR /home/job

# 安装动态执行的golang库
RUN go get github.com/codegangsta/gin

# 替换源
COPY ./etc/apt/sources.list /etc/apt/sources.list

# 安装软件包
RUN set -xe \
  && echo " # Install ..." \
  && apt-get update \
  && apt-get install -y \
  cron \
  net-tools \
  netcat \
  bc \
  && rm -rf /var/lib/apt/lists/*

# Copy hello-cron file to the cron.d directory
COPY ./src/job/crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab \
  # Apply cron job
  && crontab /etc/cron.d/crontab

# 启动镜像
CMD ["cron", "-f"]

# ================= docker jobs =================
FROM willfarrell/crontab as crontab

WORKDIR /opt/crontab

COPY ./src/job/config.json ${HOME_DIR}/

# ================= python3 =================
FROM python:3 as python3

WORKDIR /usr/src/app

COPY ./src/py3/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
  --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/

# 暴露端口
EXPOSE 5000

CMD FLASK_APP=qiming FLASK_ENV=development flask run --host=0.0.0.0