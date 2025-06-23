SHELL := /bin/bash

# Container name
WEB_CONTAINER=marcus_web

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make init-db         Initialize migrations folder"
	@echo "  make migrate         Generate migration from models"
	@echo "  make upgrade         Apply migration to DB"
	@echo "  make downgrade       Rollback last migration"
	@echo "  make shell           Open bash shell in Flask container"

init-db:
	docker exec -it $(WEB_CONTAINER) python3 -m flask db init

migrate:
	docker exec -it $(WEB_CONTAINER) python3 -m flask db migrate -m "Auto migration"

upgrade:
	docker exec -it $(WEB_CONTAINER) python3 -m flask db upgrade

downgrade:
	docker exec -it $(WEB_CONTAINER) python3 -m flask db downgrade

shell:
	docker exec -it $(WEB_CONTAINER) bash
