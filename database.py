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
    rendezvous["taxes_dues"] = result_set_item[9]
    rendezvous["tip"] = result_set_item[10]
    return rendezvous


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
                 "depot, prix_total, taxes_dues, tip from rendezvous")
        cursor.execute(query)
        all_data = cursor.fetchall()
        return [_build_rendezvous(item) for item in all_data]

    def get_rendezvous(self, rendezvous_id):
        cursor = self.get_connection().cursor()
        query = ("select id, user_id, nom, num_tattoo, jour, mois, annee, depot, "
                 "prix_total, taxes_dues, tip from rendezvous where id = ?")
        cursor.execute(query, (rendezvous_id,))
        item = cursor.fetchone()
        if item is None:
            return item
        else:
            return _build_rendezvous(item)

    def add_rendezvous(self, nom, num_tattoo, mois, jour, description, depot,
                   prix_total, taxes_dues, tip):
        connection = self.get_connection()
        query = ("insert into rendezvous(user_id, nom, num_tattoo, mois, jour, description, "
                 "depot, prix_total, taxes_dues, tip) "
                 "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        connection.execute(query, (nom, num_tattoo, mois, jour, description,
                                   depot, prix_total, taxes_dues, tip))
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
    
