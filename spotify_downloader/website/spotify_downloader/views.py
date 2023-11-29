from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import linkForm
from . import download

# Create your views here.
def home(request):
    form = linkForm()
    return render(request, 'index.html', context = {'form' : form})

def music(request):
    if request.method == "POST":
        form = linkForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['musicLink']
            print(link)
            download.downloadSongs(link)
            return HttpResponse("Downliading")
        else:
            return HttpResponse("Error")
    else:
        return redirect(home)