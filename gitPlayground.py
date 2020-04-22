#!/usr/bin/python3
#import pygit2
from pygit2 import Repository
from pygit2 import GIT_SORT_TOPOLOGICAL
import os.path
from os import path
import sys

#get arg verify path existence

if  len(sys.argv) == 1:
    print('path should be specified')
    exit()

if path.exists(sys.argv[1]) and str(sys.argv[1]).endswith('.git'):
    pass
else:
    print('path ether not exis or it\'s not a repo')

repo = Repository(sys.argv[1])

for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
    #print(commit.message)
    diffs = repo.diff('HEAD', 'HEAD~1')
    patches = [p for p in diffs]
    for p in patches:
        print(p.text)
                                                                                                                                                                                                                                                                                