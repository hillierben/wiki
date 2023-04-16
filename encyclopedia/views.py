from django import forms
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, request, HttpResponseRedirect
import re
from markdown2 import Markdown
from random import choice

from . import util

class CreatePage(forms.Form):
    new_page = forms.CharField(label="Page Title")
    content = forms.CharField(widget=forms.Textarea)



markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, name):
        if not util.get_entry(name):
            return render(request, "encyclopedia/404error.html", {
            })
        else:
            page = name
            words = " "
            with open(f"entries/{page}.md", "r") as file:
                lines = file.readlines()
                for line in lines:
                    new_line = markdowner.convert(line)
                    words += new_line
                 
            return render(request, "encyclopedia/wiki.html", {
                    "title": lines[0].replace("#", ""),
                    "content": words
            })
        

def search(request,):
    print(request.GET["q"])
    if util.get_entry(request.GET["q"]):
        page = request.GET["q"]
        words = " "
        with open(f"entries/{page}.md", "r") as file:
            lines = file.readlines()
            for line in lines:
                new_line = markdowner.convert(line)
                words += new_line
                
        return render(request, "encyclopedia/wiki.html", {
                "title": lines[0].replace("#", ""),
                "content": words
        })
    else:
        pages = []
        for entry in util.list_entries():
            if request.GET["q"].lower() in entry.lower():
                pages.append(entry)
        return render(request, "encyclopedia/search-results.html", {
            "pages": pages
        })
              

def create(request):

    if request.method == "POST":
        for page in util.list_entries():
            if request.POST["new_page"].lower() in page.lower():
                return render(request, "encyclopedia/already_exists.html")
                
        util.save_entry(request.POST["new_page"], request.POST["content"])
        return wiki(request, request.POST["new_page"])

    return render(request, "encyclopedia/create.html", {
        "page": CreatePage()
    })


def edit(request, name):

    if request.method == "GET":
        content = util.get_entry(name.strip())
        title = name.strip()
        class EditPage(forms.Form):
            edit = forms.CharField(label="", widget=forms.Textarea, initial=content)
        edits = EditPage()

        return render(request, "encyclopedia/edit.html", {
            #"prefill": content
            "edit": edits,
            "title": title
        })
              
    elif request.method == "POST":
        util.save_entry(name, request.POST["edit"])
        return wiki(request, name)
    

def random(request):
    list = util.list_entries()
    rand = choice(list)
    return wiki(request, rand)
    