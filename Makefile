run_parallel:
	docker compose up --build

run_serial:
	docker compose -f docker-compose-serial.yml up --build