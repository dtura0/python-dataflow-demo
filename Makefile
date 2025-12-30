.PHONY: init run test down

init:
	docker compose up -d db
	docker compose build
	docker compose run --rm db_init

run:
	docker compose run --rm app

test:
	docker compose run --rm test

clean:
	docker compose down -v
