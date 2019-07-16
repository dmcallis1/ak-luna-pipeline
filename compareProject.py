import logging
import argparse
import os
import shutil
import json
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
lunaDiff = [value for value in lunaSnippets if value not in pipelineSnippets]

if pipelineSnippets == lunaSnippets:
    log.info('Snippets are identical between Luna and Pipeline.')

elif lunaDiff:
    log.info('New Luna snippets detected which are not in pipeline project: ' + args.pipeline)

    # Initialize new list with differences
    for snippet in lunaDiff:
        log.info('Copying snippet: ' + snippet + ' to pipeline project: ' + args.pipeline)
        try:
            shutil.copyfile(args.snippets + '/' + snippet, args.pipeline + '/templates/' + snippet)
        except Exception as e:
            log.error('Error copying snippet to target directory!')
            log.error('Attempted to copy: ' + args.snippets + '/' + snippet + ' to destination: ' + args.pipeline + '/templates/' + snippet)
            log.error(e)

else:
    log.info('Pipeline project has more snippets than Luna. Deleting old snippets..')
    for snippet in [value for value in pipelineSnippets if value not in lunaSnippets]:
        log.info('Deleting ' + args.pipeline + '/templates/' + snippet)
        os.remove(args.pipeline + '/templates/' + snippet)

log.info('Updating pipeline template snippet includes.')

try:
    with open(args.snippets + '/main.json') as mainSnippet:
        includes = json.load(mainSnippet)
        pipelineUtil.updateImports(args.pipeline, includes['rules']['children'])

except Exception as e:
    log.error('Failed to update template manifest!')
    log.error(e)

skippedList = []

log.info('Comparing existing snippet structure and content.')
for snippet in [value for value in lunaSnippets if value in pipelineSnippets]:

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

    try:
        shutil.copyfile(args.snippets + '/' + snippet, args.pipeline + '/templates/' + snippet)

    except Exception as e:
        log.error('Error copying snippet: ' + snippet)
        log.error(e)

log.info('The following snippets were not automatically reconciled (snippet content) due to tokens detected within the pipeline snippet: ' + str(skippedList))