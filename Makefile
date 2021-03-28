start:
	docker-compose up --remove-orphans

stop:
	docker-compose down --remove-orphans

migrate:
	docker-compose exec orthodontist python manage.py migrate

makemigrations:
	docker-compose exec orthodontist python manage.py makemigrations

startapp:
	docker-compose exec orthodontist python manage.py startapp $(name)
	docker-compose exec orthodontist chmod -R a+w $(name)/
	docker-compose exec orthodontist ls -l

shell:
	docker-compose exec orthodontist python manage.py shell

psql:
	docker-compose exec db psql --user=orthodontist --dbname=orthodontist_dev

flush:
	docker-compose exec orthodontist python manage.py flush --no-input


start-prod:
	docker-compose -f docker-compose.prod.yml up --remove-orphans

stop-prod:
	docker-compose -f docker-compose.prod.yml down --remove-orphans