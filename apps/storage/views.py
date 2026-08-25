from django.shortcuts import render

def boxes_view(request):
  return render(request, 'boxes.html')

def faq_view(request):
  return render(request, 'faq.html')