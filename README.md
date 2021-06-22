## What is this

`mr` is command line client for Jenkins, with just the ability to _configure_ and start builds remotely. 

This tools makes sense when you have _parametrized_ jobs that you are manually starting from Jenkins' UI, which is error-prone and tedious (unless you like checklists).

#### Features (so far)

- starts a build from the command line
- prints link when the build starts
- overrides parameters from the command line
- uses local configuration ([sample](mr.toml)), which you can check into version control
- stores credentials securely (i.e. keychain on macOS)
- no need to fire up the browser
- can customize SSL certificates (useful in a corporate environment)

#### Limitations (so far)

- supports only parametrized pipelines
- only tested on macOS, but should work on Windows and Linux too


## Installation

There is no PYPi package yet.

Installation from source (needs `Python 3` and [poetry](https://github.com/python-poetry/poetry)):

1. clone this repo
2. run `poetry build`
3. install with `python3 -m pip dist/WHEEL_FILE_NAME`

## Usage

1. get a personal access token for your Jenkins server
2. add a corresponding server in the configuration file
3. add one or more tasks for the server in the configuration file
4. run `mr start YOUR_TASK_NAME`

`mr` will look up your credentials in the keychain, and start the build. If your credentials are not in the keychain already, `mr` will ask you to enter your token and then save it.


## Work in progress

Features:

- option to override the user name (--user)
- catch ctrl-c
- option to wait for build completion (polling for feedback)

Tech debt:

- use objects instead of dictionaries for configuration

