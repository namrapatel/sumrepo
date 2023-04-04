from github import Github, UnknownObjectException

url = 'https://raw.githubusercontent.com/HaliteChallenge/Halite/master/admin/cron/haliteEmailer.py'
# Parse the URL to extract the repository name, file path, and branch name
_, _, repo_name, _, branch_name, *file_path = url.split('/')
file_path = '/'.join(file_path)

print(repo_name)
print(branch_name)
print(file_path)


# Authenticate with GitHub using an access token or username/password
g = Github('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')
# Retrieve the repository and branch
try:
    repo = g.get_repo(repo_name)
    branch = repo.get_branch(branch_name)
except UnknownObjectException as e:
    print(f"Error: {e}")
    print("Make sure the repository and branch names are correct.")
    exit()
# Retrieve the file contents as a string
try:
    file_contents = repo.get_contents(file_path, ref=branch.name).decoded_content.decode()
except UnknownObjectException as e:
    print(f"Error: {e}")
    print("Make sure the file path and name are correct.")
    exit()

print(file_contents)
