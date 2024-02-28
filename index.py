# Copyright 2023 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import g
from flask import redirect,url_for,request
from .database import Database
import re
import datetime

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

def val_username(username):
    if(len(username) > 0):
        db = get_db()
        valid = db.verify_user(username)
        return valid
    else:
        return False

def val_password(username, password):
    if(len(password) > 0):
        db = get_db()
        valid = db.verify_password(username, password)
        return valid
    else:
        return False

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/page', methods=["POST"])
def page():
    username = request.form["floatingInput"]
    password = request.form["floatingPassword"]
    if(val_username(username) and val_password(username, password)):
        current_year = datetime.datetime.now().year
        db = get_db()
        user_id = db.get_user_id(username)
        prix_total = db.total_annuel("prix_total", current_year, user_id)
        tip = db.total_annuel("tip", current_year, user_id)
        taxes = db.total_annuel("taxes_dues", current_year, user_id)
        depot = db.total_annuel("depot", current_year, user_id)
        mois = db.get_monthly_earnings()
        return render_template('page.html', prix_total=prix_total, tip=tip, taxes=taxes, depot=depot, mois=mois)
    else:
        return render_template('index.html', username=username)
    
#@app.route('/')
def developpement():
    db = get_db()
    connection = db.get_connection()
    prix = db.total_annuel("prix_total", 2024, 1, connection)
    tip = db.total_annuel("tip", 2024, 1, connection)
    taxes = db.total_annuel("taxes_dues", 2024, 1, connection)
    connection.close()
    db.disconnect()
    return render_template('page.html', prix=prix, tip=tip, taxes=taxes )

#@app.route('/')
def tets():
    return render_template('page.html')
