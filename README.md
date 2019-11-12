# My Sushi Recipes

This is a full stack CRUD application which allows a user to register, login and logout to create, read, edit, update and delete recipes.
This web application has been created using Python 3.7 for the back-end with Flask which is a Python-based microframework. MongoDB Atlas has been used for the database. Bootstrap has been implemented for the front-end.

The purpose of this project is for educational purposes and serves as the Milestone 4 Project in the Data Centric Development module of the Full Stack Software Development Program at the Code Institute.

The live project can be viewed [link](https://www.google.com) here.

## CRUD Functionality

### CREATE
Users and anyone can view a list of recipes a user or users has already created in the database. These recipe lists are displayed on the index page and also the search page (which is called recipes.html) whether a user or non-user ("viewer") is logged in or not.

### READ 
Following on from the above point, therefore all viewers to the site can effectively read the recipes from the database collection respectively. Furthermore, if a user/viewer presses the "more info" button they can view a recipe as a single page with all the details. The idea was provided by the Task Manager project at CI.

The search feature within the `recipes.html` page as a search bar and which is also accessed as a `link` on the `menu bar` on every page,  also allows viewers to search for a term as a filter via a keyword such as a tag to read from the collection and the results of which will be displayed after the search button is depressed.

### UPDATE 

This is only available to registered/logged-in users a hashed password security feature using *bycrypt* and *weurkzug* discussed in Security. A user has to fill in all the fields to be able to add a new recipe.

I used the code of *update one* in the `app.py` as part of the edit_recipe route as *recipe_db = mongo.db.recipes.find_one_or_404({'_id': ObjectId(recipe_id)})* which is also translated via code in `{{ form.submit() }}`,  on the `edit_recipe.html` originating from `forms.py`. There is no update link on the menu bar, the page appears as an option to view from the `Add Recipe` page. Checking was done by simply logging into MongoDB itself to check the recipe list had been updated, then a browser refresh on the front-end.

### DELETE 

This is accessed from the `Add Recipe` page as a button option, similar functionality to the `update` button. If a user presses the delete button there is a flash message warning beforehand. The code is handled with `forms.py` Similar logic to that described for *update one*, here it is `recipes_db.delete_one({...etc` in`app.py`. 

## Technologies Used
* [Python 3.7](https://www.python.org/download/releases/3.0/)
* [Flask 1.0.2](http://flask.pocoo.org/)
* [HTML5](https://en.wikipedia.org/wiki/HTML5)
* [CCS3](https://www.w3.org/Style/CSS/)
* [JavaScript](https://www.javascript.com/)
* [jQuery](https://jquery.com/) Menu bar dropdown
* [Jinja2](https://palljtsprojects.com/p/jinja/) Jinja2 templating engine for Python used to keep the same features as a template so it is less loading for the browser
* [MongoDB](https://www.mongodb.com/)

## Testing
#### Responsivness
The UX fonts and card feature, plus the navbar and hamurger are all scalable, responsive and easy to navigate throughout the site.
The site follows responsive design and works for desktop viewing on browsers: google chrome, firefox and explorer as well as mobiles having checked the rending on the iPhone: from 5 to X, Samsung Galaxy: all versions, iPad: all versions, Google: Pixel 2 and 3.


