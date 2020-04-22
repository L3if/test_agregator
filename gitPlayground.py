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

print(list(repo.branches))

#branch = repo.lookup_branch('develop')
#ref = repo.lookup_reference(branch.name)

branch = repo.lookup_branch('develop')
ref = repo.lookup_reference(branch.name)
repo.checkout(ref)
pass
for commit in repo.walk(repo.head.target):
    print(commit.id)
    #diffs = repo.diff('HEAD', commit.id)
    #patches = [p for p in diffs]
    #for p in patches:
    #    print
    #    print(p.text)
    #    pass                                                                                                                                                                                                                                                                         