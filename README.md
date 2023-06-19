# Insurance technical challenge
The aim of this challenge is to create a insurance simulation system.
* The user fills a form with his information
* These information are saved for later sale usage
* These information are used to simulate a quote with the help of an external system
* A recommandation is made on the covers and ceiling the user should make
* The result is presented to the user with a possibility for him to go back to it later

## Implemented features

### For the user
The user can :
* Fill the form
  * Personal information
  * Enterprise information
  * Domain of activity
* Get his quote 
* Be adviced of the best covers for his domain of activity
* Go back to his quote later (via a unique URL)

### For the sales persons
The sales persons can :
* Connect to an admin interface 
* Input data in the covers recommandation system
* Access existing quotes
* Modify a quote to mark it as "reviewed" : here we suppose that a cover is reviewed when the sales person have contacted the lead in order to contractualize the quote or cancel it.


## Install global dependencies
* `just` : on macos `brew install just` should be enough
* `docker` and `docker compose`

If you want to run the app locally (not on docker)
* `python 3.10` : suggested installation method is through `asdf` 
* `pipenv` for python dependencies management : `pip3 install pipenv`

## Run the app via Docker

### Configure
Copy `.env.example` to `.env`.

An example configuration is like this : 
```
INSURER_ENDPOINT="https://staging-gtw.seraphin.be"
INSURER_API_KEY="changeme"
POSTGRES_NAME="postgres"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="suchpassword"
POSTGRES_HOST="db"
DEBUG="False"
```

Don't forget to **change the api key**

### Run
The simplest method is via : `just run_docker`

This will run the app via `docker compose`.

However, this is not enough to have a fully functionnal app.

You also have to `migrate` and `seed` the database

### Migrate the database
`just migrate_docker`


### Seed the database
`just seed_docker`

### Create admin user
Creating an admin user is mandatory to connect to the sales/admin interface (at URI `/admin`)

To create an admin user : `just createadmin_docker`


## Design decisions
### Using a complete web framework
For this technical challenge, I decided to use a features-full web framework ([Django](https://www.djangoproject.com)). 

I hesitated for a long time between Django and using a more minimalist framework (where I would have more things to do by myself). My thinking was that this kind of framework does a lot of things for you and that may not be suitable for a technical test (as a technical test is made for you to show your abilities, not the ones of the web framework).

I finaly decided to select Django as :
- When seniority of a developper grows, he often use simpler and simpler approach (KISS)
- In a production environment, this kind of features-full web framework is the most suitable
- It allows to focus on the business case and not technical details
- It certainly ensure a more robust app
- It reduces the time to market of a feature
- Yago uses this kind of web framework (Rails)
- Django is quite similar to Rails
- Django automaticaly provides an admin interface that allows Yago's salespeople to see the lead's contact information

However a downside of using Django is that I am not as familiar with this technology.

### Justfile
...

### Suggestion system
...

### Not separating frontend and backend
...

### Not creating a tree structure in the nacebel codes table

### Not sending an email with the quote URL

## Hypothesis
### Advices only on five digits codes
* Not enforced on admin interface at the moment

## Security concerns

## Possible enhancements 
- [ ] Fix nacebel english labels that are always empty
- [ ] Make sections and level collapsible in the form
- [ ] Create a single view with all the information on the admin interface
## Possible (but possibly premature) optimisations
### Pre-render codes tree for form