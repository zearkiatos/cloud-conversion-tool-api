activate:
	source run.sh; activate

install:
	source run.sh; install

run:
	source run.sh; run $(port)

docker-up:
	source run.sh; docker_up

docker-down:
	source run.sh; docker_down

docker-dev-up:
	docker compose -f=docker-compose.develop.yml up --build

docker-pubsub-down:
	docker exec -it gcloud-pubsub-queue gcloud pubsub topics delete task-convert
	docker exec -it gcloud-pubsub-queue gcloud pubsub subscriptions delete task-convert-subscription

docker-dev-down:
	make docker-pubsub-down
	docker compose -f=docker-compose.develop.yml down


run-docker:
ifeq ($(strip $(port)),)
	flask run -h 0.0.0.0
else
	flask run -p $(port) -h 0.0.0.0
endif

docker-gunicorn:
	gunicorn --bind 0.0.0.0:5000 wsgi:app