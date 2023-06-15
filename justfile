nacebeltoyaml:
  pipenv run python3 scripts/nacebel_to_yaml.py
  mv nacebel.yaml yago/quotes/seeds/0001_nacebel.yaml

migrate:
  pipenv run python3 yago/manage.py migrate

makemigrations:
  pipenv run python3 yago/manage.py migrate

createadmin:
  pipenv run python3 yago/manage.py createsuperuser

run:
  pipenv run python3 yago/manage.py runserver

flush:
  pipenv run python3 yago/manage.py flush

seed:
  pipenv run python3 yago/manage.py loaddata yago/quotes/seeds/0001_nacebel.yaml
  pipenv run python3 yago/manage.py loaddata yago/quotes/seeds/0002_nacebel_code_advices.yaml
  pipenv run python3 yago/manage.py loaddata yago/quotes/seeds/0003_nacebel_code_cover_advices.yaml