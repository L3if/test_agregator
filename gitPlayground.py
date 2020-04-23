#!/usr/bin/python3
# import pygit2
from pygit2 import Repository, Remote
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
import os.path
from os import path
import sys

# get arg verify path existence

if len(sys.argv) == 1:
    print('path should be specified')
    exit()

if path.exists(sys.argv[1]) and str(sys.argv[1]).endswith('.git'):
    pass
else:
    print('path ether not exis or it\'s not a repo')

repo = Repository(sys.argv[1])

# print(list(repo.branches))

# branch = repo.lookup_branch('develop')
# ref = repo.lookup_reference(branch.name)

branch = repo.lookup_branch('develop')
ref = repo.lookup_reference(branch.name)
repo.checkout(ref)
pass


#def function get_commit_list(first_commit_id, last_commit_id):
for commit in repo.walk(repo.head.target, GIT_SORT_REVERSE):
    print(commit.id)
    if commit.parents:
        diffs = repo.diff(commit.parents[0], commit)
        print (len(diffs))
        for p in diffs:
            print(p.text)
        
        
        
        pass
    '''diffs = repo.diff('HEAD', commit.id)
    patches = [p for p in diffs]
    for p in patches:
        print
        print(p.text)
        pass'''                                                                        
