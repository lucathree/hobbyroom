local: build-local run-local

build-local:
	docker-compose -f docker-compose.local.yml build

run-local:
	docker-compose -f docker-compose.local.yml up
