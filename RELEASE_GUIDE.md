# How to release

## Prepare the new release
1. Create a new branch using `git flow release start {NEW_VERSION}` (insert new version number)
2. change the packages version to new version in `setup.py`
3. generate changelog with `github_changelog_generator -u SebRut -p pygrocy --future-release v{{NEW_VERSION}}`