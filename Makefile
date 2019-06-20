run:
	docker-compose -f ./stack.yml up -d --build

stop:
	docker-compose -f ./stack.yml down

restart: stop run

ls:
	docker container ls
	
api:
	docker exec -it $$(docker container ls |grep api:latest | awk '{print $$1}') sh

job:
	docker exec -it $$(docker container ls |grep job:latest | awk '{print $$1}') sh

docker_images:
	docker images

git_reset:
	git fetch
	git reset --hard origin/master

init_projects:
	@hash glide > /dev/null 2>&1; if [ $$? -ne 0 ]; then \
		curl https://glide.sh/get | sh; \
	fi

	cd ./src/api \
		&& glide install \
		&& go get -d -v ./... \
		&& cd ../../

	cd ./src/py3/ \
		&& pip3 install -r requirements.txt --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ \
		&& cd ../../

update:
	@hash glide > /dev/null 2>&1; if [ $$? -ne 0 ]; then \
		curl https://glide.sh/get | sh; \
	fi

	cd ./src/api \
		&& glide update \
		&& go get -d -v ./... \
		&& cd ../../

	cd ./src/py3/ \
		&& pip3 install -U -r requirements.txt --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ \
		&& cd ../../

