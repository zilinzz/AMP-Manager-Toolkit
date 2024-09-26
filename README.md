# AMP-Manager-Toolkit

## Cloning the Repository
To clone the repository and start working on the project, follow the instructions provided by GitHub at GitHub Docs on [Cloning a Repository][https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository].

For additional Git guides and best practices, refer to [Git Guides][https://github.com/git-guides].

## Collaboration Workflow
### Moving to the master Branch
To switch to the master branch:

```
git checkout master
```

### Rebasing
To rebase and update your local repository:

```
git pull --rebase
```

### Working on Feature Branches
To work on a feature branch:

```
git checkout my-feature-branch
```

### Committing Changes
After implementing your feature, commit changes by only adding Python files (do not add `__pycache__` or similar):

```
git add *.py
git commit -m "your message"
git push origin my-feature-branch
```

### Rebasing onto master
Before merging, rebase your branch onto master:

```
git rebase master
```

### Submitting Pull Requests
After rebasing, submit a pull request through the GitHub web interface. Wait for your peers to review your changes and merge them into the main branch.

## Running the code
