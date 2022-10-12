from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, past
from flask import flash 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Current: 
    db = "work_tracker"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.location = data['location']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.pay = data['pay']
        self.address = data['address']
        self.full_name = data['full_name']
        self.phone = data['phone']
        self.email_address = data['email_address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None



    @classmethod 
    def save_current(cls, data):
        query = "INSERT INTO current (name, description, location, start_date, end_date, pay, address, full_name, phone, email_address, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(location)s, %(start_date)s, %(end_date)s, %(pay)s, %(address)s, %(full_name)s, %(phone)s, %(email_address)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def get_current_job(cls, data):
        query = "SELECT * FROM current WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod 
    def update_current(cls, data):
        query = "UPDATE current SET name=%(name)s, description=%(description)s, location=%(location)s, start_date=%(start_date)s, end_date=%(end_date)s, pay=%(pay)s, full_name=%(full_name)s, phone=%(phone)s, email_address=%(email_address)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_current(cls, data):
        query = "DELETE FROM current WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def complete_job(cls, data):
        query = "INSERT INTO past SELECT * FROM current WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_jobs(cls):
        query = "SELECT * FROM current;"
        results = connectToMySQL(cls.db).query_db(query)
        current = []
        for current_data in results:
            current.append( current_data )
        return current

    @classmethod 
    def get_current_jobs(cls):
        query = "SELECT * FROM current JOIN users ON current.user_id = users.id;"
        result =  connectToMySQL(cls.db).query_db(query)
        if len(result) == 0:
            return []
        else:
            currents = []
            for row in result:
                current = cls(row)
                user_info = {
                    "id": row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
                }
                author = user.User(user_info)
                current.user_id = author
                currents.append(current)
            return currents

    @staticmethod
    def validate_current(current):
        is_valid = True
        if len(current['name']) < 3:
            flash("Job name must be at least 3 characters!", "current")
            is_valid = False
        if len(current['description']) < 3:
            flash("Job description must be at least 3 characters!", "current")
            is_valid = False
        if current['start_date'] == "":
            flash("Start date is required!", "current")
            is_valid = False
        if current['end_date'] == "":
            flash("End date is required!", "current")
            is_valid = False
        if current['pay'] == "":
            flash("Pay is required!", "current")
            is_valid = False
        return is_valid 