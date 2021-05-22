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
	docker-compose -f docker-compose.prod.yml up -d --build --remove-orphans
	sleep 15
	docker-compose -f docker-compose.prod.yml exec orthodontist python manage.py migrate --noinput
	docker-compose -f docker-compose.prod.yml exec orthodontist python manage.py collectstatic --no-input --clear
	docker-compose -f docker-compose.prod.yml exec orthodontist mkdir media/profile_pics
	docker-compose -f docker-compose.prod.yml exec orthodontist cp staticfiles/default.png media/profile_pics/

stop-prod: backup-data
	docker-compose -f docker-compose.prod.yml down --remove-orphans


test-data:
	docker-compose -f docker-compose.prod.yml exec orthodontist python manage.py flush --no-input
	docker-compose -f docker-compose.prod.yml exec -T orthodontist python manage.py shell < orthodontist/test_data.py

backup-data:
	docker run --rm --volumes-from orthodontist_prod_orthodontist_1 -v $$(pwd)/orthodontist/backup:/backup alpine tar cvf /backup/media_`date +%d-%m-%Y"_"%H_%M`.tar home/balthasar/orthodontist/media
	docker-compose -f docker-compose.prod.yml exec db pg_dumpall -c -U orthodontist >  orthodontist/backup/db_`date +%d-%m-%Y"_"%H_%M`.sql

restore-data:
	docker run --rm --volumes-from orthodontist_prod_orthodontist_1 -v $$(pwd)/orthodontist/backup:/backup alpine sh -c "cd home/ && tar xvf /backup/$(media) --strip 1 && ls -l /home/balthasar/orthodontist/media/profile_pics"
	docker-compose -f docker-compose.prod.yml exec orthodontist python manage.py flush --no-input
	docker-compose -f docker-compose.prod.yml exec db psql --user=orthodontist --dbname=orthodontist_prod -c "CREATE DATABASE orthodontist;"
	cat orthodontist/backup/$(db) | docker-compose -f docker-compose.prod.yml exec -T db psql -U orthodontist
