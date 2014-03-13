##############################
# Play a single song from the command line
# Usage: python cplay.py "{Song Name}"
# 
# Will play the first playable song returned from a search for that song name
##############################

from __future__ import print_function

import subprocess
import argparse
import utils


parser = argparse.ArgumentParser(description='Play a song.')
parser.add_argument('songName')
args = parser.parse_args()

utils.play(args.songName)
