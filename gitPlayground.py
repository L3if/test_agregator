#!/usr/bin/python3
# import pygit2
from pygit2 import Repository, Remote, Oid
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
from os import path
import sys
import structparser
import pprint
import argparse

# get arg
# verify path existence
#print avaliable branches

if len(sys.argv) == 1:
    print('path should be specified')
    exit()

if path.exists(sys.argv[1]) and str(sys.argv[1]).endswith('.git'):
    proj_path = sys.argv[1][:-4]
    pass
else:
    print('path ether not exis or it\'s not a repo')
    exit()

repo = Repository(sys.argv[1])
print('Current Branch:')
print(repo.head.shorthand)
print('Avaliable branches:')
print(*list(repo.branches.local), sep="\n")

branch = repo.lookup_branch(list(repo.branches.local)[1])
ref = repo.lookup_reference(branch.name)
repo.checkout(ref)

'''branch = repo.lookup_branch('develop')
ref = repo.lookup_reference(branch.name)
repo.checkout(ref)
commit_list = []
for commit in repo.walk(repo.head.target, GIT_SORT_REVERSE):
        commit_list.append(commit.id)
print(commit_list)'''

print(structparser.get_cpp_funcs('/Users/tester/aggr/fuzzingpintool/Tracker.cpp'))


def get_commit_id_list(last_commit_id=None, first_commit_id=None):
    commit_list = []
    last = last_commit_id if last_commit_id is not None else repo.head.target
    for commit in repo.walk(last, GIT_SORT_REVERSE):
        commit_list.append(commit.id)
    
    first_commit_id_Oid = Oid(hex=first_commit_id) if first_commit_id is not None else commit_list[0]
    
    modified_commit_list = commit_list[commit_list.index(first_commit_id_Oid):]
    return modified_commit_list
 
    
commit_id_list = get_commit_id_list()
print(commit_id_list)

commit_id_list = get_commit_id_list('250c11c6fff841220d93db5379659342a038436d',
                                    '4766ee44dcf75a28ac728d9292d2f09419982ac5')

print(commit_id_list)
start_commit = repo.get(commit_id_list[0])
last_commit = repo.get(commit_id_list[-1])


def get_hunks_in_commits(start_commit, last_commit):
    changed_func_dict = {}
    for patch in repo.diff(start_commit, last_commit):
        if patch.delta.new_file.path not in changed_func_dict:
            changed_func_dict.update({patch.delta.new_file.path: []})
        for hunk in patch.hunks:
            changed_func_dict[patch.delta.new_file.path].append(hunk)
    return changed_func_dict
    
hunks_dict = get_hunks_in_commits(start_commit, last_commit)

for key in hunks_dict:
    for hunk in hunks_dict[key]:
        print(hunk.header)



pprint.pprint(get_hunks_in_commits(start_commit, last_commit))

