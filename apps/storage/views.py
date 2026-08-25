from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def boxes_view(request):
  return render(request, 'boxes.html')

def faq_view(request):
  return render(request, 'faq.html')