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
	docker-compose -f docker-compose.prod.yml up --build --remove-orphans
	
launch-prod:	
	docker-compose -f docker-compose.prod.yml exec orthodontist python manage.py migrate --noinput
	docker-compose -f docker-compose.prod.yml exec orthodontist python manage.py collectstatic --no-input --clear
	docker-compose -f docker-compose.prod.yml exec orthodontist mkdir media/profile_pics
	docker-compose -f docker-compose.prod.yml exec orthodontist cp staticfiles/default.png media/profile_pics/

stop-prod:
	docker-compose -f docker-compose.prod.yml down --remove-orphans

test-data:
	docker-compose exec -T orthodontist python manage.py shell < orthodontist/test_data.py

backup-media:
	docker run --rm --volumes-from orthodontist_prod_orthodontist_1 -v $$(pwd):/backup alpine tar cvf /backup/backup-media.tar home/balthasar/orthodontist/media

restore-media:
	docker run --rm --volumes-from orthodontist_prod_orthodontist_1 -v $$(pwd):/backup alpine sh -c "cd home/ && tar xvf /backup/backup-media.tar --strip 1 && ls -l /home/balthasar/orthodontist/media/profile_pics"

backup-db:
	docker-compose -f docker-compose.prod.yml exec db pg_dumpall -c -U orthodontist > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql

restore-db:
	docker-compose -f docker-compose.prod.yml exec orthodontist python manage.py flush --no-input
	docker-compose -f docker-compose.prod.yml exec db psql --user=orthodontist --dbname=orthodontist_prod -c "CREATE DATABASE orthodontist;"
	cat $(filename) | docker-compose -f docker-compose.prod.yml exec -T db psql -U orthodontist