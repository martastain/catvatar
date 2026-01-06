IMAGE_NAME := martastain/catvatar:latest

.PHONY: build push

build:
	docker build -t $(IMAGE_NAME) .

push: build
	docker push $(IMAGE_NAME)

run: build
	docker run -p 8000:8000 $(IMAGE_NAME)
