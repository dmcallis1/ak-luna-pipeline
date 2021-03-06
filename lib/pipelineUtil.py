import os
import json
import jsonpatch

def checkPipelineDir(dir):

    error = False

    if not os.path.isdir(dir):
        error = True

    if not os.path.exists(dir + '/projectInfo.json'):
        error = True

    return error

def pipelineStages(dir):

    stageList = [x[1] for x in os.walk(dir + '/environments')]

    stages = {}

    for stage in stageList[0]:

        with open(dir + '/environments/' + stage + '/envInfo.json') as envInfo:
           stageData = json.load(envInfo)
           stageDict = {
                'propertyName': stageData['propertyName'],
                'propertyId': stageData['propertyId'],
                'propertyVersion': stageData['latestVersionInfo']['propertyVersion'],
                'etag': stageData['latestVersionInfo']['etag'],
                'ruleFormat': stageData['latestVersionInfo']['ruleFormat'],
                'stagingStatus': stageData['latestVersionInfo']['stagingStatus'],
                'productionStatus': stageData['latestVersionInfo']['productionStatus']
           }

           stages[stage] = stageDict

    return stages

def compareDefinition(stageDict, propertyDict):

    equal = True
    reason = ''

    if stageDict['propertyVersion'] != propertyDict['versions']['items'][0]['propertyVersion']:
        equal = False
        reason =  reason + '(Version) '

    if stageDict['etag'] != propertyDict['versions']['items'][0]['etag']:
        equal = False
        reason = reason + '(Etag) '

    if stageDict['ruleFormat'] != propertyDict['versions']['items'][0]['ruleFormat']:
        equal = False
        reason = reason + '(Rule Format) '

    if stageDict['stagingStatus'] != propertyDict['versions']['items'][0]['stagingStatus']:
        equal = False
        reason = reason + '(Staging Status) '

    if stageDict['productionStatus'] != propertyDict['versions']['items'][0]['productionStatus']:
        equal = False
        reason = reason + '(Production Status) '

    return equal, reason

def compareStateDefinition(stageDict, propertyDict):

    equal = True
    reason = ''

    patch = jsonpatch.JsonPatch.make_patch(stageDict, propertyDict['versions']['items'][0])

    return equal, reason

def updateDefinition(dir, stage, propertyDict):

    with open(dir + '/environments/' + stage + '/envInfo.json') as envInfo:

        stageData = json.load(envInfo)

        stageData['latestVersionInfo']['propertyVersion'] = propertyDict['versions']['items'][0]['propertyVersion']
        stageData['latestVersionInfo']['etag'] = propertyDict['versions']['items'][0]['etag']
        stageData['latestVersionInfo']['ruleFormat'] = propertyDict['versions']['items'][0]['ruleFormat']
        stageData['latestVersionInfo']['stagingStatus'] = propertyDict['versions']['items'][0]['stagingStatus']
        stageData['latestVersionInfo']['productionStatus'] = propertyDict['versions']['items'][0]['productionStatus']

        envInfo.close()

        with open (dir + '/environments/' + stage + '/envInfo.json', 'w') as outfile:
            json.dump(stageData, outfile, indent=4)
            outfile.close()

    return None

def updateActivation(dir, stage, networkDict):

    with open(dir + '/environments/' + stage + '/envInfo.json') as envInfo:

        networkData = json.load(envInfo)

        dictElement = 'activeIn_' + networkDict['network'] + '_Info'

        networkData[dictElement]['propertyVersion'] = networkDict['version']
        networkData[dictElement]['etag'] = networkDict['etag']

        with open (dir + '/environments/' + stage + '/envInfo.json', 'w') as outfile:
            json.dump(networkData, outfile, indent=4)
            outfile.close()

    return None

def compareSnippet(lunaSnippet, plSnippet):

    with open(lunaSnippet) as file:
        luna = json.load(file)
        file.close()

    with open(plSnippet) as file:
        pipeline = json.load(file)
        file.close()

    patch = jsonpatch.JsonPatch.from_diff(luna, pipeline)
    return patch

def updateImports(dir, importList):

    with open(dir + '/templates/main.json') as template:
        templateData = json.load(template)
        templateData['rules']['children'] = importList
        template.close()

    with open(dir + '/templates/main.json', 'w') as outfile:
        json.dump(templateData, outfile, indent=4)
        outfile.close()

    return None