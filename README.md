## **Installing Virtual Environment**

`apt-get install python3-venv`

## **Project SetUp**

To create a virtual environment, use the following command, where ".venv" is the name of the environment folder:

`python3 -m venv .venv`

Activate the virtualenv (OS X & Linux):

`source .venv/bin/activate`

You’ll need to activate your virtual environment every time you work on your Python project. In the rare cases when you want to deactivate your virtualenv without closing your terminal session, just use the deactivate command.

## **Package and Dependency Manager**

To install the package, you can just run:

`pip3 install <somepackage>` 

That will build an extra Python library in your home directory.

Running 'pip freeze',can help to check installed packages and packages versions listed in case-insensitive sorted order.

Save all the packages in the file with:

`pip freeze > requirements.txt`.

Add `requirements.txt` to the root directory of the project. Done.

If you’re going to share the project you will need to install dependencies by running

`pip install -r requirements.txt`

The recipient still needs to create their own virtual environment, however.

**OBS:** Use `pip3 install -r requirements.txt` if you are using Python3

# **Install Django**

`pip3 install Django`

## **Creating a Project**

`django-admin startproject <my-project-name> .`

This will create a **my-project-name** directory in your current directory.

# **The development server**

Let’s verify your Django project works.

`python manage.py runserver`

You’ve started the Django development server, a lightweight Web server written purely in Python.

### **Changing the Port**

By default, the runserver command starts the development server on the internal IP at port 8000.

If you want to change the server’s port, pass it as a command-line argument. For instance, this command starts the server on port 8080:

`python manage.py runserver 8080`

If you want to change the server’s IP, pass it along with the port. So to listen on all public IPs (useful if you want to show off your work on other computers on your network), use:

`python manage.py runserver 0.0.0.0:8000`

## Creating an app

To create your app, make sure you’re in the same directory as manage.py and type this command:

`python manage.py startapp <app-name>`

## **Use the collectstatic command**

For production deployments, you typically collect all the static files from your apps into a single folder using the python manage.py collectstatic command. You can then use a dedicated static file server to serve those files, which typically results in better overall performance. The following steps show how this collection is made, although you don't use the collection when running with the Django development server.

1. In `works_single_view/settings.py`, add the following line that defines a location where static files are collected when you use the `collectstatic` command:

`STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')`

2. In the Terminal, run the command `python manage.py collectstatic` and observe that `hello/site.css` is copied into the top level `static_collected` folder alongside `manage.py`.

3. In practice, run `collectstatic` any time you change static files and before deploying into production.

## **Work With Data, Data Models, and Migrations**

Many web apps work with information stored in a database, and Django makes it easy to represent the objects in that database using models. In Django, a model is a Python class, derived from `django.db.models.Model`, that represents a specific database object, typically a table. You place these classes in an app's `models.py` file.

With Django, your work with your database almost exclusively through the models you define in code. Django's "migrations" then handle all the details of the underlying database automatically as you evolve the models over time. The general workflow is as follows:

1. Make changes to the models in your `models.py` file.
2. Run `python manage.py makemigrations` to generate scripts in the migrations folder that migrate the database from its current state to the new state.
3. Run `python manage.py migrate` to apply the scripts to the actual database.

# **Database Bindings**

In addition to a database backend, you’ll need to make sure your Python database bindings are installed.

If you’re using PostgreSQL, you’ll need the `psycopg2` package. Use these following commands

`sudo apt-get install postgresql postgresql-contrib postgresql`

`sudo apt-get install python-psycopg2`

`sudo apt-get install libpq-dev`

The installation procedure created a user account called `postgres` that is associated with the default Postgres role. In order to use Postgres, we can log into that account.

Switch over to the postgres account on your server by typing:

`sudo -i -u postgres`

You can now access a Postgres prompt immediately by typing:

`psql`

You will be logged in and able to interact with the database management system right away.

Exit out of the PostgreSQL prompt by typing:

`\q`


## **Connecting to my Database**

psql is a regular PostgreSQL client application. In order to connect to a database you need to know the name of your target database, the host name and port number of the server, and what user name you want to connect as. psql can be told about those parameters via command line options, namely -d, -h, -p, and -U respectively. 

`psql -h <host> -p <port> -u <database>`
`psql -h <host> -p <port> -U <username> -W <password> <database>`
`psql -h hostname -U username -d database`


## **Configure PostgreSQL to allow remote connection [OPTIONAL]**

By default PostgreSQL is configured to be bound to “localhost”.

The port `5432` is bound to `127.0.0.1`. It means any attempt to connect to the postgresql server from outside the machine will be refused. We can try hitting the port 5432 by using telnet.

`telnet <host_ip_address> 5432`

## **Configuring postgresql.conf**

In order to fix this issue we need to find `postgresql.conf`, which if you are using linux, can be found at:

`/etc/postgresql/<version>/main`

Open `postgresql.conf` file and replace line

`listen_addresses = 'localhost'`

with

`listen_addresses = '*'`

You can use Vim to do that:

`sudo vim postgresql.conf`

Add the following lines to the `pg_hba.conf`

```
# Allow non-local connections
host    all             all             0.0.0.0/0               md5
host    all             all             ::/0                    md5

```

Now restart postgresql server and type:

`netstat -nlt`

Restart the server

`sudo service postgresql restart`

List all databases

`\l list databases`

First Connect with the Database using following command

`\c database_name`

If you only want to see the list of tables you've created, you may only say:

`\dt`

## **CREATING OUR DATABASE AND TABLES**

Run the file `data/works_single_view.sql` in order to generate the Database and Table of the project

`\i path_to_sql_file`

## **GUI Tools for PostgreSQL**

https://dbeaver.io/download/

## **Optimizing PostgreSQL’s configuration**

Django needs the following parameters for its database connections:

* **client_encoding: 'UTF8'**,
* **default_transaction_isolation: 'read committed'** by default, or the value set in the connection options (see below),
* **timezone: 'UTC'** **when USE_TZ** is **True**, value of **TIME_ZONE** otherwise.

If these parameters already have the correct values, Django won’t set them for every new connection, which improves performance slightly. You can configure them directly in postgresql.conf or more conveniently per database user with ALTER ROLE.

Django will work just fine without this optimization, but each new connection will do some additional queries to set these parameters.

When connecting to other database backends, such as MySQL, Oracle, or PostgreSQL, additional connection parameters will be required. See the ENGINE setting below on how to specify other database types. This example is for PostgreSQL:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

## **Creating Environmental Variables [OPTIONAL]**

Now, let's turn our shell variable into an environmental variable. We can do this by exporting the variable. The command to do so is appropriately named:

`export TEST_VAR="Testing  export"`

`printenv | grep TEST_VAR`

TEST_VAR=Hello World!
This time, our variable shows up. Let's try our experiment with our child shell again:

bash
echo $TEST_VAR
Hello World!

## **Deploy Python using Docker containers**

### **Install Docker CE Using the repository**

Follow the instructions in the documentation:

`https://docs.docker.com/install/linux/docker-ce/ubuntu/`

if you use Linux Mint use:

`sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"`

Make sure you also read "**Manage Docker as a non-root user**":

`https://docs.docker.com/install/linux/linux-postinstall/`

## **Docker Files for Django app**

A good base image for Django is `tiangolo/uwsgi-nginx:python3.6-alpine3.7`, which is also available for other versions of Python.

This base image already contains the production-ready uwsgi and nginx servers, but does not include Django. It's also necessary to provide settings to uwsgi so it can find the app's startup code.

## **Build Docker image**

`docker build --rm -f "Dockerfile" -t <image-name>:latest .`

When prompted for a name to give the image, use a name that follows the conventional form of `<registry or username>/<image name>:<tag>`, where `<tag>` is typically latest. Here are some examples:

```
# Examples for Azure Container Registry, prefixed with the registry name
vsdocsregistry.azurecr.io/python-sample-vscode-django-tutorial:latest
vsdocsregistry.azurecr.io/python-sample-vscode-flask-tutorial:latest
vsdocsregistry.azurecr.io/myexpressapp:latest

# Examples for Docker hub, prefixed with your username
vsdocs-team/python-sample-vscode-django-tutorial:latest
vsdocs-team/python-sample-vscode-flask-tutorial:latest
vsdocs-team/myexpressapp:latest
```

## **Run and Test Your Container**

Run and test your container locally by using the following command, replacing `<image_name>` with your specific image, and changing the port numbers as needed. For web apps, you can then open browser to `localhost:<port>` to see the running app.

`docker run --rm -it -p 8000:8000 <image_name>`

`docker run --rm -it -p 8000:8000 vs-code-tutorial`

## My approach to the problem

## **Basics of Entity Resolution with Python and Dedupe**

I found this solution the most complete and detailed, so I based my solution on the article bellow.

`https://medium.com/district-data-labsbasics-of-entity-resolution-with-python-and-dedupe-bc87440b64d4`


# **Google Style Guides**

For this project I am going to follow Google Style Guides convention. It is much easier to understand a large codebase when all the code in it is in a consistent style.

## **YAPF - Yet Another Python Formatter**

Most of the current formatters for Python --- e.g., autopep8, and pep8ify --- are made to remove lint errors from code. This has some obvious limitations. For instance, code that conforms to the PEP 8 guidelines may not be reformatted. But it doesn't mean that the code looks good.

In essence, the algorithm takes the code and reformats it to the best formatting that conforms to the style guide, even if the original code didn't violate the style guide. 

The goal using it is to end all holy wars about formatting - if the whole codebase of a project is simply piped through YAPF whenever modifications are made, the style remains consistent throughout the project and there's no point arguing about style in every code review.

The ultimate goal is that the code YAPF produces is as good as the code that a programmer would write if they were following the style guide. It takes away some of the drudgery of maintaining your code.

To install YAPF from PyPI:

`$ pip3 install yapf`

Usage: `yapf -i {source_file_or_directory}`

here `-i` is to make changes to files in place.

## **Pylint**

Pylint is a python linter which checks the source code and also acts as a bug and quality checker. It has more verification checks and options than just PEP8(Python style guide).

This is the most commonly used tool for linting in python.

* It includes the following features:
* Checking the length of each line
* Checking if variable names are well-formed according to the project’s coding standard
* Checking if declared interfaces are truly implemented.

`pip3 install pylint`

## **Installing Flake8**

Flake8 is just a wrapper around pyflakes, pycodestyle and McCabe script (circular complexity checker) (which is used to detect complex-code).

If we like Pyflakes but also want stylistic checks, we can use flake8, which combines Pyflakes with style checks against PEP 8.

`pip3 install flake8`

## **Tox**

`pip3 install tox`

## **Test Coverage**

## **Continuous Integration Tools**

## **Configuring Visual Studio Code to Work with Python**

Add the following in your `settings.json` file:

```json
"python.unitTest.unittestEnabled": true,
"python.linting.pylintEnabled": true,
"python.linting.flake8Path": "${workspaceRoot}/.venv/bin/flake8",
"python.linting.flake8Enabled": true,
"python.linting.flake8Args": [
    "--max-line-length=79"
],
"python.formatting.provider": "yapf",
"python.formatting.blackPath": "${workspaceRoot}/.venv/bin/yapf",
"editor.formatOnSave": true,
```

## **RESOURCES**

- https://docs.python.org/3/tutorial/venv.html 
- https://code.visualstudio.com/docs/python/tutorial-deploy-containers
- https://pip.readthedocs.io/en/stable/user_guide/#requirements-files 
- https://google.github.io/styleguide/pyguide.html
- https://github.com/google/yapf/
- http://books.agiliq.com/projects/essential-python-tools/en/latest/linters.html
- https://fedoramagazine.org/vscode-python-howto/
- https://code.visualstudio.com/docs/python/tutorial-django
- https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite
- https://docs.docker.com/install/linux/docker-ce/ubuntu/
- https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest
- http://www.postgresqltutorial.com/postgresql-hstore/
- http://www.postgresqltutorial.com/postgresql-array/
- http://www.postgresqltutorial.com/postgresql-unique-constraint/
- https://docs.djangoproject.com/en/2.1/ref/databases/#postgresql-notes
- https://docs.djangoproject.com/en/2.1/topics/testing/overview/
- https://pybit.es/persistent-environment-variables.html
- https://medium.com/agatha-codes/painless-postgresql-django-d4f03364989
- https://medium.com/district-data-labs/basics-of-entity-resolution-with-python-and-dedupe-bc87440b64d4