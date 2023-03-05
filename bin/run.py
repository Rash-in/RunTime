#!/usr/bin/env python3

import os, sys, argparse, json
from typing import Union

# Keep raised errors to just error message, not stack trace.
sys.tracebacklimit = 0

# -------------------- Script Arguments Setup and Parsing -------------------- #
parser = argparse.ArgumentParser(
    prog='run.py',
    description='Runs downstream applications passing the dotenv_path as an argument',
    epilog='''---'''
)
parser.add_argument('-a', '--application', type=str, required=True, help='Application name created from setup.py as listed in app.json')
args = parser.parse_args()
application = args.application
# ---------------------------------------------------------------------------- #

def get_application_data(filename='app.json') -> list:
    try:
        file_data = open(filename)
    except RuntimeError as Err:
        raise RuntimeError(Err)
    else:
        application_data = json.load(file_data)
    return application_data['applications']

def validate_app_name(app:str) -> Union[bool, list | None]:
    valid = False; app_data = {}
    application_data = get_application_data()
    for application in application_data:
        if application['app_name'] == app:
            valid = True; app_data = application
    return valid, app_data

# ------------------------------ SCRIPT RUNTIME ------------------------------ #
def main(application):
    isAppValid, app_data = validate_app_name(app=application)
    if not isAppValid:
        raise ValueError(f"App Name Not Found: {application}")
    
    app_path = app_data['app_path']
    dotenv_path = app_data['dotenv_path']
    
    try:
        os.system(f"python3 -B {app_path} -d {dotenv_path} >&1")
    except RuntimeError as Err:
        raise RuntimeError(Err)
    else:
        quit(1)

if __name__ == "__main__":
    main(application=application)
# ---------------------------------------------------------------------------- #

# EOF