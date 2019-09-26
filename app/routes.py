from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Fileo'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Japan!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Cars movie was excellent!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)