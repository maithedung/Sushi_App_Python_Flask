from flask import Flask, render_template, flash, redirect, url_for, request, session
from config import Config
from forms import LoginForm, RegisterForm, CreateRecipeForm, EditRecipeForm, ConfirmDelete
from flask_login import login_manager, login_required, logout_user
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId
import bcrypt
import math
import re
import env
import os
import sys

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
app.config.from_object(Config)

mongo = PyMongo(app)



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'test'}
    print('hey', list( mongo.db.recipes.find()), file=sys.stdout, flush=True)
    #r = list(i['title'] for i in mongo.db.recipes.find())
    r = list(mongo.db.recipes.find())
    return render_template('index.html', title="Home", user=user, r=r)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        users = mongo.db.users
        login_user = users.find_one({'name': request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index', title="Sign In", form=form))
            flash('Invalid username/password combination')
    return render_template("login.html", title="Sign In", form=form)


@app.route('/logout')
def logout():
    """Clear session and redirect to the homepage"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hash_pass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'],
                          'password': hash_pass,
                          'email': request.form['email']})
            session['username'] = request.form['username']
            flash('Thanks for registering')
            return redirect(url_for('index'))
        flash('Sorry, that username is already taken - use another')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    """Creates a recipe and enters into recipe collection"""
    form = CreateRecipeForm(request.form)
    if form.validate_on_submit():
        # set the collection
        recipes_db = mongo.db.recipes
        # insert a new recipe
        recipes_db.insert_one({
            'title': request.form['title'],
            'user': session['username'],
            'short_description': request.form['short_description'],
            'ingredients': request.form['ingredients'],
            'method': request.form['method'],
            'tags': request.form['tags'],
            'image': request.form['image'],
            'views': 0
        })
        return redirect(url_for('index', title='New Recipe Added'))
    return render_template('create_recipe.html', title='create a recipe', form=form)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """Allows a logged in user to edit their own recipes"""
    recipe_db = mongo.db.recipes.find_one_or_404({'_id': ObjectId(recipe_id)})
    if request.method == 'GET':
        form = EditRecipeForm(data=recipe_db)
        return render_template('edit_recipe.html', recipe=recipe_db, form=form)
    form = EditRecipeForm(request.form)
    if form.validate_on_submit():
        recipes_db = mongo.db.recipes
        recipes_db.update_one({
            '_id': ObjectId(recipe_id),
        }, {
            '$set': {
                'title': request.form['title'],
                'user': session['username'],
                'short_description': request.form['short_description'],
                'ingredients': request.form['ingredients'],
                'method': request.form['method'],
                'tags': request.form['tags'],
                'image': request.form['image'],
            }
        })
        return redirect(url_for('index', title='New Recipe Added'))
    return render_template('edit_recipe.html', recipe=recipe_db, form=form)


@app.route('/search')
def search():
    """Logic for the search criteria"""
    orig_query = request.args['query']
    # using regular expression setting option for any case
    query = {'$regex': re.compile(
        '.*{}.*'.format(orig_query)), '$options': 'i'}
    # find instances of the entered word in title, tags or ingredients
    results = mongo.db.recipes.find({
        '$or': [
            {'title': query},
            {'tags': query},
            {'ingredients': query},
            {'short_description': query},
            {'image': query},
            {'views': query},
            {'like': query},
        ]
    })
    return render_template('search.html', query=orig_query, results=results)


@app.route('/recipes')
def recipes():
    """Logic for recipe list and pagination"""
    # number of recipes per page
    per_page = 1
    page = int(request.args.get('page', 1))


    # count total number of recipes
    total = mongo.db.recipes.count_documents({})
    # logic for what recipes to return
    all_recipes = mongo.db.recipes.find().skip((page - 1)*per_page).limit(per_page)
    pages = range(1, int(math.ceil(total / per_page)) + 1)
    r = list(mongo.db.recipes.find())
    return render_template('recipes.html', recipes=all_recipes, page=page, pages=pages, total=total, r=r)


@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    """Shows full recipe and increments view"""
    mongo.db.recipes.find_one_and_update(
        {'_id': ObjectId(recipe_id)},
        {'$inc': {'views': 1}}
    )
    recipe_db = mongo.db.recipes.find_one_or_404({'_id': ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe_db)


@app.route('/delete_recipe/<recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    """Allows logged in user to delete one of their recipes with added confirmation"""
    recipe_db = mongo.db.recipes.find_one_or_404({'_id': ObjectId(recipe_id)})
    if request.method == 'GET':
        form = ConfirmDelete(data=recipe_db)
        return render_template('delete_recipe.html', title="Delete Recipe", form=form)
    form = ConfirmDelete(request.form)
    if form.validate_on_submit():
        recipes_db = mongo.db.recipes
        recipes_db.delete_one({
            '_id': ObjectId(recipe_id),
        })
        return redirect(url_for('index', title='Recipe Updated'))
    return render_template('delete_recipe.html', title="delete recipe", recipe=recipe_db, form=form)


@app.errorhandler(404)
def handle_404(exception):
    return render_template('404.html', exception=exception)


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.config['DEBUG'] = True
    app.run(host='127.0.0.1', debug=True)
