from django.shortcuts import render

# Create your views here.
def main_index(request):
    return render(request,'main/main-index.html')

def about(request):
    return render(request,'main/about.html')

def contact(request):
    return render(request,'main/contact.html')