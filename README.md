
# PrairieLearn

PrairieLearn is an online problem-driven learning system. It consists
of a server component that presents questions and other data via an
API, and a web-app that interfaces with the user and communicates with
the server.

## User Documentation

* [Overview](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/overview.md)
* [Installing and running PrairieLearn on Linux or OS X](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/installingLinux.md)
* [Installing and running PrairieLearn on Windows](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/installingWindows.md)
* [PrairieLearn server configuration](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/serverConfig.md)
* [Course configuration](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/courseConfig.md)
* [Writing questions](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/writingQuestions.md)
* [Writing tests](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/writingTests.md)
* [Syncing with GitHub](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/sync.md)

## Developer Documentation

* [Development notes](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/devNotes.md)
* [Client/server API](https://github.com/PrairieLearn/PrairieLearn/blob/master/doc/api.md)

## ChangeLog

* __1.3.2__ - 2015-08-24

  * Fix `allowAccess` checks to not always fail.

* __1.3.1__ - 2015-08-24

  * Fix `pulls` error when `gitCourseBranch` is not set.

* __1.3.0__ - 2015-08-24

  * Change default `allowAccess` to block all non-instructor access.

* __1.2.1__ - 2015-08-24

  * Fix race condition in user creation and correctly record user names.

* __1.2.0__ - 2015-08-23

  * Add "Sync" feature to pull from a git repository.

  * Fix missing `template` field in `config.json` schema.

  * Improve error logging with more specific error information.

* __1.1.0__ - 2015-08-22

  * Add access logging to the database.

* __1.0.2__ - 2015-08-19

  * Documentation fixes following the bootcamp.

  * Fix undefined logger error if `config.json` contains errors (reported by Craig and Mariana).

* __1.0.1__ - 2015-08-18

  * Fix `npm` module list during bootcamp (remove `nodetime`, add `moment`).

* __1.0.0__ - 2015-08-18

  * First public release for pre-Fall-2015 bootcamp.
