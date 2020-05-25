# How to release

## Update used grocy version
1. Create a new branch using `git flow bugfix start update-used-grocy-release`
2. Update the used grocy-docker repository tag in `.travis.yml` to the latest available version
3. Run the tests against these new releases either locally or using Travis CI
4. (Create issues for all upcoming issues)
5. push branch and merge on when checks pass

## Prepare the new release
1. Create a new branch using `git flow release start {NEW_VERSION}` (insert new version number)
2. change the packages version to new version in `setup.py`
3. generate changelog with `github_changelog_generator -u SebRut -p pygrocy --future-release v{{NEW_VERSION}}`