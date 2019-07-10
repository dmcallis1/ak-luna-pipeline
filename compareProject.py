import logging
import argparse
import os
import shutil
import sys
from lib import pipelineUtil

# Setup logging
logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# Initialize Argument Parsing
parser = argparse.ArgumentParser(description='Akamai Pipeline Toolkit',
                                 epilog='Supports Akamai pipeline project management, in tandem with Luna',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Positional Args
parser.add_argument('pipeline', metavar='pipeline', type=str, help='The location of the Akamai pipeline CLI project.')
parser.add_argument('snippets', metavar='snippets', type=str, help='The location of the property snippets to compare.')
args = parser.parse_args()

pipelineSnippets = [f for f in os.listdir(args.pipeline + '/templates') if os.path.isfile(os.path.join(args.pipeline + '/templates', f))]
lunaSnippets = [f for f in os.listdir(args.snippets) if os.path.isfile(os.path.join(args.snippets, f))]

if pipelineSnippets == lunaSnippets:
    log.info('Snippet counts are identical between Luna and Pipeline.')

skippedList = []

for snippet in lunaSnippets:

    luna = os.path.join(args.snippets, snippet)
    pipeline = os.path.join(args.pipeline + '/templates', snippet)

    diff = pipelineUtil.compareSnippet(luna, pipeline)

    isToken = False

    if bool(diff) is True:
        log.info('Discrepancy detected between snippet: ' + snippet)
        for element in diff:

            if '${env.' in str(element['value']):
                isToken = True
                skippedList.append(snippet)
                break

    else:
        log.info('No structural changes detected in snippet: ' + snippet)
        continue

    if isToken is True:
        log.info('Tokens detected in patch for snippet: ' + snippet)
        log.info('This snippet needs to be manually reconciled!')
        continue

    log.info('No tokens were detected in the pipeline snippet ' + snippet + '. It will be replaced with the version from Luna.')
    shutil.copyfile(args.snippets + '/' + snippet, args.pipeline + '/templates/' + snippet)

log.info('The following snippets were not automatically reconciled due to tokens detected: ' + str(skippedList))