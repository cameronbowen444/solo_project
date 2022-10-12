from flask_app import app 
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import current, user, past
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route("/new-job")
def new_job():
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
    return render_template("new.html", user=user.User.get_by_id(data), states=states)


@app.route("/current", methods=['POST'])
def current_job():
    if 'user_id' not in session:
        return redirect('/logout')

    if not current.Current.validate_current(request.form):
        return redirect("/new-job")
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
    current.Current.save_current(data)
    return redirect("/dashboard")


@app.route("/job/<int:id>")
def upcomming(id):
    if 'user_id' not in session:
        return redirect("/logout")
    user_data = {
        'id' : session['user_id']
    }
    data = {
        'id' : id
    }
    return render_template("newdetails.html", user=user.User.get_by_id(user_data), current=current.Current.get_current_job(data))


@app.route("/job/edit/<int:id>")
def update_new(id):
    if 'user_id' not in session:
        return redirect("/logout")
    user_data = {
        'id' : session['user_id']
    }
    data = {
        'id' : id
    }
    states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
        'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
        'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
        'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
        'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    return render_template("new_edit.html", user=user.User.get_by_id(user_data), current=current.Current.get_current_job(data), states=states)

@app.route("/update_new", methods=['POST'])
def updating_job():
    if 'user_id' not in session:
        return redirect('/logout')

    if not current.Current.validate_current(request.form):
        current_data = {
            "current_id" : request.form['id']
        }
        return redirect(url_for("update_new", id=current_data['current_id']))
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
    current.Current.update_current(data)
    return redirect("/dashboard")

@app.route('/delete/current/<int:id>')
def destroy_current(id):
    data = {
        "id" : id
    }
    current.Current.delete_current(data)
    return redirect('/dashboard')



@app.route("/complete", methods=['POST'])
def complete_job():

    if 'user_id' not in session:
        return redirect('/logout')

    current.Current.complete_job(request.form)
    current_data = {
            "current_id" : request.form['id']
        }
    return redirect(url_for("destroy_current", id=current_data['current_id']))

