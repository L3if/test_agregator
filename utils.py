import subprocess


def git_checkout(pwd, commit_id):
    cmd = ['git', 'checkout', commit_id]
    p = subprocess.Popen(cmd, cwd=pwd, stdout=PIPE)
    p.wait()
    return p.returncode
