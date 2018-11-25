# Feature Requester

This app helps you manage feature request from your customers. Online version for this app can be found here - https://rquesta.herokuapp.com/

## Prequisite

This app uses the following technologies:

- Python 3.6+
- ES6
- KnockoutJS (for DOM manipulation)
- Bootstrap (for the front-end)

To get this project up and running on your local machine, make sure you have:
 - [Python 3.6](https://www.python.org/downloads/) or higher installed on your machine.

Next, open up a command interface and clone the project:

```bash
   $ git clone https://github.com/dongido001/feature-request-app.git
```

Then change your current location to the project root folder:

```bash
   $ cd feature-request-app
```

From your command line, change your directory to the Flask project root folder, execute the below command:


    $ python3 -m venv env

Or:


    $ python -m venv env

The command to use depends on which associates with your Python 3 installation.

Then, activate the virtual environment:


    $ source env/bin/activate

If you are using Windows, activate the virtualenv with the below command:


    > \path\to\env\Scripts\activate

This is meant to be a full path to the activate script. Replace `\path\to` with your correct path name.

Next, install dependencies:

```bash
   $ pip install -r requirements.txt
```

Next, run the migration and seed the database with some data:

```bash
   $ python run.py db init 
   $ python run.py db migrate 
   $ python run.py db upgrade
   $ python run.py seed
```

Finally, start up the server:

```
  $ python run.py runserver
```

By default, this will start a web server accessible from http://127.0.0.1:5000/

Congrats! feel free to play around with the app. 

The app is protected with a password, the default detail is:

```bash
Username: login
Password: login
```

You can find this detail in `seeder.py`.
