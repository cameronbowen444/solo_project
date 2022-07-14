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
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None
        

    @classmethod 
    def save_current(cls, data):
        query = "INSERT INTO current (name, description, location, start_date, end_date, pay, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(location)s, %(start_date)s, %(end_date)s, %(pay)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def get_current_job(cls, data):
        query = "SELECT * FROM current WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod 
    def update_current(cls, data):
        query = "UPDATE current SET name=%(name)s, description=%(description)s, location=%(location)s, start_date=%(start_date)s, end_date=%(end_date)s, pay=%(pay)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_current(cls, data):
        query = "DELETE FROM current WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def complete_job(cls, data):
        query = "INSERT INTO past SELECT * FROM current WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_current(current):
        is_valid = True
        if len(current['name']) < 3:
            flash("Job name must be at least 3 characters!", "current")
            is_valid = False
        if len(current['description']) < 3:
            flash("Job description must be at least 3 characters!", "current")
            is_valid = False
        if len(current['location']) < 3:
            flash("Job location must be at least 3 characters!", "current")
            is_valid = False
        if len(current['start_date']) < 1:
            flash("Start date is required!", "current")
            is_valid = False
        if len(current['end_date']) < 1:
            flash("End date is required!", "current")
            is_valid = False
        if len(current['pay']) < 0:
            flash("Pay is required!", "current")
            is_valid = False
        return is_valid 