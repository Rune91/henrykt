from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import UserMixin, login_user, logout_user

from statapp.db.stat_db import myDB
from statapp.forms.forms import LoginForm

BP = Blueprint(
    "user", __name__, static_folder="stat/static", template_folder="stat/templates"
)

class User(UserMixin):
    def __init__(self, UserId, UserName, UserLogin, UserPin, ValidFrom, ValidTo):
        self.UserId = UserId
        self.UserName = UserName
        self.UserLogin = UserLogin
        self.UserPin = UserPin
        self.ValidFrom = ValidFrom
        self.ValidTo = ValidTo
    
    def user_setup(choice: str, value):
        with myDB() as db:
            if choice == "login":
                result = db.get_user_by_login(value)
            elif choice == "id":
                result = db.get_user_by_id(value)
            else:
                return False
            
            if not result:
                return False
            
            user = User(UserId=result['UserId'],
                        UserName = result['UserName'],
                        UserLogin = result['UserLogin'],
                        UserPin = result['UserPin'],
                        ValidFrom = result['ValidFrom'],
                        ValidTo = result['ValidTo'],)
            return user
        
    def login(username, password):
        user = User.user_setup("login", username)
        if not user or password != user.UserPin:
            # Username or password is wrong
            return False
        login_user(user)
        return True
    
    def get_id(self):
        return self.UserId
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return self.active

@BP.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        logged_in = User.login(username, password)
        if logged_in:
            flash("De er nå innlogget", category="success")
            return redirect(url_for("feedback.options"))
        else:
            print("incorrect user or password")
            flash("Ugyldig brukernavn eller PIN-kode", category="error")

    return render_template("login.html", form=form)

@BP.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("user.login"))