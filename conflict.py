#!/usr/bin/python
"""Conflict creation tool for EECS 183 lecture.

Usage:
  conflict.py create <filename>
  conflict.py commit <text>
"""

import requests, re, time, os, glob, sys, pprint, json
from docopt import docopt
REPO = "git@github.com:eecs183/lecture_practice.git"
UNIQNAMES = "uniqnames.txt"

def generate(text):
    data = requests.get("https://api.github.com/repos/eecs183/lecture_practice/git/refs/heads")
    pprint.pprint(data.json())

    # move into the directory
    for branch in data.json():
        name = branch["ref"].split('/')[-1]
        if name != "master":
            os.system("git checkout {}".format(name))
            os.system("echo {} >> README.md".format(text))
            os.system("git add README.md")
            os.system("git commit -m 'automated commit from stevemer'")
            os.system("git push")

def create_branches(filename):
    data = requests.get("https://api.github.com/repos/eecs183/lecture_practice/git/refs/heads")
    pprint.pprint(data.json())

    master = None
    for branch in data.json():
        if branch["ref"].split('/')[-1] == "master":
            master = branch
            break
        pass
    assert(master)

    for uniqname in [x.strip() for x in open(filename, "rU").readlines()]:
        req = {
            "ref": "refs/heads/{}".format(uniqname),
            "sha": str(master["object"]["sha"])
        }
        print "Sending: {}".format(req)
        result = requests.post('https://api.github.com/repos/eecs183/lecture_practice/git/refs', data=json.dumps(req), auth = ('stevemer', 'temp_password1'))
        print result, result.text

if __name__ == '__main__':
    arguments = docopt(__doc__, version='EECS 183 Conflict Generator 1.0')
    if arguments['commit']:
        generate(arguments['<text>'])
    elif arguments['create']:
        create_branches(arguments['<filename>'])
    else:
        print "Invalid arguments" 
