# Every Breath of the Way

## The Project:

Every Breath of the Way, is a personalized monitoring tool for users to gain greater insight 
into their Asthma. Ever Breath of the Way is built in Python with a Flask framework, uses a SQLite database,
and integrates  Charts.js, Google Maps Api, Twitter, and DISQUS.

Scientific studies show that the health problems face by asthma sufferers can be almost completely
brought under control with careful maintanence.

Every Breath of the Way allows users to track their asthma attacks with ease- 
providing users an online up-to-date log of their health. Through the asthma dashboard users can 
unveil trends regarding frequency, common triggers, and symptoms of attacks. 
Users can share attackinformation with their primary physician, providing the physician a platform from which to make more 
informed decisions on how to best manage their patients asthma. Users can also share invaluable tips about controlling asthma through the DISQUS forum, and learn about current asthma, and lung information by monitoring the live Tweets of the American Lung Association.

#### Table of Contents
- [Technologies](#technologies)
- [Project Details](#project-details)
  - [The Database](#the-database)
    - [Password Encryption] (#password-encryption)
    - [Twitter and DISQUS](#twitter-and-disqus)
    - [Charts and DataTables](#charts-and-datatables)
- [Project Structure](#project-structure)
- [Try it Yourself!](#try-it-yourself)
- Next Steps

##Technologies:
 
**Backend**
Python, Flask, SQLAlchemy, PyCrypto, Google Maps API

**Frontend**
Charts.js, Javascript, HTML, CSS, Bootstrap, DataTable.js

##Project Details
####The Database
The Sqlite database uses SQLAlchemy as its ORM and contains table user, attack, attack syptoms, symptoms, attrack triggger,   and possible triggers.
To seed the attack triggers, and attack symptoms tables, I used the Lung Association most common Asthma attack triggers, and symptoms, and wrote that data into two separate files u.triggers, and u.symptoms. The data was cleaned using the script seed.py
  
####Password Encryption
Upon reviewing my database queries for each user, I noticed that I was storing user's passwords in the database in plain text which poses a security risk. I was able to significantly improve password security by using Crypto.Hash SHA256 to hash the passwords, generating a number value from their plain text value, and storing the hashed version in the database.

####Twitter and DISQUS
Every Breath of the Way  is also a place to share, and gather information to become an Asthma Warrior,
someone who is in control of their asthma. The DISQUS widget allows user to share, and gather information
in an open community forum. 
Users can also see live tweets from the American Lung Association which provide up-to-date information about air-quality, seasonal precautions and actives, etc. 

####Charts and DataTables
######Charts.js
The dashboard of the app allows users to visualize multiple components of their Asthma 
attacks( for a month by month, and trigger by trigger comparison with real-time updates). 
It uses charts.js, an open-source nimble charting library, to display the data. The line graph displays the frequency of
the users asthma attacks over time, and the doughnut chart allows for comparison of the possible triggers present in the 
user's attack. 

Both charts contain real-time information about the user’s attack. The chart data is derived from 
querying the database base on the user id in session, and attacks assocaited with that id. Then through and effective use of backrefs relationships in my database I manipulated returned data- utilizing for-loops aggregrate the data and convert the response into JSON to display on the front-end charts.

######DataTables.js
With the help of the DataTables.js., a user can interface with the table to get a brief summary
of the number of symptoms, and triggers in each attack by by date. The information is style using Jinja  and standard table formatting. The user also has the ability to dive deeper into their attacks by accessing specific details of the attack through the date hyperlink situated on the jquery created table.

##Project Structure

  ***Main application files***

* server.py: core of the Flask app, lists dashboard, log indicent routes, and contains all server API 
endpoints sending data to client

* model.py: Database class declarations and class methods

* seed.py: Script to import symptoms, and triggers into the Database

*Templates Directory: html templates that implement Jinja2 for template inheritance to render pages in the browser.

*Static Directory: 
  - Images: Logo
  - JS: Jquery, Boostrap, Charts.js DataTables.js

## Try it Yourself!
 
#####Environment 

1) Clone the repository:

<pre><code>$ git clone https://github.com/kcart/Every-Breath-of-the-Way.git</code></pre>

2) Create and activate a virtual environment in the same directory: 

<pre><code>$ pip install virtualenv
$ source env/bin/activate/
</code></pre>

3) Install the required packages using pip:

<pre><code>(env)$ pip install -r requirements.txt
</code></pre>

#####Database

1) Create the database, create the database using Python:

<pre><code>(env)$ python -i model.py
(env)$ create_db()
</code></pre>

2) Still in your virtual environment, create the database tables and seed the standards table:

<pre><code>(env)$ python model.py
(env)$ python seed.py
</code></pre>

3) Run the app: 

<pre><code>(env)$ python server.py
</code></pre>

4) Point your browser to:

<pre><code>http://localhost:5000/</code></pre>

## Next Steps

##### Heat map of users attack.

