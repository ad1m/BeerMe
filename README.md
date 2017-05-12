#BeerMe: 
BeerMe is a machine learning application, hosted at crafte.herokuapp.com, to recommend craft beers based on a user selected beer. 

##Directory Structure
* features.p - a pickle file of a dataframe that holds the feature vectors for our data where the beer name is the index
* namez.p - a pickle file of a dataframe that is an alteration of features.p, where the index is a range(0,n) and the beer name is a column 
* reverse\_dict\_brewery.p - a pickle file of a dictionary for reverse look up of integer to brewery name 
* reverse\_dict\_name - a pickle file of a dictionary for reverse look up of integer to beer name 
* reverse\_dict\_style - a pickle file of a dictionary for reverse lookup of integer to beer style. 
* tree.p - a pickle file of a KDTree 
* notebooks - contains scratch work Jupyter notebooks
	* BeerMe.ipynb - a python 3.x jupyter notebook used as scratch work for development of the backend python 2.x code. 
* static - styling for flask app
	* css - contains the css for the site 
		* style.css - main stylesheet for index.html 
	* js - contains the js for the site
		* index.js - main js for index.html
* templates - contains the html and datasets used for the site 
	* data.csv - all beer data 
	* data2.txt - formated all beer data
	* dataUse.txt - formatted selected beer data for user to query (reduced so DOM does not crash in dropdown)
	* index.html - splash page for site 
	* index2.html - user beer selection page for site 
	* recommendations.html - user recommended beers result page 
* requirements.txt - python libraries used in backend files, also required for hosting on Heroku 
* app.py - powers the flask application, handles routing and display between pages and passes data between them 
* model.py - python file for the KDTree model 
* utility.py - python file for loading data and processing it 
* Procfile - required for hosting through Heroku

##Hosted Application
The application can be found at crafte.herokuapp.com. Please note that this is hosted on a free account so Heroku puts apps to sleep. Thus, the application might take a few seconds to initially boot up if it has been asleep. 

##Runing Application
To run the application make sure port 5000 is available on your localhost. Then run app.py and navigate to http://localhost:5000 in a web browser of your choice.


##Technology Details
###Backend: 
The backend of this application was written in python 2.x. 

###Frontend: 
The frontend was written with standard HTML, CSS, and JavaScript. 

###Microframework: 
Flask and Jinja2 were used to bridge the backend to the fronend and pass data for view on the frontend. 

###Hosting: 
Heroku was used to host the flask application at crafte.herokuapp.com. 
