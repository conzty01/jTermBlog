J-Term Blog
===========

Overview
--------

A simple blogging site created to document my adventures on a school trip. 

A running version of this blog can be found on Heroku here_.

Requirements
------------

This application runs on Python 3.5 and uses the below modules

	1. Flask
	2. Psycopg2
	3. Jinja2

	Along with PostgreSQL 9.5

Alternatively, you can just install the Python modules via the included requirements.txt:

::

	$ sudo pip install -r requirements.txt


Installation and Operation
--------------------------

Before running the server, you will need to set up the database with ``createDB.py``. You'll 
have to update the connection to the your PostgreSQL database with the approrpriate information.

::

	conn = psycopg2.connect(dbname=[DATABSE_NAME], user=[USER_NAME])

Afterwards, update the information in ``post.txt`` and add the post to the database with ``uploadProjects.py``.
Run the following command

::

	$ python server.py

and open your browser. By default, the flask application uses port 5000 and can be
accessed at http://localhost:5000/ .

.. _here: https://jterm-blogger.herokuapp.com/
