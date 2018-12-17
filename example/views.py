from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext
from example import main
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt


class HomePageView(TemplateView):
    template_name = "index.html"

def dispqueue(request):
    return render(request, 'dispqueue.html', {'data': ""})

@csrf_exempt
def get_more_tables(request):
    increment = int(request.GET.get('append_increment'))
    increment_to = increment + 1
    runningqueue,queuelist = main.JenkinsQueue.getJenkinsQueue(main.JenkinsQueue)
    #  order = DATAW[3]
    if(len(runningqueue)<1):
        runningqueue.append({"srprofile":"Running queue is empty!"})
    if (len(queuelist) < 1):
        queuelist.append({"srprofile": "Queue is empty!"})
    return render(request, 'get_more_tables.html', {'data': runningqueue, 'data1': queuelist})
