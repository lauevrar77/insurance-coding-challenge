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

## Executing unit tests on the app
This app has a minimal unit tests coverture. They are mainly focused on the domain and the more "usefull" parts. 
At start, I developped like I would normally do, with as much tests as possible and in a TDD approach. However as time flew by, I was forced to lower my expectations in term of tests coverage. This would never happen in a real production codebase

To execute the tests : `just test`

## User manual
### Normal user
Just access the root of the website. You will be welcomed with the quote form. 
The following steps should be pretty straigthforward. 

Note that the "submit button" is at the end of the page.

### Admin user
Access the `/admin` URI of the website. 

Next you can connect with the credentials you received by email. 

#### Add advice for a nacebel code
Once connected, access the `Nacebel code advices` link in the `Quotes` menu.

You will see the list of all existing code advices. This list is searchable by code. 

Next on the top right of the page, you can click the `Add Nacebel code advice` button the access the adding form

In this form you can select one of the level 5 codes, the `deductible formula` and the `coverage ceiling formula`. Finally, you can add one or more suggested covers for this code.

When you are done just click the `Save` button.

Once done, future quotes asking for this code will be enriched with your suggestion.

#### Access the existing quotes
Once connected, access the `Quote simulations` link in the `Quotes` menu.

You will see the list of all existing quotes. This list is searchable by different criterions and filterable by review status.

Next, click one of the existing quotes. 

You will access it and see all the information involved.

You will notice that : 
* Enterprise and Lead Contact menus are not very "filled with information". They are just pointers to other domain objects accessible in their own menus.
* The list of codes may seem useless but selected ones have a different background color
* The simulated quote is a pointer to another domain object that retains the raw information from the insurer's API endpoint
* The `reviewed` field allows a salesperson to mark that the client linked to this simulation have already been contacted. 
* The adviced cover field represent the adviced covers from `Nacebel code advices`

## Repository structure
The root of this repository contains : 
* A `scripts` directory. It contains some scripts used mainly for oneshot data transformation (for seeds).
* Some files for editor and tools configuration
* `justfile` the file used to configure the `just` command. It's like a `makefile`but with an easier and more modern synthax (in my opinion at least)
* `nacebel.csv` : the raw nacebel codes csv
* `Pipfile` and `Pipfile.lock` : used for Python dependencies management
* `requirements.txt` : standardized export of dependencies better handled in `Pipfile`
* `yago` : the Django app. Its structure will be explained in the following section

### The `Yago` directory
* `manage.py` : allows to manage the Django project. The just file contains a lot of commands using this file
* `yago` directory : the base django app. Files other than the `settings.py` are not very usefull
* `quotes` directory : the app developped for this technical challenge. Its structure will be described in the following section.

### The `quotes` directory
* `models.py` and `models_test.py` : contain the domain objects and their tests. I would prefer to make this a directory with one file per domain object but Django seems quite "touchy" with this file and the structure of the project.
* `views.py` : where the views are defined. Architecturaly, my usual aim is that views contains as less business logic as possible. I would even prefer to cut `adapters` (marshaling, unmarshaling) from `endpoints`(receive requests as plain objects) but it doesn't seem easy in Django. In that purpose (as less business logic as possible), `persistance views` and `usecases` are introduced in the `infrastructure` layer. These classes take `commands` as arguments to make them able to manage requests from http views as well as (even if it is not the case here) asynchronous tasks from queues or GRPC requests.
* `urls.py` : Mapping between URLs and views
* `templates` : directory for html templates
* `seeds` and `migrations` : directories for migrations and seeds
* `infrastructure/persistance/views` : Contains objects aimed to make queries (and only queries) on the database. This clear distinction between "query side" and "write side" make simpler and smaller objects. Views receive requests as `commands` to allow to :
  * executes them later if necessary
  * replay a failed command if necessary
  * receive the same query from different http views or protocols
  * ... 
* `infrastructure/services` : place where internal and external services are defined. 
* `usecases` : interface between the "communication side of the app" (communication from and to the client or external systems) and the domain model. The aim of usecases is to load the domain object and apply the received command on them. It is the domain model the contains the business logic. Usecases are just and interface between the domain model and the outside worl and the domain model. 
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

### Suggestion system
The suggestion system works by creating `Nacebel code advices`.

This domain object's aim is to represent the adviced `deductible formula`, the `coverage ceiling formula` as well as adviced covers for the selected code. 

If a quote has multiple `Nacebel codes`, all the `advices` would be loaded from the database and merged using the following algorithm : 
* For each `deductible` and `coverage ceiling` formulas, the maximum value is selected among the once present in the advices
* The `adviced covers` are all adviced.


#### Note
At the moment, `Nacebel code advices` can only be created for `level 5` code. This hypothesis was made for simplification reasons. It would be "quite easy" to remove it (if it is meaninful for the business). 

Each `level 5` code would be divided in its constituting parts and each part would be queried in the database for `Nacebel code advices`. The advices merging algorithm wouldn't need to be modified.

### Not separating frontend and backend
In this challenge, the frontend and the backend are tighted in a single application.

This may seem a "bad practice" as of today's standards as technologies as VueJS often live in another repository and request the backend application via API requests. 

If I totally agree with this argument, I made this choice of using a single codebase and simple technologies as it is a technical challenge were the frontend is explicitely said to not be a priority (this is also the reason why it is so "rudimentary" and ugly).

The downsides of this choice are however counterbalanced by the usage of `commands` in `persitance views` and `usecases`. Indeed, with this pattern it is "quite easy" to add more transports (API for instance) to the app. API endpoints would just have to be created and create `commands` that are sent to usecases and views.

### Not sending an email with the quote URL
The exercise asked to send a link to the quote in an email to the client. 

I decided not to send the email. I only advertise the user that he can save the link of the quote for later use.

I took this decision as sending the email is a technical complexity that doesn't offer much business value. 

It doesn't seem mandatory in a MVP (minimum viable product)

## Security concerns
* Credentials are outside the codebase 
* The Docker container runs with a non priviledged user
* It should be deployed with a readonly filesystem

For the purpose of this challenge, I didn't generate a proper SSL certificate for the website but it would be mandatory for real production trafic.

## Possible enhancements 
- [ ] Have a proper unit test coverage
- [ ] Fix nacebel english labels that are always empty
- [ ] Make sections and level collapsible in the form
- [ ] Create a single view with all the information on the admin interface
- [ ] Creating a real tree structure on the naceel codes table
- [ ] Add CSS and make it beautiful
- [ ] Make code sections a dropdown
## Possible (but possibly premature) optimisations
* Pre-render codes tree for form