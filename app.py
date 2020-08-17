from flask import render_template, url_for,request, redirect, flash, session
from models import *
from passlib.hash import sha256_crypt
from profiles import patient_profile, org_profile


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/nav_page")
def nav_page():
    return render_template('home.html')


@app.route("/Org-Register", methods=["GET", "POST"])
def Org_Register():
    if request.method == "POST":
        organization_name = request.form.get("Organization Name")
        organization_speciality = request.form.get("Organization Speciality")
        email = request.form.get('Email')
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        role = 'Organization'
        secure_password = sha256_crypt.encrypt(str(password))

        usernamedata = db.session.query(User).filter_by(email=email).first()
        if usernamedata is None:
            if password == confirm:
                organization = Organization(username=username, email=email, password=secure_password,
                                            organizationName=organization_name,
                                            organization_speciality=organization_speciality, role=role)
                db.session.add(organization)
                db.session.commit()
                flash("You are registered and can now login", "success")
                return redirect(url_for('ORG_login'))
            else:
                flash("password does not match", "danger")
                return render_template('Register.html')
        else:
            flash("user already existed, please login or contact admin", "danger")
            return redirect(url_for('ORG_login'))

    return render_template('Register.html')


@app.route("/Patient-Register", methods=["GET", "POST"])
def Patient_Register():
    if request.method == "POST":
        first_name = request.form.get("First Name")
        last_name = request.form.get("Last Name")
        email = request.form.get('Email')
        username = request.form.get("username")
        age = request.form.get("Age")
        race = request.form.get("Race")
        gender = request.form.get("Gender")
        weight = request.form.get("Weight")
        height = request.form.get("Height")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        role = 'Patient'
        secure_password = sha256_crypt.encrypt(str(password))

        usernamedata = db.session.query(User).filter_by(email=email).first()
        if usernamedata is None:
            # only unique emails allowed
            if password == confirm:
                patient = Patient(username=username, email=email, password=secure_password, first_name=first_name,
                                  last_name=last_name,
                                  age=age, weight=weight, height=height, gender=gender, race=race, role=role)
                db.session.add(patient)
                db.session.commit()
                flash("You are registered and can now login", "success")
                return redirect(url_for('patient_login'))
            else:
                flash("password does not match", "danger")
                return render_template('Patient_Register.html')
        else:
            flash("user already existed, please login or contact admin", "danger")
            return redirect(url_for('patient_login'))

    return render_template('Patient_Register.html')


@app.route("/PATIENT_LOGIN", methods=['GET', 'POST'])
def patient_login():
    if session["log"]:
        return redirect(url_for('patient_profile'))
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Patient.query.filter_by(username=username).first()

        if user is None:
            flash("No username", "danger")
            return render_template('Patient_login.html')
        else:
            if sha256_crypt.verify(password, user.password):
                session["log"] = True
                session['USERNAME'] = user.username
                session['role'] = user.role
                flash("You are now logged in!!", "success")
                return redirect(url_for('patient_profile'))  # REDIRECT TO PATIENT HOME
            else:
                flash("incorrect password", "danger")
                return render_template('Patient_login.html')

    return render_template('Patient_login.html')


@app.route("/ORG_LOGIN", methods=['GET', 'POST'])
def ORG_login():
    if session["log"]:
        return redirect(url_for('org_profile'))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Organization.query.filter_by(username=username).first()

        if user is None:
            flash("No username", "danger")
            return render_template('login.html')
        else:
            if sha256_crypt.verify(password, user.password):
                session["log"] = True
                session['role'] = user.role
                session['USERNAME'] = user.username
                flash("You are now logged in!!", "success")
                return redirect(url_for('org_profile'))  # REDIRECT TO ORGANIZATION HOME
            else:
                flash("incorrect password", "danger")
                return render_template('login.html')

    return render_template('login.html')


@app.route("/signout")
def sign_out():
    session.pop("USERNAME", None)
    session["log"] = False
    return redirect(url_for('nav_page'))
