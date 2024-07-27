from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from statapp.db.stat_db import myDB
from statapp.classes import Event, Operator
from statapp.forms.forms import NewOperatorForm, EditOperatorForm

BP = Blueprint(
    "operator", __name__, static_folder="stat/static", template_folder="stat/templates"
)

@BP.route("new", methods=["GET", "POST"])
@login_required
def new():
    form = NewOperatorForm()

    if form.validate_on_submit():
        operator_name = form.name.data
        with myDB() as db:
            db.insert_operator(current_user.UserId, operator_name)
        return redirect(url_for("event.index"))
    
    return render_template("new_operator.html", form=form)

@BP.route("edit/<operator_id>", methods=["GET", "POST"])
@login_required
def edit(operator_id):
    with myDB() as db:
        result = db.get_operator_by_id(operator_id)
        operator = Operator(*list(result.values()))
    
    form = EditOperatorForm()

    if form.validate_on_submit():
        new_operator_name = form.name.data        
        with myDB() as db:
            db.change_name_for_operator(operator_id, new_operator_name)
        return redirect(url_for("event.index"))
    
    # Set default form data
    form.name.data = operator.name

    return render_template("edit_operator.html", form=form, operator=operator)
