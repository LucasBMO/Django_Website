from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Items
from .forms import CreateNewList


# Create your views here. functions that will show on the front page
def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.items_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2:
                ls.items_set.create(text=txt, complete=False)
            else:
                print('Invalid')

    return render(response, "main/list.html", {"ls": ls})


def home(response):
    return render(response, 'main/home.html', {})


def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()

        return HttpResponseRedirect(f"/{t.id}")
    else:
        form = CreateNewList()
    return render(response, 'main/create.html', {"form": form})
