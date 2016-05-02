import json
from km_to_list import Parser


#------------------------------------------------------------------
from flask import Flask, request, Request, render_template, url_for, redirect, flash, session, make_response, jsonify
from flask_restful import Api, Resource, fields, marshal_with
import ast
import os
from functools import wraps
import config
from form import LoginForm

app = Flask(__name__)
api = Api(app)
app.secret_key = os.urandom(24)


def parse_kml_from_file(filename):
    parser = Parser(filename)
    out_dict = parser.parse()
    #for k in out_dict:
    #    print (json.dumps(k, indent=4))
    #print (out_dict)
    return out_dict


def validate_user(username, password):
    return username =="john" and password == "doe123"


def authenticate(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        auth = request.authorization
        if not auth or not validate_user(auth.username, auth.password):
            resp = make_response("", 401)
            resp.header["WWW.Authenticate"] = 'Basic realm = "Login Required"'
            return resp
        return func(*args, **kwargs)
    return decorated


def login_required(f):
    """
    wrapper check for logged session
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Log in first')
            return redirect(url_for('login'))
    return wrap


@app.route('/')		
def home():
    logged = False
    if 'logged_in' in session:
        logged = True
    return render_template('home.html', logged=logged, GOOGLEMAPS_KEY=config.GOOGLEMAPS_KEY)	


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    form = LoginForm(request.form)
    if request.method == 'POST':
        if request.form['username'] != 'testUser01' or request.form['password'] != 'testUser01':
            error = 'Invalid username+password pair. Check your spelling or contact support.'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', form=form, error=error)
	

#logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# REST core
class KMLReader(Resource):
    def get (self, param):        
        try:
            output = parse_kml_from_file(param)
            #print (output)
            return output, 200
        except Exception as e:
            print ("No requested file found", e)
            return [], 200


api.add_resource(KMLReader, '/api/kml/<param>')

if __name__ == "__main__":
    app.run(debug=True)