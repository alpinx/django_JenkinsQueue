import calendar
import jenkins
from operator import itemgetter
import datetime
import time
import pytz


class JenkinsQueue:
    def getJenkinsQueue(self):
        server = jenkins.Jenkins('http://jenkins-vm01:8083')
        version = server.get_version()

        print('JenkinsQueue call')

        queuelist = []
        runningqueue = []

        queue_info = server.get_queue_info()
        for queue in queue_info:
            if (queue['task']['name'] == 'SeleniumStartAutomationTests'):
                paramindex = next(
                    item for item in queue['actions'] if item.get('_class') == 'hudson.model.ParametersAction')

                srprofile = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'PROFILE_PROJECT')['value'].replace('INWK.', '').replace('.srprofile', '')
                testname = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'SELENIUM_TAG')['value'].replace('INWK.', '').replace('@', '')
                testname = testname[testname.find('.')+1:]
                vm = ""
                env = paramindex['parameters'][4]['value']
                queuelist.append({
                    "srprofile": srprofile,
                    "testname": testname,
                    "vm": vm,
                    "env": env
                })
        builds = server.get_running_builds()
        for build in builds:
            if (build['name'] == 'SeleniumStartAutomationTests'):
                buildinfo = server.get_build_info(name='SeleniumStartAutomationTests', number=build['number'])

                paramindex = next(item for item in buildinfo['actions']
                                  if item.get('_class') == 'hudson.model.ParametersAction')
                srprofile = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'PROFILE_PROJECT')['value'].replace('INWK.', '').replace('.srprofile', '')
                testname = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'SELENIUM_TAG')['value'].replace('INWK.', '').replace('@', '')
                testname = testname[testname.find('.')+1:]
                vm = buildinfo['builtOn'].replace('Jenkins-', '')
                env = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'ENVIRONMENT')['value']
                duration = (datetime.datetime.now() - datetime.datetime.fromtimestamp(buildinfo['timestamp']/ 1e3)).seconds
                runningqueue.append({
                    "srprofile": srprofile,
                    "testname": testname,
                    "vm": vm,
                    "env": env,
                    "duration": duration
                })

        for count, item in enumerate([d["srprofile"] for d in queuelist]):
            if item in enumerate([d["srprofile"] for d in runningqueue]):
                queuelist[count]["srprofile"] = item + "      <-- already running!!!"
            if ([d["srprofile"] for d in queuelist]).count(item) > 1:
                queuelist[count]["srprofile"] = item + "      <-- already in queue!!!"
        for count, item in enumerate([d["srprofile"] for d in runningqueue]):
            if ([d["srprofile"] for d in runningqueue]).count(item) > 1:
                runningqueue[count]["srprofile"] = item + "      <-- running twice!!!"
        for count, item in enumerate([d["duration"]/60 for d in runningqueue]):
            if item > 60:
                runningqueue[count]["srprofile"] +="   <-- Duration is longer as 1 hour!!!"
        print(f"Queue count: {len(queuelist)}")
        for i in queuelist:
            print(i)
        print("-----------------------------------------------------------------------")
        print(f"Builds in Progress: {len(runningqueue)}")
        # for ri in runningqueue:
        #     print(ri)
        return sorted(runningqueue, key=itemgetter('srprofile')), sorted(queuelist, key=itemgetter('srprofile'))

    def getJenkinsBuilds(self):
        server = jenkins.Jenkins('http://jenkins-vm01:8083')
        version = server.get_version()

        print('JenkinsBuilds call')
        finishedbuilds = []
        builds = server.get_job_info(name='SeleniumStartAutomationTests')
        for build in builds['builds']:
            buildinfo = server.get_build_info(name='SeleniumStartAutomationTests', number=build['number'])
            if buildinfo['building'] == False:
                status = buildinfo['result']
                paramindex = next(item for item in buildinfo['actions']
                                  if item.get('_class') == 'hudson.model.ParametersAction')
                srprofile = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'PROFILE_PROJECT')['value'].replace('INWK.', '').replace(
                    '.srprofile', '')
                testname = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'SELENIUM_TAG')['value'].replace('INWK.', '').replace('@', '')
                testname = testname[testname.find('.')+1:]
                reportUrl = buildinfo['url']+"SeleniumReport"
                finishedbuilds.append({
                    "status": status,
                    "srprofile": srprofile,
                    "testname": testname,
                    "report": reportUrl
                })
                if len(finishedbuilds) > 15:
                    break
            # for ri in finishedbuilds:
            #     print(ri)
        return finishedbuilds

arr1 = JenkinsQueue.getJenkinsBuilds(JenkinsQueue)
print("-------------------")

print(arr1)

