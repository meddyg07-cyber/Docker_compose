COMPOSE = docker compose -f docker-compose.yml

.PHONY: up down purge_bdd purge_all

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

# Supprime UNIQUEMENT les données PostgreSQL
purge_bdd:
	$(COMPOSE) down
	docker volume rm ex04_pgdata || true
	$(COMPOSE) up -d

# Nettoyage TOTAL du projet
purge_all:
	$(COMPOSE) down --volumes --remove-orphans

	# Suppression des images Docker
	docker image prune -af

	# Suppression des volumes Docker
	docker volume prune -f

	# Suppression des réseaux Docker
	docker network prune -f

	# Suppression des dossiers générés (cache, build, etc.)
	rm -rf backend/node_modules frontend/node_modules
	rm -rf backend/**/__pycache__ frontend/**/__pycache__
	rm -rf backend/dist frontend/dist
	rm -rf backend/.cache frontend/.cache

	# Relance complète du stack
	$(COMPOSE) up -d --build
