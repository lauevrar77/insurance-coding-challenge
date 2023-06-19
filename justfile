set dotenv-load

nacebeltoyaml:
  pipenv run python3 scripts/nacebel_to_yaml.py
  mv nacebel.yaml yago/quotes/seeds/0001_nacebel.yaml

migrate_local:
  pipenv run python3 yago/manage.py migrate

migrate_docker:
  docker compose exec web python3 manage.py migrate

makemigrations:
  pipenv run python3 yago/manage.py migrate

createadmin:
  pipenv run python3 yago/manage.py createsuperuser

createadmin_docker:
  docker compose exec web python3 manage.py createsuperuser

run_local:
  pipenv run python3 yago/manage.py runserver

run_docker:
  docker compose up -d

down_docker:
  docker compose down

flush_local:
  pipenv run python3 yago/manage.py flush

flush_docker:
  docker compose up -d
  docker compose exec web python3 manage.py flush
  docker compose down 
  rm -r data

lock:
  pipenv requirements > requirements.txt

test:
  cd yago; DJANGO_SETTINGS_MODULE="yago.settings" pipenv run python3 -m pytest

seed_local:
  pipenv run python3 yago/manage.py loaddata yago/quotes/seeds/0001_nacebel.yaml
  pipenv run python3 yago/manage.py loaddata yago/quotes/seeds/0002_nacebel_code_advices.yaml
  pipenv run python3 yago/manage.py loaddata yago/quotes/seeds/0003_nacebel_code_cover_advices.yaml
  
seed_docker:
  docker compose exec web python3 manage.py loaddata quotes/seeds/0001_nacebel.yaml
  docker compose exec web python3 manage.py loaddata quotes/seeds/0002_nacebel_code_advices.yaml
  docker compose exec web python3 manage.py loaddata quotes/seeds/0003_nacebel_code_cover_advices.yaml