from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, current
from flask import flash 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Past: 
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
    def save_past(cls, data):
        query = "INSERT INTO past (name, description, location, start_date, end_date, pay, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(location)s, %(start_date)s, %(end_date)s, %(pay)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def get_past_job(cls, data):
        query = "SELECT * FROM past WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod 
    def update_past(cls, data):
        query = "UPDATE past SET name=%(name)s, description=%(description)s, location=%(location)s, start_date=%(start_date)s, end_date=%(end_date)s, pay=%(pay)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def delete_past(cls, data):
        query = "DELETE FROM past WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_past(past):
        is_valid = True
        if len(past['name']) < 3:
            flash("Job name must be at least 3 characters!", "past")
            is_valid = False
        if len(past['description']) < 3:
            flash("Job description must be at least 3 characters!", "past")
            is_valid = False
        if len(past['location']) < 3:
            flash("Job location must be at least 3 characters!", "past")
            is_valid = False
        if len(past['start_date']) < 1:
            flash("Start date is required!", "past")
            is_valid = False
        if len(past['end_date']) < 1:
            flash("End date is required!", "past")
            is_valid = False
        if len(past['pay']) < 0:
            flash("Pay is required!", "past")
            is_valid = False
        return is_valid 