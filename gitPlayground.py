#!/usr/local/bin/python3
import pygit2
from pygit2 import Repository, Remote, Oid
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
from os import path
import sys
import structparser
import pprint
import argparse
import utils


def get_commit_id_list(last_commit_id=None, first_commit_id=None):
    commit_list = []
    last = last_commit_id if last_commit_id is not None else repo.head.target
    for commit in repo.walk(last, GIT_SORT_REVERSE):
        commit_list.append(commit.id)
    
    first_commit_id_Oid = Oid(hex=first_commit_id) if first_commit_id is not None else commit_list[0]
    
    modified_commit_list = commit_list[commit_list.index(first_commit_id_Oid):]
    return modified_commit_list


def get_hunks_in_commits(start_commit, last_commit):
    changed_func_dict = {}
    for patch in repo.diff(start_commit, last_commit):
        if patch.delta.new_file.path not in changed_func_dict:
            changed_func_dict.update({patch.delta.new_file.path: []})
        for hunk in patch.hunks:
            changed_func_dict[patch.delta.new_file.path].append(hunk)
    return changed_func_dict

# get arg

# args parsed here, current args are: --path <path to repo> --branch


def git_perform_analysis(start, finish, path):
    import os
    # get list of files in start commit
    utils.git_checkout(path, start)
    start_files_funcs = {}
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.cpp' in file or '.h' in file:
                start_files_funcs.update({os.path.join(r, file): structparser.get_cpp_funcs(os.path.join(r, file))})
    pprint.pprint(start_files_funcs)
    # get list of files in start commit
    utils.git_checkout(path, finish)
    finish_files_funcs = {}
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.cpp' in file or '.h' in file:
                finish_files_funcs.update({os.path.join(r, file): structparser.get_cpp_funcs(os.path.join(r, file))})
    
    pprint.pprint(finish_files_funcs)
    return 


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Tool to get and parse changed structures and instrunctuions in any .cpp repository")

    parser.add_argument("-p", "--path", help="path to a repository",
                        type=str)
    parser.add_argument("-b", "--branch", help="branch name to mine changes",
                        type=str)
    parser.add_argument("-l", "--list", help="list full commit list in branch",
                        action='store_true')
    parser.add_argument("-s", "--start", help="full commit id to start from",
                        type=str)
    parser.add_argument("-f", "--finish", help="full commit id to end with",
                        type=str)

    args = parser.parse_args()
    if args.path:
        # verify path existence
        if path.exists(args.path) and args.path.endswith('.git'):
            proj_path = args.path[:-4]
            repo = Repository(args.path)
            if args.branch and args.branch in list(repo.branches.local):
                branch = repo.lookup_branch(list(repo.branches.local)[list(repo.branches.local).index(args.branch)])
                ref = repo.lookup_reference(branch.name)
                repo.checkout(ref)
                print('Current Branch:')
                print(repo.head.shorthand)
                if args.list:
                    pprint.pprint(get_commit_id_list(args.finish, args.start))
                if args.start and args.finish:
                    git_perform_analysis(args.start, args.finish, proj_path)
            else:
                # pyprint avaliable branches
                print('Specify one of local avaliable local branches:')
                print(*list(repo.branches.local), sep="\n")
    else:
        print('path ether not exis or it\'s not a repo')
        exit()




    # print(structparser.get_cpp_funcs('/Users/tester/aggr/fuzzingpintool/Tracker.cpp'))


    # hunks_dict = get_hunks_in_commits(start_commit, last_commit)

    '''for key in hunks_dict:
        for hunk in hunks_dict[key]:
            print(hunk.header)



    pprint.pprint(get_hunks_in_commits(start_commit, last_commit))'''

