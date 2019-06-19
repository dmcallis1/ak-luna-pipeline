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
    log.info('Snippets are identical. No reconciliation needed.')
    sys.exit(0)
else:
    diff = [x for x in lunaSnippets if x not in pipelineSnippets]
    log.info('Snippets are not identical - found ' + str(len(diff)) + ' new snippets.')
    try:
        log.info('Copying snippets from: ' + args.snippets + ' to: ' + args.pipeline + '/templates')
        for snippet in diff:
                shutil.copyfile(args.snippets + '/' + snippet, args.pipeline + '/templates/' + snippet)
        sys.exit(0)
    except Exception as e:
        log.error('Error copying snippet: ' + snippet)
        sys.exit(1)

