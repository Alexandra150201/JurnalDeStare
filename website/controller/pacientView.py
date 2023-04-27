from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.domain.models import Post, Pacient
from website import db
from functools import wraps
from website.utils.detectDepressionModel import DepressionDetector
from datetime import date

class ControllerPacient:

    @staticmethod
    def role_required(role):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not current_user.role == role:
                    return "Unauthorized access", 403
                return func(*args, **kwargs)
            return wrapper
        return decorator


    views = Blueprint("pacientView", __name__)

    @staticmethod
    @views.route("/")
    @views.route("/home")
    @login_required
    def home():
        if current_user.role == 'terapeut':
            return redirect(url_for('terapeutView.home_Terapeut'))
        else:
            return redirect(url_for('pacientView.home_Pacient'))

    @staticmethod
    @views.route("/home/pacient")
    @login_required
    @role_required('pacient')
    def home_Pacient():
        posts = Post.query.filter_by(author=current_user.id).all()
        pacienti = Pacient.query.filter_by(terapeut_asignat=current_user.id)
        lista_finala = []
        for post in posts:
            if post.date_created.date() == date.today():
                lista_finala.append(post)
        if current_user.role == 'terapeut':
            return render_template("homeTerapeut.html", user=current_user, pacienti=pacienti)
        else:
            return render_template("homePacient.html", user=current_user, posts=lista_finala)

    @staticmethod
    @views.route("/create-post", methods=['GET', 'POST'])
    @login_required
    @role_required('pacient')
    def create_post():
        if request.method == "POST":
            text = request.form.get('text')
            depr = DepressionDetector()
            if not text:
                flash('Post cannot be empty', category='error')
            else:
                result = depr.detectDepressionFromtext(text)
                post = Post(text=text, author=current_user.id,result=result)
                db.session.add(post)
                db.session.commit()
                flash('Post created!', category='success')
                return redirect(url_for('pacientView.home'))

        return render_template('create_post.html', user=current_user)

    @staticmethod
    @views.route("/jurnal")
    @role_required('pacient')
    @login_required
    def posts():
        posts_today = Post.query.filter_by(author=current_user.id)
        return render_template("posts.html", user=current_user, posts=posts_today)
