from flask import Blueprint, render_template, redirect, url_for, request, flash
from website import db
from website.domain.models import User,Pacient,Terapeut
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

class ControllerAuth:
    auth = Blueprint("auth", __name__)

    @staticmethod
    @auth.route("http://ec2-16-16-138-138.eu-north-1.compute.amazonaws.com/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in!", category='success')
                    login_user(user, remember=True)
                    if user.role == 'terapeut':
                        return redirect(url_for('terapeutView.home_Terapeut'))
                    else:
                        return redirect(url_for('pacientView.home_Pacient'))
                else:
                    flash('Password is incorrect.', category='error')
            else:
                flash('Email does not exist.', category='error')


        return render_template("login.html", user=current_user)

    @staticmethod
    @auth.route("http://ec2-16-16-138-138.eu-north-1.compute.amazonaws.com/sign-up", methods=['GET', 'POST'])
    def sign_up():
        teraps = Terapeut.query.all()
        if request.method == 'POST':
            email = request.form.get("email")
            username = request.form.get("username")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            role = request.form.get("user-type")
            terapeutAsignat = request.form.get("terapeut-select",type=int)
            function = request.form.get("function")
            license = request.form.get("license")
            startYear = request.form.get("startYear",type=int)


            email_exists = User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first()
            if teraps is None:
                teraps = []

            if email_exists:
                flash('Email is already in use.', category='error')
            elif username_exists:
                flash('Username is already in use.', category='error')
            elif password1 != password2:
                flash('Password don\'t match!', category='error')
            elif len(username) < 2:
                flash('Username is too short.', category='error')
            elif len(password1) < 6:
                flash('Password is too short.', category='error')
            elif len(email) < 4:
                flash("Email is invalid.", category='error')
            elif len(first_name) < 1:
                flash('First name not introduced', category='error')
            elif len(last_name) < 1:
                flash('Last name not introduced.', category='error')
            else:
                new_user = User(email=email, username=username, password=generate_password_hash(
                    password1, method='sha256'), role=role)
                db.session.add(new_user)
                db.session.commit()
                id = User.query.filter_by(email=email).first().id
                if role == 'terapeut':
                    new_terapeut= Terapeut(id=id,first_name=first_name,last_name=last_name,license=license,function=function,activity_start_year=startYear)
                    db.session.add(new_terapeut)
                else:
                    new_pacient= Pacient(id=id,first_name=first_name,last_name=last_name,terapeut_asignat=terapeutAsignat)
                    db.session.add(new_pacient)
                db.session.commit()

                login_user(new_user, remember=True)
                flash('User created!')
                if new_user.role == 'terapeut':
                    return redirect(url_for('terapeutView.home_Terapeut'))
                else:
                    return redirect(url_for('pacientView.home_Pacient'))

        return render_template("signup.html", user=current_user, terapeuts= teraps)

    @staticmethod
    @auth.route("http://ec2-16-16-138-138.eu-north-1.compute.amazonaws.com/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('pacientView.home'))
