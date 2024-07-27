from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

from statapp.db.stat_db import myDB
from statapp.classes import Event, Operator
from statapp.forms.forms import FeedbackOptionsForm

BP = Blueprint(
    "feedback", __name__, static_folder="stat/static", template_folder="stat/templates"
)

@BP.route("/<event_id>/<operator_id>")
@login_required
def index(event_id, operator_id):
    with myDB() as db:
        event = Event(*db.get_event_by_id(event_id).values())
        operator = Operator(*db.get_operator_by_id(operator_id).values())
    return render_template("feedback.html", event=event, operator=operator)


@BP.route("/options", methods=["GET", "POST"])
@login_required
def options():
    print(current_user)
    form = FeedbackOptionsForm()

    with myDB() as db:
        event_results = db.get_all_events_by_user(current_user.UserId)
        events = [Event(*list(event.values())) for event in event_results]
        operator_results = db.get_all_operators_by_user(current_user.UserId)
        operators = [Operator(*list(operator.values())) for operator in operator_results]

    form.event.choices = [(event.id, event.name) for event in events]
    form.operator.choices = [(operator.id, operator.name) for operator in operators]

    if form.validate_on_submit():
        print(f"form validated! {form.event.data}")
        event_id = form.event.data
        operator_id = form.operator.data
        return redirect(url_for("feedback.index", event_id=event_id, operator_id=operator_id))

    return render_template("feedback_options.html", form=form)


@BP.route("/send/<event_id>/<operator_id>/<evaluation>")
@login_required
def send(event_id, operator_id, evaluation):
    with myDB() as db:
        db.insert_evaluation(event_id, operator_id, evaluation)


    response = jsonify(success=True)
    response.status_code = 200
    return response

    #return "success", 200, {'Content-Type': 'text/plain'}


