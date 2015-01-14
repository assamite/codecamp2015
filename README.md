 Group CALCULUS, ProSECCO Code Camp, January 2015
=================================================

Project: News headline and movie title collider

Install Notes
=============

Codecamp is developed as a [Django](https://djangoproject.com/) app. Access to 
[Twitter API](https://dev.twitter.com/overview/documentation) is gained using 
[tweepy](http://www.tweepy.org/).

You should be familiar with basic Django project layout and have a working 
[Twitter app](https://apps.twitter.com/) which allows you to Tweet before 
using this project.

**Short installing notes:**

* Clone (or fork) project's git-repository::

	```
	$> git clone https://github.com/assamite/codecamp.git
	``

* Install [pip](https://pypi.python.org/pypi/pip)
* Install third party libraries::

	```
	$> cd project_root/
	$> pip install -r requirements.txt // you might need root privileges
	```
	
* Create local settings file::

	```
	$> cd project_root/codecamp/
	$> touch lsettings.py
	```
	
* Configure ``lsettings.py``  with at least following attributes (see Twitter API documentation for details)::

	```
	SECRET_KEY = 'Secret key for Django'
	TWITTER_API_KEY = 'Your Twitter API key'
	TWITTER_API_SECRET  = 'Your Twitter API secret'
	TWITTER_ACCESS_TOKEN = 'Your Twitter access token'
	TWITTER_ACCESS_TOKEN_SECRET = 'Your Twitter access token secret'
	```

* Create DB-tables::
	
	```
	$> cd project_root/
	$> python manage.py syncdb
	```

* Configure project's cronjobs to be run every 5 minutes (or so)

	.. warning::
		This will make your bot to Tweet every once in a while, so only do this
		when you are ready to face the consequences.
		
		**If you just want to test the bot locally, don't enable cronjobs.**

	* Open crontab in new editor from terminal::

		```
		$> env EDITOR=nano crontab -e
		```
		
	* Write the cronjob on new line (you need to change the paths to your bash profile and project)::
	
		```
		*/5 * * * * source ~/.bash_profile && python path/to/codecamp/manage.py runcrons > path/to/codecamp/logs/cronjob.log
		```
		
	* Save and exit. Now the terminal should say something like::
	
		```
		crontab: installing new crontab
		```
	
**Local Usage:**
	
* Run the Django's builtin test server::

	```
	$> python manage.py runserver
	```
	
* Now the web site should be served for you in ``127.0.0.1:8000/``
	


