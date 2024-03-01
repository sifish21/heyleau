# Copyright 2022 Jacques Berger
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


import sqlite3

BRACK_CAN = [15000, 38000, 1000, 51000, 55000, 50000, 200000]
BRACK_QC = [17000, 1000, 31000, 1000, 50000, 15000, 280000]
POURC_CAN = [0, 0.1253, 0.1547, 0.1712, 0.2171, 0.2456, 0.2756]
POURC_QC = [0, 0.114, 0.14, 0.176, 0.19, 0.24, 0.2575]
IMPOT_MAX = 0.5331

def _build_rendezvous(result_set_item):
    rendezvous = {}
    rendezvous["id"] = result_set_item[0]
    rendezvous["user_id"] = result_set_item[1]
    rendezvous["nom"] = result_set_item[2]
    rendezvous["num_tattoo"] = result_set_item[3]
    rendezvous["jour"] = result_set_item[4]
    rendezvous["mois"] = result_set_item[5]
    rendezvous["annee"] = result_set_item[6]
    rendezvous["depot"] = result_set_item[7]
    rendezvous["prix_total"] = result_set_item[8]
    rendezvous["type_paiement"] = result_set_item[9]
    rendezvous["tip"] = result_set_item[10]
    rendezvous["pistache"] = result_set_item[11]
    return rendezvous

def _build_earnings_mois(months):
    mois = {}
    mois["janvier"] = months[0]
    mois["fevrier"] = months[1]
    mois["mars"] = months[2]
    mois["avril"] = months[3]
    mois["mai"] = months[4]
    mois["juin"] = months[5]
    mois["juillet"] = months[6]
    mois["aout"] = months[7]
    mois["septembre"] = months[8]
    mois["octobre"] = months[9]
    mois["novembre"] = months[10]
    mois["decembre"] = months[11]
    return mois

def _build_infos_page(items):
    infos = {}
    infos["prix_total"] = items[0]
    infos["taxes"] = items[1]
    infos["qc"] = items[2]
    infos["can"] = items[3]
    return infos


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/rendezvous.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_all_rendezvous(self):
        cursor = self.get_connection().cursor()
        query = ("select id, user_id, nom, num_tattoo, jour, mois, annee, "
                 "depot, prix_total, type_paiement, tip, pistache from rendezvous")
        cursor.execute(query)
        all_data = cursor.fetchall()
        return [_build_rendezvous(item) for item in all_data]
    
    def get_monthly_earnings(self, annee, user_id):
        cursor = self.get_connection().cursor()
        months = []
        query = ("SELECT SUM(prix_total) AS total FROM rendezvous r JOIN users u ON u.user_id = r.user_id WHERE mois = ? AND r.user_id = ? AND annee = ?")
        for i in range(1, 13):
            cursor.execute(query, (i, user_id, annee))
            gains = cursor.fetchone()[0]
            if gains == None:
                months.append(0)
            else:
                months.append(gains)
        return _build_earnings_mois(months)
    
    def get_infos_page(self, current_year, user_id):
        infos = []
        infos.append( format(self.total_annuel("prix_total", current_year, user_id), '.2f'))
        infos.append( format(self.total_taxes_annee(current_year, user_id), '.2f'))
        infos.append( format(self.total_qc_annee(current_year, user_id), '.2f'))
        infos.append( format(self.total_can_annee(current_year, user_id), '.2f'))
        return _build_infos_page(infos)
        
    def get_rendezvous(self, rendezvous_id):
        cursor = self.get_connection().cursor()
        query = ("select id, user_id, nom, num_tattoo, jour, mois, annee, depot, "
                 "prix_total, type_paiement, tip, pistache from rendezvous where id = ?")
        cursor.execute(query, (rendezvous_id,))
        item = cursor.fetchone()
        if item is None:
            return item
        else:
            return _build_rendezvous(item)

    def add_rendezvous(self, user_id, nom, num_tattoo, jour, mois, annee, depot,
                   prix_total, type_paiement, tip, pistache):
        connection = self.get_connection()
        query = ("insert into rendezvous(user_id, nom, num_tattoo, jour, mois, annee, depot, "
                 "prix_total, type_paiement, tip, pistache) "
                 "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        connection.execute(query, (user_id, nom, num_tattoo, jour, mois, annee, depot,
                                prix_total, type_paiement, tip, pistache))
        cursor = connection.cursor()
        cursor.execute("select last_insert_rowid()")
        lastId = cursor.fetchone()[0]
        connection.commit()
        return lastId
    
    def add_user(self, username, password):
        connection = self.get_connection()
        query = ("insert into users(username, password) values(?, ?)")
        connection.execute(query, (username, password))
        cursor = connection.cursor()
        cursor.execute("select last_insert_rowid()")
        lastID = cursor.fetchone()[0]
        connection.commit()
        return lastID
    
    def verify_user(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = ("select exists (select 1 from users where username = ?)")
        cursor.execute(query, (username,))
        result = cursor.fetchone()[0]
        cursor.close()
        username_exists = bool(result)
        return username_exists
    
    def verify_password(self, username, password):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = ("select exists (select 1 from users where username = ? and password = ?)")
        cursor.execute(query, (username, password))
        result = cursor.fetchone()[0]
        cursor.close()
        valid_password = bool(result)
        return valid_password
    
    def get_user_id(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = ("SELECT user_id FROM users WHERE username = ?")
        cursor.execute(query, (username,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    
    def total_annuel(self, column_name, annee, user_id):
        if column_name in ["prix_total", "tip", "taxes_dues", "depot"]:
            connection = self.get_connection()
            cursor = connection.cursor()
            query = (f"SELECT SUM( {column_name} ) AS total FROM rendezvous r JOIN users u "
                        "ON r.user_id = u.user_id WHERE annee = ? AND r.user_id = ?")
            cursor.execute(query, (annee, user_id))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        else:
            return None
    
    def total_annuel_pistache(self, column_name, annee, user_id, pistache):
        if column_name in ["prix_total", "tip", "taxes_dues", "depot"]:
            connection = self.get_connection()
            cursor = connection.cursor()
            query = (f"SELECT SUM( {column_name} ) AS total FROM rendezvous r JOIN users u "
                        "ON r.user_id = u.user_id WHERE annee = ? AND r.user_id = ? AND pistache = ?")
            cursor.execute(query, (annee, user_id, pistache))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        else:
            return None

    def total_mensuel(self, column_name, mois, annee, user_id):
        if column_name in ["prix_total", "tip", "taxes_dues", "depot"]:
            connection = self.get_connection()
            cursor = connection.cursor()
            query = (f"SELECT SUM( {column_name} ) AS total FROM rendezvous r JOIN users u "
                        "ON r.user_id = u.user_id WHERE mois = ? AND annee = ? AND r.user_id = ?")
            cursor.execute(query, (mois, annee, user_id))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        else:
            return None
        
    def total_taxes_annee(self, annee, user_id):
        total_recu = self.total_annuel_pistache("prix_total", annee, user_id, 0)
        tips_recu = self.total_annuel_pistache("tip", annee, user_id, 0)
        return (total_recu - tips_recu) * 0.11
    
    def total_qc_annee(self, annee, user_id):
        total_taxable = self.total_annuel_pistache("prix_total", annee, user_id, 0)
        impots_qc = 0
        i = 0
        if total_taxable > 250000:
            impots_qc = (total_taxable - 250000) * IMPOT_MAX
            total_taxable = 250000

        while total_taxable > 0:
            if total_taxable < BRACK_QC[i]:
                impots_qc += (total_taxable * POURC_QC[i])
                total_taxable = 0
            else:
                impots_qc += (BRACK_QC[i] * POURC_QC[i])
                total_taxable -= BRACK_QC[i]
            i += 1
        return impots_qc

    def total_can_annee(self, annee, user_id):
        total_taxable = self.total_annuel_pistache("prix_total", annee, user_id, 0)
        impots_can = 0
        i = 0
        if total_taxable > 250000:
            impots_can = (total_taxable - 250000) * IMPOT_MAX
            total_taxable = 250000
            
        while total_taxable > 0:
            if total_taxable < BRACK_CAN[i]:
                impots_can += (total_taxable * POURC_CAN[i])
                total_taxable = 0
            else:
                impots_can += (BRACK_CAN[i] * POURC_CAN[i])
                total_taxable -= BRACK_CAN[i]

        return impots_can
        
    
