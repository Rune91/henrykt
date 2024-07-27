from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from statapp.db.stat_db import myDB
from statapp.classes import Event, Operator
from statapp.forms.forms import NewEventForm, EditEventForm

BP = Blueprint(
    "event", __name__, static_folder="stat/static", template_folder="stat/templates"
)

@BP.route("new", methods=["GET", "POST"])
@login_required
def new():
    form = NewEventForm()

    if form.validate_on_submit():
        event_name = form.name.data
        with myDB() as db:
            db.insert_event(current_user.UserId, event_name)
        return redirect(url_for("event.index"))
    
    return render_template("new_event.html", form=form)

@BP.route("index")
@login_required
def index():
    with myDB() as db:
        event_results = db.get_all_events_by_user(current_user.UserId)
        events = [Event(*list(event.values())) for event in event_results]
        operator_results = db.get_all_operators_by_user(current_user.UserId)
        operators = [Operator(*list(operator.values())) for operator in operator_results]
    return render_template("events_index.html", events=events, operators=operators)

@BP.route("edit/<event_id>", methods=["GET", "POST"])
@login_required
def edit(event_id):
    with myDB() as db:
        result = db.get_event_by_id(event_id)
        event = Event(*list(result.values()))
    
    form = EditEventForm()

    if form.validate_on_submit():
        new_event_name = form.name.data        
        with myDB() as db:
            db.change_name_for_event(event_id, new_event_name)
        return redirect(url_for("event.index"))
    
    # Set default form data
    form.name.data = event.name

    return render_template("edit_event.html", form=form, event=event)
