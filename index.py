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
import random
import re

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

def val_username(username):
    if(len(username) > 0):
        db = get_db()
        return db.verify_user(username)

    else:
        return False




@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def index():
    db = get_db()
    rdv_test = db.get_rendezvous(1)
    db.disconnect()

    return render_template('index.html', rdv_test=rdv_test)

@app.route('/page', methods=["POST"])
def page():
    username = request.form["floatingInput"]
    print(username)
    if(val_username(username)):
        return render_template('page.html')
    else:
        return render_template('index.html', username=username)
    
    
