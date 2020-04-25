# How to release

## Update used docker images
1. Create a new branch using `git flow support start update-used-grocy-release`
2. Update the used docker images in `docker-compose.yml` to the latest available version
3. Run the tests against these new releases either locally or using Travis CI
4. (Create issues for all upcoming issues)

## Prepare the new release
1. Create a new branch using `git flow release start {NEW_VERSION}` (insert new version number)
2. change the packages version to new version in `setup.py`