from django.shortcuts import render
import os

# Create your views here.

def tables_view(request): #ADDON
    path = os.path.join( os.getcwd(), "catalog", "templates", "tables.html")
    with open(path, "r") as f:
        print(f.read())
    return render(request, path) # {'form': login_form, 'message': message}