from flask_app import app 
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import past, user, current
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route("/past-job")
def old_job():
    if 'user_id' not in session:
        return redirect("/logout")
    data = {
        'id' : session['user_id']
    }
    return render_template("old.html", user=user.User.get_by_id(data))

@app.route("/past", methods=['POST'])
def past_job():
    if 'user_id' not in session:
        return redirect('/logout')

    if not past.Past.validate_past(request.form):
        return redirect('/past-job')

    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "location": request.form['location'],
        "start_date": request.form['start_date'],
        "end_date": request.form['end_date'],
        "pay" : request.form['pay'],
        "user_id" : session['user_id']
    }
    
    past.Past.save_past(data)
    return redirect("/dashboard")


@app.route("/past/<int:id>")
def past_position(id):
    if 'user_id' not in session:
        return redirect("/logout")
    user_data = {
        'id' : session['user_id']
    }
    data = {
        'id' : id
    }
    return render_template("olddetails.html", user=user.User.get_by_id(user_data), past=past.Past.get_past_job(data))

@app.route("/past/edit/<int:id>")
def update_old(id):
    if 'user_id' not in session:
        return redirect("/logout")
    user_data = {
        'id' : session['user_id']
    }
    data = {
        'id' : id
    }
    return render_template("old_edit.html", user=user.User.get_by_id(user_data), past=past.Past.get_past_job(data))

@app.route("/update_old", methods=['POST'])
def updating_past():
    if 'user_id' not in session:
        return redirect('/logout')

    if not past.Past.validate_past(request.form):
        past_data = {
            "past_id" : request.form['id']
        }
        return redirect(url_for("update_old", id=past_data['past_id']))

    data = {
        "id" : request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "location": request.form['location'],
        "start_date": request.form['start_date'],
        "end_date": request.form['end_date'],
        "pay" : request.form['pay']
    }
    
    past.Past.update_past(data)
    return redirect("/dashboard")

@app.route('/delete/past/<int:id>')
def destroy_past(id):
    data = {
        "id" : id
    }
    past.Past.delete_past(data)
    return redirect('/dashboard')