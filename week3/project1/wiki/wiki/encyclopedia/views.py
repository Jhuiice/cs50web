from django.http.response import HttpResponse
from django.shortcuts import render
import re
from . import util
from django import forms
from random import randint
from markdown2 import Markdown

MARKDOWNER = Markdown()

class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea())

class NewEditForm(forms.Form):
    title = forms.CharField(max_length=100, disabled=True)
    content = forms.CharField(widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if request.method == "GET":
        # random entry generator
        if title.lower() == "random":
            list_entries = util.list_entries()
            length_ = len(list_entries)
            random_int = randint(0, length_)
            title = list_entries[random_int]
            entry = util.get_entry(title)
            print(title, entry)
            return render(request, 'encyclopedia/title.html',{
                "title": title,
                "content": MARKDOWNER.convert(entry),
            })
        get_entry = util.get_entry(title)
        if get_entry:
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": MARKDOWNER.convert(get_entry),
            })
        else: 
            return render(request, 'encyclopedia/error.html', {
                "title" : title,
            })
            
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    if request.method == "GET":
        search = request.GET['q']
        # have to call list_entries() first and then use regex to see if there is a match
        # in any of the entries and showcase the entries with substrings of the search
        get_entry = util.get_entry(search)
        if get_entry:
            return render (request, 'encyclopedia/search.html', {
                "entry" : get_entry,
                "title" : search,
            })
        else:
            entries = util.list_entries()
            entry_matches = []
            for entry in entries:
                # match is a list 
                match = re.findall(search.lower(), entry.lower())
                # if there is a match in the list add to substring list
                if match:
                    entry_matches.append(entry)
                    print(entry_matches)
            return render (request, 'encyclopedia/search.html', {
                'title' : search,
                'matches': MARKDOWNER.convert(entry_matches),
            })
    else:
        render(request, "encyclopedia/index.html",{
            "entries": util.list_entries(),
        })


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        list_entries = util.list_entries() 
        if form.is_valid():
            for entry in list_entries:
                if entry.lower() == request.POST['title'].lower():
                    return render(request, 'encyclopedia/error.html', {
                    "error": f"A title of {request.POST['title']} is already created."})

            # save entry into the db
            util.save_entry(request.POST['title'], request.POST['content'])

            return render(request, "encyclopedia/title.html",{
            "title": request.POST['title'],
            "content": MARKDOWNER.convert(request.POST['content']),
            })
                
        else: 
            return render(request, 'encyclopedia/error.html', {
                "error": "Form is invalid"
            })
    else:
        form = NewEntryForm()
        return render(request, 'encyclopedia/create.html', {
            'form': form,
        })

def edit(request, title):
    # form that prepopulates with the entry that is being edited
    # do i need a title parameter? 
    # then save the new entry as the old entry

    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return render(request, 'encyclopedia/title.html', {
            'title': title,
            'content': content,
        })
    
    elif request.method == "GET":
        content = util.get_entry(title)
        form = NewEditForm(initial={'title':title, 'content':content})
        # print(title, content, form)
        return render(request, 'encyclopedia/edit.html', {
            'form': form,
            'title': title,
        })

