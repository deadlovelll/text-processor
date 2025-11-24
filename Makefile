run_parallel:
	docker compose up --build

run_parallel_optimized:
	docker compose -f docker-compose-optimized.yml up --build

run_serial:
	docker compose -f docker-compose-serial.yml up --build

run_serial_optimized:
	docker compose -f docker-compose-serial-optimized.yml up --build