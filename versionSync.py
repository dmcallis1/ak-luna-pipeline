import logging
import argparse
import os
import requests
import sys
from lib import pipelineUtil
from akamai.edgegrid import EdgeGridAuth, EdgeRc

# Setup logging
logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# Initialize Argument Parsing
parser = argparse.ArgumentParser(description='Akamai Pipeline Toolkit',
                                 epilog='Supports Akamai pipeline project management, in tandem with Luna',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Positional Args
parser.add_argument('pipeline', metavar='property', type=str, help='The location of the Akamai pipeline CLI project.')

# Optional Arguments for .edgerc sourcing and version
parser.add_argument('--config', action="store", default=os.environ['HOME'] + "/.edgerc", help="Full or relative path to .edgerc file")
parser.add_argument('--section', action="store", default="default", help="The section of the edgerc file with the proper {OPEN} API credentials.")
args = parser.parse_args()

if pipelineUtil.checkPipelineDir(args.pipeline) is not False:
    log.error('The provided pipeline directory location: ' + args.pipeline + ' is either invalid, or not a Akamai pipeline project')
    sys.exit(1)

stageDict = pipelineUtil.pipelineStages(args.pipeline)
log.info('Identified ' + str(len(stageDict.keys())) + ' pipeline stages in pipeline project: ' + args.pipeline)

# Initialize EdgeGrid client
try:
    edgerc = EdgeRc(args.config)
    baseurl = 'https://%s' % edgerc.get(args.section, 'host')
    session = requests.Session()
    session.auth = EdgeGridAuth.from_edgerc(edgerc, args.section)

except Exception as e:
    log.error('Error authenticating Akamai {OPEN} API client.')
    log.error(e)


for stage in stageDict:

    propertyId = 'prp_' + str(stageDict[stage]['propertyId'])
    version = str(stageDict[stage]['propertyVersion'])
    log.info('Identified propertyId: ' + propertyId + '. Latest Version (pipeline): ' + version)

    # Get latest version from Luna
    try:
        endpoint = baseurl + '/papi/v1/properties/' + propertyId + '/versions'
        versionDetails = session.get(endpoint).json()
    except Exception as e:
        log.error('Error pulling versions for property: ' + stageDict[stage]['propertyName'])

    version = str(versionDetails['versions']['items'][0]['propertyVersion'])

    log.info('Pulling property details from Luna for stage: ' + stage + ' property: ' + stageDict[stage]['propertyName'])
    try:
        endpoint = baseurl + '/papi/v1/properties/' + propertyId + '/versions/' + version
        propertyDetails = session.get(endpoint).json()
    except Exception as e:
        log.error('Error pulling property version details.')

    log.info('Comparing Pipeline stage definition with Luna Definition.')
    equal, reason = pipelineUtil.compareDefinition(stageDict[stage], propertyDetails)

    if equal is not True:
        log.info('Found a discrepancy between Luna and Pipeline.')
        log.info('Discrepancy Detected: ' + reason)
        log.info('Reconciling pipeline project stage (' + stage + ') with Luna status...')
        pipelineUtil.updateDefinition(args.pipeline, stage, propertyDetails)
        log.info('Pipeline definition updated with Luna details.')
    else:
        log.info('Property definition for ' + stageDict[stage]['propertyName'] + ' (stage: ' + stage + ') is in sync with Luna.')