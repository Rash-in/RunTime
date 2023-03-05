# RunTime
This repo contains a folder structure and common scripts used for local development for multiple projects.

I personally manage a few projects that are similar in setup. Each using a common dotenv, logs, pids, certs location. I found that it was tedious to keep setting up new projects. This repo is the automation to keep that to a minimum.

## How-To Overview
Once cloned in a common location for git repositories. go into an existing project and symlink the repo folder `RunTime` into the .env/venv python virtual environment folder.

Example location of Runtime: `/home/me/GitRepos/RunTime`
Example location of a project: `/home/me/GitRepos/SUPERPROJECT`

`ln -s /home/me/GitRepos/RunTime/ /home/me/GitRepos/SUPERPROJECT/.env/`

In your IDE you should be able to see the new folder mapped inside the .env folder

## Getting Started
Once the repo is cloned and symlinked to the virtual environment folder:
**Change anything in all caps to whatyou call it.**
1) `cd /path/to/RunTime`
2) `touch envs/APPNAME.env`
3) `python3 -n app-name -p /path/to/RunTime/envs/APPNAME.env -f FRAMEWORK_NAME`
    - Allowed values for FRAMEWORK_NAME are - `django`, `fastapi`, `python_script`

4) `python3 -B run.py -a APPNAME`

## What Setup Does
it takes in the arguments for app name, path to app, and framework and validates the values,
- app_name: lowercase, uses hypens for word seperation. It replaces characters based on that.
- dotenv_path: verifies that the path/file exists

After validation, it writes to `app.json` and appends the three values to the `applications` list.

## What Run Does
Reads the application json and executes the application command with the dotenv_path to the application of choice.

I code all my apps to assume local development if a dotenv_path is sent as an argument. If it doesn't pass that arg, then the assumption is that it follows the CI/CD pattern that createst the variables needed to process it.