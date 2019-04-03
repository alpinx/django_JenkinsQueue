from operator import itemgetter
import jenkins
import datetime
import time


class JenkinsQueue:
    server = jenkins.Jenkins('http://jenkins-vm01:8083')

    def getJenkinsRunningBuilds(self):
        version = self.server.get_version()
        print('JenkinsRunningBuilds call')
        runningqueue = []
        builds = self.server.get_running_builds()
        for build in builds:
            if build['name'] == 'SeleniumStartAutomationTests':
                buildinfo = self.server.get_build_info(name='SeleniumStartAutomationTests', number=build['number'])

                paramindex = next(item for item in buildinfo['actions']
                                  if item.get('_class') == 'hudson.model.ParametersAction')
                srprofile = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'PROFILE_PROJECT')['value'].replace('INWK.', '').replace(
                    '.srprofile', '')
                testname = next(param for param in paramindex['parameters']
                                if param.get('name') == 'SELENIUM_TAG')['value'].replace('INWK.', '').replace('@', '')
                testname = testname[testname.find('.') + 1:]
                vm = buildinfo['builtOn'].replace('Jenkins-', '')
                env = next(param for param in paramindex['parameters']
                           if param.get('name') == 'ENVIRONMENT')['value']
                duration = (datetime.datetime.now() - datetime.datetime.fromtimestamp(
                    buildinfo['timestamp'] / 1e3)).seconds
                runningqueue.append({
                    "srprofile": srprofile,
                    "testname": testname,
                    "vm": vm,
                    "env": env,
                    "duration": duration
                })
        #print(f"Builds in Progress: {len(runningqueue)}")
        return runningqueue

    def getJenkinsQueue(self):
        print('JenkinsQueue call')
        queuelist = []
        queue_info = self.server.get_queue_info()
        for queue in queue_info:
            if queue['task']['name'] == 'SeleniumStartAutomationTests':
                paramindex = next(
                    item for item in queue['actions'] if item.get('_class') == 'hudson.model.ParametersAction')

                srprofile = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'PROFILE_PROJECT')['value'].replace('INWK.', '').replace(
                    '.srprofile', '')
                testname = next(param for param in paramindex['parameters']
                                if param.get('name') == 'SELENIUM_TAG')['value'].replace('INWK.', '').replace('@', '')
                testname = testname[testname.find('.') + 1:]
                vm = ""
                env = paramindex['parameters'][4]['value']
                queuelist.append({
                    "srprofile": srprofile,
                    "testname": testname,
                    "vm": vm,
                    "env": env
                })
        #print(f"Queue count: {len(queuelist)}")
        return queuelist

    def getJenkinsBuilds(self):
        version = self.server.get_version()

        print('JenkinsFinishedBuilds call')
        finishedbuilds = []
        builds = self.server.get_job_info(name='SeleniumStartAutomationTests')
        for count, build in enumerate(builds['builds']):
            buildinfo = self.server.get_build_info(name='SeleniumStartAutomationTests', number=build['number'])
            if buildinfo['building'] == False:
                status = buildinfo['result']
                paramindex = next(item for item in buildinfo['actions']
                                  if item.get('_class') == 'hudson.model.ParametersAction')
                srprofile = next(param for param in paramindex['parameters']
                                 if param.get('name') == 'PROFILE_PROJECT')['value'].replace('INWK.', '').replace(
                    '.srprofile', '')
                testname = next(param for param in paramindex['parameters']
                                if param.get('name') == 'SELENIUM_TAG')['value'].replace('INWK.', '').replace('@', '')
                testname = testname[testname.find('.') + 1:]
                reportUrl = buildinfo['url'] + "SeleniumReport"
                finishedbuilds.append({
                    "status": status,
                    "srprofile": srprofile,
                    "testname": testname,
                    "report": reportUrl
                })
                if count > 15:
                    break
            # for ri in finishedbuilds:
            #     print(ri)
        return finishedbuilds


def verifyErrorRunning(queuelist, runningqueue):
    for count, item in enumerate([d["srprofile"] for d in queuelist]):
        if item in enumerate([d["srprofile"] for d in runningqueue]):
            queuelist[count]["srprofile"] = item + "      <-- already running!!!"
        if ([d["srprofile"] for d in queuelist]).count(item) > 1:
            queuelist[count]["srprofile"] = item + "      <-- already in queue!!!"
    for count, item in enumerate([d["srprofile"] for d in runningqueue]):
        if ([d["srprofile"] for d in runningqueue]).count(item) > 1:
            runningqueue[count]["srprofile"] = item + "      <-- running twice!!!"
    for count, item in enumerate([d["duration"] / 60 for d in runningqueue]):
        if item > 60:
            runningqueue[count]["srprofile"] += "   <-- Duration is longer as 1 hour!!!"
    return queuelist, runningqueue


def makeBuildsForAllVms(runningqueue):
    runningqueue = sorted(runningqueue, key=itemgetter('vm'))
    allVm = []
    for i in range(2, 12):
        allVm.append({
            "srprofile": "",
            "testname": "",
            "vm": "vm0" + str(i) if i < 10 else "vm" + str(i),
            "env": "",
            "duration": ""
        })


    for count, item in enumerate([d["vm"] for d in runningqueue]):
                 for i, d in enumerate(allVm):
                     if item in d["vm"]:
                        allVm[i]["srprofile"] = runningqueue[count]["srprofile"]
                        allVm[i]["testname"] = runningqueue[count]["testname"]
                        allVm[i]["env"] = runningqueue[count]["env"]
                        allVm[i]["duration"] = runningqueue[count]["duration"]
    return allVm

#
# start = time.time()
# inst = JenkinsQueue()
# arr1 = JenkinsQueue.getJenkinsRunningBuilds(inst)
# end = time.time()
# start2 = time.time()
# all = makeBuildsForAllVms(arr1)
#
# end2 = time.time()
# print(end - start)
# print(end2 - start2)
#print(all)
# print("-------------------")
#
# print(arr1)


