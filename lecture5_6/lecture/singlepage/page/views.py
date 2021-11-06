from django.shortcuts import render
from django.http import Http404, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'page/index.html')

texts = ["Page 1", "Page 2", "Page 3"]

# Single Pages send back responses instead of rendering a whole new page
# This is a good thing to remember
def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num - 1])
    else:
        return Http404("No Such Section")