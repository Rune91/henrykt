from flask import Blueprint, render_template, Response
from flask_login import login_required, current_user

from statapp.db.stat_db import myDB
from statapp.classes import Event, Operator, EvaluationSet
from statapp.forms.forms import NewEventForm, EditEventForm

BP = Blueprint(
    "stats", __name__, static_folder="stat/static", template_folder="stat/templates"
)

@BP.route("index")
@login_required
def index():
    with myDB() as db:
        evaluation_sets_results = db.get_evaluation_sets_by_userid(current_user.UserId)
        evaluation_sets_ = [EvaluationSet(*list(evaluation_set.values())) for evaluation_set in evaluation_sets_results]
    
    return render_template("stats_index.html", evaluation_sets=evaluation_sets_)

@BP.route("download/<int:event_id>")
@login_required
def download(event_id):
    with myDB() as db:
        if event_id == 0:
            result = db.get_all_evaluations_by_userid(current_user.UserId)
            filename = "data_alle.csv"
        else:
            result = db.get_all_evaluations_by_eventid(event_id)
            filename = f"data_{event_id:03}.csv"

    csv_data = "Arrangement,Operatør,Evaluering,Tid\n"
    for evaluation in result:
        evaluation_as_list = list(evaluation.values())
        evaluation_as_list[-1] = evaluation_as_list[-1].strftime("%Y-%m-%d %H:%M:%S")
        csv_data += ",".join([str(e) for e in evaluation_as_list]) + "\n"


    response = Response(u'\uFEFF' + csv_data, content_type="text/csv; charset=utf-8")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response
