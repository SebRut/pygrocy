# Changelog

## [v1.1.0](https://github.com/SebRut/pygrocy/tree/v1.1.0) (2022-03-05)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v1.0.0...v1.1.0)

**Implemented enhancements:**

- Feature: Edit Stock [\#201](https://github.com/SebRut/pygrocy/issues/201)
- Add path in request when creating base url [\#121](https://github.com/SebRut/pygrocy/issues/121)
- Get product by Barcode [\#85](https://github.com/SebRut/pygrocy/issues/85)

**Fixed bugs:**

- min\_stock\_amount should be float, not int [\#217](https://github.com/SebRut/pygrocy/issues/217)

**Closed issues:**

- execute\_chore is formatting time in UTC time. grocy server ignores the timezone, so it shifts the date of chore execution [\#222](https://github.com/SebRut/pygrocy/issues/222)
- Update Product Userfields [\#196](https://github.com/SebRut/pygrocy/issues/196)

**Merged pull requests:**

- update python [\#219](https://github.com/SebRut/pygrocy/pull/219) ([SebRut](https://github.com/SebRut))
- Optional float [\#218](https://github.com/SebRut/pygrocy/pull/218) ([harshi1122](https://github.com/harshi1122))
- Update responses requirement from ~=0.14.0 to ~=0.18.0 [\#216](https://github.com/SebRut/pygrocy/pull/216) ([dependabot[bot]](https://github.com/apps/dependabot))
- Added support for product quantities [\#214](https://github.com/SebRut/pygrocy/pull/214) ([andreheuer](https://github.com/andreheuer))
- Update pydantic requirement from ~=1.8.2 to \>=1.8.2,\<1.10.0 [\#212](https://github.com/SebRut/pygrocy/pull/212) ([dependabot[bot]](https://github.com/apps/dependabot))
- Feature/edit stock [\#209](https://github.com/SebRut/pygrocy/pull/209) ([georgegebbett](https://github.com/georgegebbett))
- Product by barcode [\#208](https://github.com/SebRut/pygrocy/pull/208) ([georgegebbett](https://github.com/georgegebbett))
- Update iso8601 requirement from ~=0.1.16 to \>=0.1.16,\<1.1.0 [\#202](https://github.com/SebRut/pygrocy/pull/202) ([dependabot[bot]](https://github.com/apps/dependabot))
- Update tzlocal requirement from \<3.0,\>=2.1 to \>=2.1,\<5.0 [\#198](https://github.com/SebRut/pygrocy/pull/198) ([dependabot[bot]](https://github.com/apps/dependabot))
- ProductDetailsResponse last\_used Type Date instead of Datetime [\#194](https://github.com/SebRut/pygrocy/pull/194) ([sebiecker](https://github.com/sebiecker))
- support path for url [\#193](https://github.com/SebRut/pygrocy/pull/193) ([SebRut](https://github.com/SebRut))
- Update responses requirement from ~=0.13.4 to ~=0.14.0 [\#191](https://github.com/SebRut/pygrocy/pull/191) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.0](https://github.com/SebRut/pygrocy/tree/v1.0.0) (2021-09-10)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.30.0...v1.0.0)

**Implemented enhancements:**

- Add assigned\_to\_user to task [\#188](https://github.com/SebRut/pygrocy/issues/188)
- Done time should be optional, as it is for execute\_chore call [\#176](https://github.com/SebRut/pygrocy/issues/176)
- Add support for meal plan sections in grocy v3.1.0 [\#172](https://github.com/SebRut/pygrocy/issues/172)
- Add debug mode [\#167](https://github.com/SebRut/pygrocy/issues/167)
- Missing generic put and get option [\#155](https://github.com/SebRut/pygrocy/issues/155)
- add "get all products" method [\#97](https://github.com/SebRut/pygrocy/issues/97)

**Fixed bugs:**

- Sending no time when tracking chore gives an error [\#175](https://github.com/SebRut/pygrocy/issues/175)

**Closed issues:**

- add category field to task [\#189](https://github.com/SebRut/pygrocy/issues/189)
- support consuming decimal amounts [\#187](https://github.com/SebRut/pygrocy/issues/187)

**Merged pull requests:**

- add assigned\_to\_user field to Task [\#190](https://github.com/SebRut/pygrocy/pull/190) ([SebRut](https://github.com/SebRut))
- apply black to everything [\#185](https://github.com/SebRut/pygrocy/pull/185) ([SebRut](https://github.com/SebRut))
- migrate to pydantic [\#184](https://github.com/SebRut/pygrocy/pull/184) ([SebRut](https://github.com/SebRut))
- add basic support for product and note type [\#183](https://github.com/SebRut/pygrocy/pull/183) ([SebRut](https://github.com/SebRut))
- add meal plan section support [\#182](https://github.com/SebRut/pygrocy/pull/182) ([SebRut](https://github.com/SebRut))
- add users getter [\#170](https://github.com/SebRut/pygrocy/pull/170) ([SebRut](https://github.com/SebRut))

## [v0.30.0](https://github.com/SebRut/pygrocy/tree/v0.30.0) (2021-08-23)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.29.0...v0.30.0)

**Fixed bugs:**

- Lovelace not accessible [\#158](https://github.com/SebRut/pygrocy/issues/158)

**Closed issues:**

- grocy.update\_generic Entity\_type not callable [\#159](https://github.com/SebRut/pygrocy/issues/159)

**Merged pull requests:**

- make done\_time optional for complete\_task [\#181](https://github.com/SebRut/pygrocy/pull/181) ([SebRut](https://github.com/SebRut))
- pin down tzlocal to \<3.0 [\#180](https://github.com/SebRut/pygrocy/pull/180) ([SebRut](https://github.com/SebRut))
- add execute chore tests [\#179](https://github.com/SebRut/pygrocy/pull/179) ([SebRut](https://github.com/SebRut))
- pin dependencies in setup.py [\#178](https://github.com/SebRut/pygrocy/pull/178) ([SebRut](https://github.com/SebRut))
- update & fix tests for grocy 3.1.0 [\#177](https://github.com/SebRut/pygrocy/pull/177) ([SebRut](https://github.com/SebRut))
- Update responses requirement from ~=0.13.3 to ~=0.13.4 [\#173](https://github.com/SebRut/pygrocy/pull/173) ([dependabot[bot]](https://github.com/apps/dependabot))
- Update iso8601 requirement from ~=0.1.14 to ~=0.1.16 [\#171](https://github.com/SebRut/pygrocy/pull/171) ([dependabot[bot]](https://github.com/apps/dependabot))
- switch from general requests logging to custom http logging events [\#169](https://github.com/SebRut/pygrocy/pull/169) ([SebRut](https://github.com/SebRut))
- add basic request/response logging capability [\#168](https://github.com/SebRut/pygrocy/pull/168) ([SebRut](https://github.com/SebRut))
- Upgrade to GitHub-native Dependabot [\#166](https://github.com/SebRut/pygrocy/pull/166) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update responses requirement from ~=0.13.2 to ~=0.13.3 [\#165](https://github.com/SebRut/pygrocy/pull/165) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update responses requirement from ~=0.13.1 to ~=0.13.2 [\#164](https://github.com/SebRut/pygrocy/pull/164) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- add tojson helper method [\#163](https://github.com/SebRut/pygrocy/pull/163) ([SebRut](https://github.com/SebRut))
- Update responses requirement from ~=0.13.0 to ~=0.13.1 [\#162](https://github.com/SebRut/pygrocy/pull/162) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update responses requirement from ~=0.12.1 to ~=0.13.0 [\#161](https://github.com/SebRut/pygrocy/pull/161) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))

## [v0.29.0](https://github.com/SebRut/pygrocy/tree/v0.29.0) (2021-03-03)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.28.0...v0.29.0)

**Closed issues:**

- 404 errors and unresponsive sensors after configuring integration in HA [\#154](https://github.com/SebRut/pygrocy/issues/154)

**Merged pull requests:**

- add all\_products method [\#157](https://github.com/SebRut/pygrocy/pull/157) ([SebRut](https://github.com/SebRut))
- add support for generic objcts [\#156](https://github.com/SebRut/pygrocy/pull/156) ([SebRut](https://github.com/SebRut))

## [v0.28.0](https://github.com/SebRut/pygrocy/tree/v0.28.0) (2021-02-20)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.27.0...v0.28.0)

**Implemented enhancements:**

- Better error messages [\#133](https://github.com/SebRut/pygrocy/issues/133)

**Closed issues:**

- Support for Grocy 3.x api [\#145](https://github.com/SebRut/pygrocy/issues/145)

**Merged pull requests:**

- better error handling [\#153](https://github.com/SebRut/pygrocy/pull/153) ([SebRut](https://github.com/SebRut))
- add python 3.6 to tox config [\#152](https://github.com/SebRut/pygrocy/pull/152) ([SebRut](https://github.com/SebRut))
- add python 3.6 to tox config [\#151](https://github.com/SebRut/pygrocy/pull/151) ([SebRut](https://github.com/SebRut))

## [v0.27.0](https://github.com/SebRut/pygrocy/tree/v0.27.0) (2021-02-15)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.26.0...v0.27.0)

**Merged pull requests:**

- add tests for meal plan && change MealItem to only fetch recipe when … [\#150](https://github.com/SebRut/pygrocy/pull/150) ([SebRut](https://github.com/SebRut))
- fix error if product has no barcodes [\#149](https://github.com/SebRut/pygrocy/pull/149) ([SebRut](https://github.com/SebRut))

## [v0.26.0](https://github.com/SebRut/pygrocy/tree/v0.26.0) (2021-02-13)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.25.0...v0.26.0)

**Implemented enhancements:**

- add support for batteries [\#127](https://github.com/SebRut/pygrocy/issues/127)
- Test data model changes [\#77](https://github.com/SebRut/pygrocy/issues/77)

**Closed issues:**

- make data used in docker grocy instance testing consistent [\#94](https://github.com/SebRut/pygrocy/issues/94)

**Merged pull requests:**

- add batteries support [\#148](https://github.com/SebRut/pygrocy/pull/148) ([SebRut](https://github.com/SebRut))

## [v0.25.0](https://github.com/SebRut/pygrocy/tree/v0.25.0) (2021-02-10)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.24.1...v0.25.0)

**Merged pull requests:**

- Grocy 3.0.0+ support [\#146](https://github.com/SebRut/pygrocy/pull/146) ([SebRut](https://github.com/SebRut))
- Update iso8601 requirement from ~=0.1.13 to ~=0.1.14 [\#144](https://github.com/SebRut/pygrocy/pull/144) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- use tox [\#143](https://github.com/SebRut/pygrocy/pull/143) ([SebRut](https://github.com/SebRut))
- Update coveralls requirement from ~=2.1.2 to ~=3.0.0 [\#142](https://github.com/SebRut/pygrocy/pull/142) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Update pdoc3 requirement from ~=0.9.1 to ~=0.9.2 [\#141](https://github.com/SebRut/pygrocy/pull/141) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))

## [v0.24.1](https://github.com/SebRut/pygrocy/tree/v0.24.1) (2020-11-16)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.24.0...v0.24.1)

**Merged pull requests:**

- upgrade travis ci to python3.8 [\#139](https://github.com/SebRut/pygrocy/pull/139) ([SebRut](https://github.com/SebRut))
- Update responses requirement from ~=0.12.0 to ~=0.12.1 [\#138](https://github.com/SebRut/pygrocy/pull/138) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))

## [v0.24.0](https://github.com/SebRut/pygrocy/tree/v0.24.0) (2020-11-16)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.23.0...v0.24.0)

**Implemented enhancements:**

- Add "yearly" PeriodType [\#137](https://github.com/SebRut/pygrocy/pull/137) ([mdallaire](https://github.com/mdallaire))

**Closed issues:**

- Dependabot couldn't authenticate with https://pypi.python.org/simple/ [\#134](https://github.com/SebRut/pygrocy/issues/134)
- Split up main file [\#110](https://github.com/SebRut/pygrocy/issues/110)

**Merged pull requests:**

- Fix example [\#136](https://github.com/SebRut/pygrocy/pull/136) ([basxto](https://github.com/basxto))
- split up the main file [\#135](https://github.com/SebRut/pygrocy/pull/135) ([yellalena](https://github.com/yellalena))

## [v0.23.0](https://github.com/SebRut/pygrocy/tree/v0.23.0) (2020-09-11)

[Full Changelog](https://github.com/SebRut/pygrocy/compare/v0.22.0...v0.23.0)

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
- Update responses requirement from ~=0.10.15 to ~=0.10.16 [\#107](https://github.com/SebRut/pygrocy/pull/107) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))

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
