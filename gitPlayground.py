#!/usr/bin/python3
# import pygit2
from pygit2 import Repository, Remote, Oid
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

'''branch = repo.lookup_branch('develop')
ref = repo.lookup_reference(branch.name)
repo.checkout(ref)
commit_list = []
for commit in repo.walk(repo.head.target, GIT_SORT_REVERSE):
        commit_list.append(commit.id)
print(commit_list)'''


def get_commit_list(first_commit_id, last_commit_id):
    commit_list = []
    for commit in repo.walk(last_commit_id, GIT_SORT_REVERSE):
        commit_list.append(commit.id)
    first_commit_id_Oid = Oid(hex=first_commit_id)
    modified_commit_list = commit_list[commit_list.index(first_commit_id_Oid):]
    return modified_commit_list


commit_list = get_commit_list('93ab25a44bb2112a659b85eda059b004f8ca43cd', 
                            '250c11c6fff841220d93db5379659342a038436d')
commit = repo.get(commit_list[1])

print(commit.parents[0].id)

print(repo.diff(commit.parents[0], commit)[0].text)






'''for commit in repo.walk(repo.head.target, GIT_SORT_REVERSE):
    print(commit.id)
    if commit.parents:
        diffs = repo.diff(commit.parents[0], commit)
        print(len(diffs))
        for p in diffs:
            print(p.text)
        pass     '''                                                            
