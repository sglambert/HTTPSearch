# HTTPSearch Repository
The code in this repository is based around making HTTP requests to websites and then sending information generated from the requests to users.

My partner likes to purchase second hand clothing on Depop. Unfortunately, the website does not have functionality to send email alerts when someone has posted something you're looking for. Therefore, I've created this little script to solve this problem.

I'm hoping to build on this functionality, clean up the code a bit more, and generalise the program so it can generate data from other websites.

SETUP GUIDE:

There are several things that need to be setup to run this code:
1) Download and install Python and Postgres.
2) Setup a gmail account with an app password: https://support.google.com/accounts/answer/185833?hl=en
3) Fill in and save the details in the configuration file configuration.py.
4) Schedule the script to run on your machine. For Windows operating systems, I used Windows Task Scheduler. There should be similar tools available for OSX and Linux operating systems.
