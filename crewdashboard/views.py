from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers

# Create your views here.

@login_required(login_url='/cleanify/login/')
def show_dashboard(request):
    return render(request, "todolist_ajax.html")

def show_json(request):
    user = request.user
    data_todo_list = ListToDo.objects.filter(user=user)
    return HttpResponse(serializers.serialize("json", data_todo_list), content_type="application/json")