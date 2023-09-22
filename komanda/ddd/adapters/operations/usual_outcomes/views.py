from dataclasses import asdict
from pathlib import Path
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from ddd.adapters.operations.usual_outcomes.commands import CreateOutcomeCommand, GetAllCategoriesCommand, GetAllOutcomesCommand, GetUsualOutcomeCommand

OUTCOME_ABS_URL = "/ddd/usual_outcomes/"

def add_outcome_form(request: WSGIRequest):
    if request.method == "POST":
        command = CreateOutcomeCommand()
        command.execute(request.POST)
        return redirect("ddd_all_outcomes")
    command = GetAllCategoriesCommand()
    command.execute()
    result = command.events[0]
    return render(request, "add_usual_outcome.html", {"data": result})

def view_usual_outcome(request, id: int):
    command = GetUsualOutcomeCommand()
    command.execute(id)
    result = command.events[0]
    return render(request, "single_outcome_view.html", {"data": result})

def view_all_outcomes(request):
    command = GetAllOutcomesCommand()
    command.execute()
    result = command.events[0]
    return render(request, "all_outcomes_view.html", {"data": result, "outcome_url": OUTCOME_ABS_URL})