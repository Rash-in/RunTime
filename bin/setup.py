import os, sys, argparse, json
from pathlib import Path

# Keep raised errors to just error message, not stack trace.
sys.tracebacklimit = 0



# ---------------- Control Arguments in Command Line Execution --------------- #
parser = argparse.ArgumentParser(
    prog='setup.py',
    description='Setup for application name and path to be put into a json file.',
    epilog='''---'''
)
allowed_frameworks =['django', 'fastapi', 'python_script']
parser.add_argument('-n', '--name', type=str, help='Application name. lowercase and hypen used as a word seperator.')
parser.add_argument('-p', '--path', type=str, help='Path name to a dotenv file.')
parser.add_argument('-f', '--framework', type=str, choices=allowed_frameworks , help='Framework that the application uses.')
args = parser.parse_args()
app_name = args.name
dotenv_path = args.path
framework = args.framework
# ---------------------------------------------------------------------------- #

def validate_arguments(app_name:str, dotenv_path:str, framework:str) -> dict:
    '''Takes argparse arguments, validates, and returns acceptable values in a dict'''
    data = {"valid": False, "msg":"", "values":{"app_name":None, "dotenv_path":None}}
    if not app_name:
        data['msg'] = f"Argument Missing: -n, --name: {app_name}"
    elif not dotenv_path:
        data['msg'] = f"Argument Missing: -p, --path: {dotenv_path}"
    elif not framework:
        data['msg'] = f"Argument Missing: -f, --framwork: {framework}"
    elif not os.path.exists(dotenv_path):
        data['msg'] = f"Dot Env Path does not exist: {dotenv_path}"
    else:
        data['valid'] = True; data['msg'] = "valid"
        data['values']['app_name'] = app_name.lower().replace("-", "_")
        data['values']['dotenv_path'] = dotenv_path
        data['values']['framework'] = framework
    return data

def write_to_json_file(values:dict, filename='app.json'):
    try:
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data['applications'].append(values)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        return True, "Application loaded."
    except RuntimeError as Err:
        return False, Err
    
def validate_json_contents(values:dict, filename='app.json'):
    try:
        file_data = open(filename)
        application_data = json.load(file_data)
    except RuntimeError as Err:
        file_data.close()
        return False, Err
    else:
        applications = application_data['applications']
        for app in applications:
            if app['app_name'] == values['app_name'] and app['dotenv_path'] == values['dotenv_path'] and app['framework'] == values['framework']:
                file_data.close()
                return True, "JSON data loaded successfully."
        return False, f"Application data is not loaded successfully. Something went wrong.\n {app}"

def main(app_name:str, dotenv_path:str, framework:str):
    '''Excution procedures for script.'''
    
    # Validate if arguments exist and are acceptable values
    argument_validation_data = validate_arguments(app_name=app_name, dotenv_path=dotenv_path, framework=framework)
    if not argument_validation_data['valid']:
        raise ValueError(f"ERROR: Argument(s) invalid. {argument_validation_data['msg']}")
    
    # Set valid values
    values = argument_validation_data['values']
    
    isJSONData, write_json_msg = write_to_json_file(values=values)
    if not isJSONData:
        raise RuntimeError(f"ERROR: {write_json_msg}")
        
    isJSONValid, json_valid_msg = validate_json_contents(values=values)
    if not isJSONValid:
        raise RuntimeError(f"ERROR: {json_valid_msg}")
    
    print(f"Script Completed: {json_valid_msg}"); quit()

if __name__ == "__main__":
    main(app_name=app_name, dotenv_path=dotenv_path, framework=framework)