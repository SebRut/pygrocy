# Changelog

## [v0.23.0](https://github.com/SebRut/pygrocy/tree/v0.23.0) (2020-09-11)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.22.0...v0.23.0)

**Implemented enhancements:**

- add "get all products" method [\#97](https://github.com/SebRut/pygrocy/issues/97)

**Closed issues:**

- 400 response when posting [\#131](https://github.com/SebRut/pygrocy/issues/131)

**Merged pull requests:**

- switch to json instead of data in post requests [\#132](https://github.com/SebRut/pygrocy/pull/132) ([SebRut](https://github.com/SebRut))

## [v0.22.0](https://github.com/SebRut/pygrocy/tree/v0.22.0) (2020-09-07)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.21.0...v0.22.0)

**Implemented enhancements:**

- prepare 1.0.0 release [\#80](https://github.com/SebRut/pygrocy/issues/80)
- Consider release to comply with semver [\#33](https://github.com/SebRut/pygrocy/issues/33)

**Fixed bugs:**

- With product location disabled nothing works [\#129](https://github.com/SebRut/pygrocy/issues/129)

**Merged pull requests:**

- check if location field exists before parsing [\#130](https://github.com/SebRut/pygrocy/pull/130) ([SebRut](https://github.com/SebRut))
- Update responses requirement from ~=0.11.0 to ~=0.12.0 [\#128](https://github.com/SebRut/pygrocy/pull/128) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update pdoc3 requirement from ~=0.9.0 to ~=0.9.1 [\#126](https://github.com/SebRut/pygrocy/pull/126) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update pdoc3 requirement from ~=0.8.4 to ~=0.9.0 [\#125](https://github.com/SebRut/pygrocy/pull/125) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update responses requirement from ~=0.10.16 to ~=0.11.0 [\#124](https://github.com/SebRut/pygrocy/pull/124) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))

## [v0.21.0](https://github.com/SebRut/pygrocy/tree/v0.21.0) (2020-08-18)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.20.0...v0.21.0)

**Implemented enhancements:**

- consider using ciso8601 instead of iso8601 [\#84](https://github.com/SebRut/pygrocy/issues/84)

**Fixed bugs:**

- Not all fields of Product are set in all cases [\#122](https://github.com/SebRut/pygrocy/issues/122)

**Closed issues:**

- Task without due date gives error [\#119](https://github.com/SebRut/pygrocy/issues/119)

**Merged pull requests:**

- init all Product fields with None by default [\#123](https://github.com/SebRut/pygrocy/pull/123) ([SebRut](https://github.com/SebRut))
- Check for empty string in parse\_date [\#120](https://github.com/SebRut/pygrocy/pull/120) ([isabellaalstrom](https://github.com/isabellaalstrom))
- Update coveralls requirement from ~=2.1.1 to ~=2.1.2 [\#108](https://github.com/SebRut/pygrocy/pull/108) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))

## [v0.20.0](https://github.com/SebRut/pygrocy/tree/v0.20.0) (2020-08-16)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.19.0...v0.20.0)

**Closed issues:**

- Use Product instead of ProductDate in ShoppingListProduct [\#116](https://github.com/SebRut/pygrocy/issues/116)

**Merged pull requests:**

- only localize datetimes not already containing tz info [\#118](https://github.com/SebRut/pygrocy/pull/118) ([SebRut](https://github.com/SebRut))
- Use Product instead of ProductData [\#117](https://github.com/SebRut/pygrocy/pull/117) ([SebRut](https://github.com/SebRut))

## [v0.19.0](https://github.com/SebRut/pygrocy/tree/v0.19.0) (2020-08-14)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.18.0...v0.19.0)

**Merged pull requests:**

- Add endpoint for adding generic entity [\#115](https://github.com/SebRut/pygrocy/pull/115) ([isabellaalstrom](https://github.com/isabellaalstrom))

## [v0.18.0](https://github.com/SebRut/pygrocy/tree/v0.18.0) (2020-08-14)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.17.0...v0.18.0)

**Merged pull requests:**

- Add details for tasks [\#114](https://github.com/SebRut/pygrocy/pull/114) ([isabellaalstrom](https://github.com/isabellaalstrom))

## [v0.17.0](https://github.com/SebRut/pygrocy/tree/v0.17.0) (2020-08-14)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.16.0...v0.17.0)

**Closed issues:**

- Misnaming in enum [\#112](https://github.com/SebRut/pygrocy/issues/112)

**Merged pull requests:**

- fix issue \#112 [\#113](https://github.com/SebRut/pygrocy/pull/113) ([SebRut](https://github.com/SebRut))

## [v0.16.0](https://github.com/SebRut/pygrocy/tree/v0.16.0) (2020-08-13)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.15.0...v0.16.0)

**Implemented enhancements:**

- implement meal plan and recipes interface [\#90](https://github.com/SebRut/pygrocy/issues/90)

**Merged pull requests:**

- Bugfix/bug smashing [\#111](https://github.com/SebRut/pygrocy/pull/111) ([SebRut](https://github.com/SebRut))
-  Add meal plan / recipe interfaces. \#90  [\#109](https://github.com/SebRut/pygrocy/pull/109) ([nervetattoo](https://github.com/nervetattoo))
- Update responses requirement from ~=0.10.15 to ~=0.10.16 [\#107](https://github.com/SebRut/pygrocy/pull/107) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update pdoc3 requirement from ~=0.8.3 to ~=0.8.4 [\#105](https://github.com/SebRut/pygrocy/pull/105) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update coveralls requirement from ~=2.0.0 to ~=2.1.1 [\#104](https://github.com/SebRut/pygrocy/pull/104) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update pdoc3 requirement from ~=0.8.1 to ~=0.8.3 [\#102](https://github.com/SebRut/pygrocy/pull/102) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update responses requirement from ~=0.10.14 to ~=0.10.15 [\#101](https://github.com/SebRut/pygrocy/pull/101) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))

## [v0.15.0](https://github.com/SebRut/pygrocy/tree/v0.15.0) (2020-05-25)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.14.0...v0.15.0)

**Implemented enhancements:**

- implement task API interface [\#91](https://github.com/SebRut/pygrocy/issues/91)
- implement chore details API interface [\#87](https://github.com/SebRut/pygrocy/issues/87)

**Fixed bugs:**

- fix failing travis build because of changed docker-grocy setup [\#92](https://github.com/SebRut/pygrocy/issues/92)

**Closed issues:**

- complete abstraction on top of server data classes [\#95](https://github.com/SebRut/pygrocy/issues/95)
- CurrentStockResponse contains Product data [\#81](https://github.com/SebRut/pygrocy/issues/81)

**Merged pull requests:**

- upgrade used grocy version [\#100](https://github.com/SebRut/pygrocy/pull/100) ([SebRut](https://github.com/SebRut))
- Feature/91 task api [\#99](https://github.com/SebRut/pygrocy/pull/99) ([SebRut](https://github.com/SebRut))
- add all fields from chore details api call [\#98](https://github.com/SebRut/pygrocy/pull/98) ([SebRut](https://github.com/SebRut))
- finish abstraction from api [\#96](https://github.com/SebRut/pygrocy/pull/96) ([SebRut](https://github.com/SebRut))
- fix travis build [\#93](https://github.com/SebRut/pygrocy/pull/93) ([SebRut](https://github.com/SebRut))
- Update responses requirement from ~=0.10.12 to ~=0.10.14 [\#89](https://github.com/SebRut/pygrocy/pull/89) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update pdoc3 requirement from ~=0.6.4 to ~=0.8.1 [\#88](https://github.com/SebRut/pygrocy/pull/88) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update coveralls requirement from ~=1.11.1 to ~=2.0.0 [\#86](https://github.com/SebRut/pygrocy/pull/86) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Fix \#81 [\#82](https://github.com/SebRut/pygrocy/pull/82) ([BlueBlueBlob](https://github.com/BlueBlueBlob))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
