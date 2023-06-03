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
    states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
        'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
        'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
        'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
        'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    return render_template("old.html", user=user.User.get_by_id(data), states=states)

@app.route("/past", methods=['POST'])
def past_job():
    if 'user_id' not in session:
        return redirect('/logout')

    if not past.Past.validate_past(request.form):
        return redirect('/past-job')
    location = request.form['street'] + " " + request.form['city'] + " " + request.form['state'] + " " + request.form['zip']
    address = request.form['street2'] + " " + request.form['city2'] + " " + request.form['state2'] + " " + request.form['zip2']
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "location": location,
        "start_date": request.form['start_date'],
        "end_date": request.form['end_date'],
        "pay" : request.form['pay'],
        "address": address,
        "full_name": request.form['full_name'],
        "phone": request.form['phone'],
        "email_address": request.form['email_address'],
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
        "id": request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "location": request.form['location'],
        "start_date": request.form['start_date'],
        "end_date": request.form['end_date'],
        "pay" : request.form['pay'],
        "address": request.form['address'],
        "full_name": request.form['full_name'],
        "phone": request.form['phone'],
        "email_address": request.form['email_address'],
        "user_id" : session['user_id']
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