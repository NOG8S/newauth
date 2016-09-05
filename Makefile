RUN=docker run -t -v $(CURDIR):/usr/src/app -p 5002:5002 newauth

build:
	docker build -t newauth .
	$(RUN) bower install
	$(RUN) mkdir /usr/src/app/migrations/versions/
	$(RUN) python manage.py assets build

init:
	$(RUN) python manage.py db migrate
	$(RUN) python manage.py db upgrade

run:
	$(RUN)
