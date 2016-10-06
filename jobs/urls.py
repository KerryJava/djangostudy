from django.conf.urls import url

from . import views
app_name = 'polls'

urlpatterns = [
		    # ex: /polls/
      url(r'^$', views.index2, name='index2'),
	    # ex: /polls/5/
      url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
      url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
					    # ex: /polls/5/vote/
      url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
      url(r'^(?P<question_id>[0-9]+)/resultsReverse/$', views.resultsReverse, name='resultsReverse'),
      url(r'^(?P<pk>[0-9]+)/resultsGeneric/$', views.ResultsView.as_view(), name='resultsGeneric'),
]

# urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)  

