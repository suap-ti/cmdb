from django.shortcuts import render

# Create your views here.
def index(request):
    print(request.user)
    return render(request, 'cmdb/index.html')