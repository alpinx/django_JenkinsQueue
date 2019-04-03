from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext
from example.main import JenkinsQueue
from example import main
import jenkins
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt


class HomePageView(TemplateView):
    template_name = "index.html"

def dispqueue(request):
    return render(request, 'dispqueue.html', {'data': ""})


instance = JenkinsQueue()


@csrf_exempt
def get_more_tables(request):
    increment= int(request.GET.get('append_increment'))
    queuelist = JenkinsQueue.getJenkinsQueue(instance)
    runningqueue = JenkinsQueue.getJenkinsRunningBuilds(instance)
    #queuelist, runningqueue = main.verifyErrorRunning(queuelist, runningqueue)
    #  order = DATAW[3]
    if(len(runningqueue)<1):
        runningqueue.append({"srprofile":"Running queue is empty!"})
    else:
        runningqueue = main.makeBuildsForAllVms(runningqueue)
    if (len(queuelist) < 1):
        queuelist.append({"srprofile": "Queue is empty!"})

    return render(request, 'get_more_tables_All_Vm.html', {'data': runningqueue, 'data1': queuelist})

@csrf_exempt
def get_finished_builds(request):
    increment = int(request.GET.get('append_increment2'))
    server = jenkins.Jenkins('http://jenkins-vm01:8083')
    increment_to = increment + 1
    builds = JenkinsQueue.getJenkinsBuilds(instance)
    #  order = DATAW[3]
    if len(builds) < 1:
        builds.append({"testname": "There is no finished builds!"})
    return render(request, 'get_finished_builds.html', {'data': builds})
