from django.http import HttpResponse
from django.template import loader


def index(request):
  context = {
	  'greeting': 'Hello, my name is Arthur!'
  }
  template = loader.get_template('core/main.html')
  return HttpResponse(template.render(context, request))


