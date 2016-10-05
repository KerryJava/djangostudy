from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Question, Choice
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
# from django.urls import reverse
from django.core.urlresolvers import reverse
from django.views import generic

import json

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def hello(request):
		return HttpResponse("Hello world ! ")

def add(request):
	a = request.GET['a']
	b = request.GET['b']
	c = int(a) + int(b)
	return ajax_list(request)
	#return HttpResponse(str(c))

def index(request):
	    return render(request, 'home.html')

def add2(request, a, b):
	c = int(a) + int(b)
#	return ajax_list(request)
	return ajax_dict(request)

	return HttpResponse(str(c))

def ajax_list(request):
    a = range(100)
    return HttpResponse(json.dumps(a), content_type='application/json')

def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')



def detail(request, question_id):
       return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "Origin You're looking at the results of question %s."
    return HttpResponse(response % question_id)
    
def resultsReverse(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote2(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def index3(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
    	output = ', '.join([q.question_text for q in latest_question_list])
    	return HttpResponse(output)

def index2(request):
   latest_question_list = Question.objects.order_by('-pub_date')[:5]
   template = loader.get_template('polls/index.html')
   context = {
           'latest_question_list': latest_question_list,
        }
   return HttpResponse(template.render(context, request))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:resultsGeneric', args=(question.id,)))
