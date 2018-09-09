# Gruplac analysis

Analisis de los grupos de investigación identificados por colciencias en todo el
país. Creación de un modelo matematico que permita a la vicerrectoria de
investigación, innovación y extensión UTP, tomar mejores decisiones frente a la
inversion de recursos y esfuerzo en los grupos de investigación de la UTP.

## Project dependencies

- Python 3.7
- pip for Python3
- virtualenv
- Node.js >= 8.X.X
- yarn or npm (package manager for Node.js)
- MongoDB

Inside '/grupvis' there are two important subfolders, first we have
'grupvis/script' which contains everything related with the colciencias' page
scraping and second, inside 'grupvis/app' we can find the web server and the
React client.

# Starting with the project

## Let's see first how setting up the scraping part

Get inside 'grupvis/script' folder

#### Create a virtual enviroment

```bash
virtualenv  -p /usr/bin/python3 env/
```

#### Activate enviroment

This must be done every new session. Before installing or using something make
sure env is active.

```bash
source  env/bin/activate
```

Previous code is for bash shell, but there is also activation script for fish
shell. Just use:

```bash
source  env/bin/activate.fish
```

#### Then install the packages

```bash
pip3 install -r top-requirements.txt
```

And thats all.

## Now let's see how to set up the web part

This time get inside 'grupvis/app' folder

#### Installing server modules

Just run:

```bash
yarn
```

then enter to 'client' folder and run same command. That's all.

## Jupyter notebooks

- Download the data and save it in `datasets/` folder

- Run jupyter notebook

```bash
jupyter notebook
```

## Run scraping script

In order to scrape groups' information first make sure mongoDB service is
running, then get into './script/scienti/scienti' folder and run:

```bash
scrapy crawl research_groups
```

For redirecting the log messages use following command:

```
scrapy crawl research_groups --logfile filename.log
```

This will save scraped data into mongo database

## Run web app

- TODO
