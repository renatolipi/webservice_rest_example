# RESTFUL WEBSERVICE EXAMPLE


#### INDEX:

 - ##### INSTALL:

     - ###### Create your virtualenv

     - ###### Clone this repo

     - ###### Setup your database

 - ##### HOW TO USE

     - ###### Listing addresses

     - ###### Including an address

     - ###### Removing an address


---

### Install:


##### Warning:

This project was created and tested on Ubuntu 12.10. 
The database used was sqlite3. No extra packages were necessary on Ubuntu 12_10.
*If you had any problem while installing this project, please contact me.*


**Go to your project path:**

    cd /path/to/my_project


**CREATE YOUR VIRTUALENV:**

    /path/to/my_project$  virtualenv VENV


**Activate it:**

    /path/to/my_project$  source VENV/bin/activate


**You'll see your virtualenv active as below:**

    (VENV)/path/to/my_project$


##### CLONE THIS REPO:

**On your "*my_project*" folder:**

    (VENV)/path/to/my_project$ git clone git@github.com:renatolipi/webservice_rest_example.git


**When ready, go to the project's folder:

    (VENV)/path/to/my_projects$  cd webservice_rest_example


**update your pip:**

    (VENV)/path/to/my_project/webservice_rest_example$  pip install -U pip


**Now, you'll need to install its requirements:**

    (VENV)/path/to/my_project/webservice_rest_example$  pip install -r requirements.txt


---

##### From now on... I'm considering you have your on `/path/to/my_project/webservice_rest_example$` and your VENV is active.

---

##### SET UP YOUR DATABASE:

    python desafio/manage.py migrate

A lot of "Applying..." lines will come. If they're all OK, then you're DONE.


---

** Automated tests:**

Run the automated tests to check if everything is working:

    pip install -r test_requirements.txt


then:

    python desafio/manage.py test zipservice


---

### How to use:

To run this app locally, enter the line below and keep it running:

    python desafio/manage.py runserver


We'll use "*curl*" for this example, but you can use some browser extensions such as "*POSTMAN*" or "*Advanced REST Client*".


**LISTING ADDRESSES** with curl:

On another terminal you can type:

    curl http://localhost:8000/zipcode/

Or you can limit your search using query string, such as below:

    curl http://localhost:8000/zipcode/?limit=1


**INCLUDING AN ADDRESS** with curl, giving a ZIP CODE:

    curl --data "zip_code=04002020" http://localhost:8000/zipcode/


**REMOVING AN ADDRESS** with curl, giving a ZIP CODE:

    curl -X DELETE http://localhost:8000/zipcode/04002020/


*Don't forget the trailing slash ("/")*
