from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item

# Create your views here.
# runs everytime homepage is called
def home_page(request):
    # request = HttpRequest 
    # checks Http Request method = Post
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
        
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
