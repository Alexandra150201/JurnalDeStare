from functools import wraps
from flask import request, render_template, make_response, Blueprint
from flask_login import login_required, current_user
from website.domain.models import Post, Pacient
from  website.service.serviceCalendar import  ServiceCalendar

class ControllerTerapeut:

    terapeutView = Blueprint("terapeutView", __name__)

    @staticmethod
    def __role_required(role):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not current_user.role == role:
                    return "Unauthorized access", 403
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    @terapeutView.route("/home/terapeut")
    @login_required
    @__role_required('terapeut')
    def home_Terapeut():
        posts_today = Post.query.filter_by(author=current_user.id)
        pacienti = Pacient.query.filter_by(terapeut_asignat=current_user.id)
        if current_user.role == 'terapeut':
            return render_template("homeTerapeut.html", user=current_user, pacienti=pacienti)
        else:
            return render_template("homePacient.html", user=current_user, posts=posts_today)

    @staticmethod
    @login_required
    @__role_required('terapeut')
    @terapeutView.route("/home/terapeut/get/", methods=["POST"])
    def get():
        ev = ServiceCalendar()
        data = dict(request.form)
        events = ev.get(int(data["month"]), int(data["year"]), int(data["pacient"]))
        return "{}" if events is None else events


