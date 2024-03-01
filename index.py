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
from flask import session
from .database import Database
import re
import datetime

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = 'caddie.poil'

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
    
def val_nom(nom):
    regex = r'^[- a-zA-Z]+$'
    return len(nom) >= 2 and re.match(regex, nom)

def val_nombre(nombre):
    try:
        number = int(nombre)
        return number > 0
    except ValueError:
        return False
    
def val_depot(depot):
    try:
        number = int(depot)
        return number >= 0
    except ValueError:
        return False
    
def val_montant(montant):
    try:
        number = float(montant)
        return number >= 0
    except ValueError:
        return False
    
def val_type_paiement(type):
    return type in ["interac", "cash", "visa", "mastercard"]



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def index():
    username = request.args.get('username')

    return render_template('index.html', username=username)

@app.route('/page', methods=["POST"])
def page():
    username = request.form["floatingInput"]
    password = request.form["floatingPassword"]
    if(val_username(username) and val_password(username, password)):
        db = get_db()
        current_year = datetime.datetime.now().year
        user_id = db.get_user_id(username)
        infos = db.get_infos_page(current_year, user_id)
        mois = db.get_monthly_earnings(current_year, user_id)
        session['user_id'] = user_id
        return render_template('page.html', infos=infos, mois=mois)
    else:
        return redirect(url_for('index', username=username))
    
@app.route('/page')
def page_2():
    user_id = session.get('user_id')
    db = get_db()
    current_year = datetime.datetime.now().year
    infos = db.get_infos_page(current_year, user_id)
    mois = db.get_monthly_earnings(current_year, user_id)
    return render_template('page.html', infos=infos, mois=mois)

@app.route('/page/nouveau', methods=["POST"])
def nouveau():
    if val_nom(request.form["nom"]) and \
    val_nombre(request.form["nombre"]) and \
    val_depot(request.form["depot"]) and \
    val_montant(request.form["fin_payer"]) and \
    val_montant(request.form["total"]) and \
    val_type_paiement(request.form["type_paiement"]):
        
        tip = 0
        total_recu = float(request.form["depot"]) + float(request.form["total"])
        pistache = 0
        if 'checkbox-taxes' in request.form:
            tip = float(request.form["total"]) - float(request.form["fin_payer"])
            pistache = 1
        else:
            tip = float(request.form["total"]) - (float(request.form["fin_payer"]) * 1.14975)
        db = get_db()
        db.add_rendezvous(session.get('user_id'),
                          request.form["nom"],
                          request.form["nombre"],
                          datetime.datetime.now().day,
                          datetime.datetime.now().month,
                          datetime.datetime.now().year,
                          request.form["depot"],
                          total_recu,
                          request.form["type_paiement"],
                          tip, 
                          pistache)
        # il a cliqué sur autre
        if 'checkbox' in request.form:
            return redirect(url_for('nouveau_2'))
        # il a cliqué sur enregistrer
        else:
            return redirect(url_for('page_2'))

    return render_template('error.html')

@app.route('/page/nouveau')
def nouveau_2():
    return render_template('nouveau.html')

#@app.route('/')
def tets():
    return render_template('nouveau.html')
