from app import *
from models import *

"""TASKS
1. Create Organization profile files 
2. How to dynamically create buttons
3. create signout button
"""

@app.route("/patient_profile", methods=['GET', 'POST'])
def patient_profile():
    if session.get("USERNAME") is None:
        print("No username found in session")
        return redirect(url_for("nav_page"))
    else:
        if request.method == 'POST':
            provider = request.form.get('Your Providers')
            session['org_speciality'] = provider
            return redirect(url_for("patient_doctor_home"))
        else:
            username = session.get("USERNAME")
            user = Patient.query.filter_by(username=username).first()
            print(user.username)
            return render_template("patient_profile.html", user=user)


@app.route("/patient_profile/yourProvider")
def patient_doctor_home():
     provider = session.get("org_speciality")
     # query records info, org info, doctor info and speciality info


@app.route("/org_profile", methods=['GET', 'POST'])
def org_profile():
    if session.get("USERNAME") is None:
        print("No username found in session")
        return redirect(url_for("nav_page"))
    else:
        if session.get('role') == 'Organization':
            username = session.get("USERNAME")
            user = Organization.query.filter_by(username=username).first()
            print(user.username)
            return render_template("doctorPages.html", user=user)



#@app.route("/org_profile/scheduling")
#def org_scheduling():
