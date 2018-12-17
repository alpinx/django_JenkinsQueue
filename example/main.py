import jenkins


class JenkinsQueue:
    def getJenkinsQueue(self):
        server = jenkins.Jenkins('http://jenkins-vm01:8083')
        version = server.get_version()

        print('Hello from Jenkins %s' % (version))

        queuelist = []
        runningqueue = []

        queue_info = server.get_queue_info()
        for queue in queue_info:
            if (queue['task']['name'] == 'SeleniumStartAutomationTests'):
                paramindex = next(
                    item for item in queue['actions'] if item.get('_class') == 'hudson.model.ParametersAction')

                srprofile = paramindex['parameters'][2]['value'].replace('.srprofile', '')
                testname = paramindex['parameters'][0]['value'].replace('INWK.', '').replace('@', '')
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
                paramindex = next(
                    item for item in buildinfo['actions'] if item.get('_class') == 'hudson.model.ParametersAction')
                srprofile = paramindex['parameters'][2]['value'].replace('.srprofile', '')
                testname = paramindex['parameters'][0]['value'].replace('INWK.', '').replace('@', '')
                testname = testname[testname.find('.')+1:]
                vm = buildinfo['builtOn'].replace('Jenkins-', '')
                env = paramindex['parameters'][4]['value']
                runningqueue.append({
                    "srprofile": srprofile,
                    "testname": testname,
                    "vm": vm,
                    "env": env
                })

        for count, item in enumerate([d["srprofile"] for d in queuelist]):
            if item in enumerate([d["srprofile"] for d in runningqueue]):
                queuelist[count]["srprofile"] = item + "      <-- already running!!!"
            if ([d["srprofile"] for d in queuelist]).count(item) > 1:
                queuelist[count]["srprofile"] = item + "      <-- already in queue!!!"
        for count, item in enumerate([d["srprofile"] for d in runningqueue]):

            if ([d["srprofile"] for d in runningqueue]).count(item) > 1:
                runningqueue[count]["srprofile"] = item + "      <-- running twice!!!"

        print(f"Queue count: {len(queuelist)}")
        for i in queuelist:
            print(i)
        print("-----------------------------------------------------------------------")
        print(f"Builds in Progress: {len(runningqueue)}")
        for ri in runningqueue:
            print(ri)
        return runningqueue, queuelist


arr1, arr2 = JenkinsQueue.getJenkinsQueue(JenkinsQueue)
print(arr1)
print(arr2)
