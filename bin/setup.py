import os, sys, argparse, json

# Keep raised errors to just error message, not stack trace.
sys.tracebacklimit = 0

# ---------------- Control Arguments in Command Line Execution --------------- #
parser = argparse.ArgumentParser(
    prog='setup.py',
    description='Setup for application name and path to be put into a json file.',
    epilog='''---'''
)
allowed_frameworks =['django', 'fastapi', 'python_script']
parser.add_argument('-n', '--name', type=str, required=True, help='Application name. lowercase and hypen used as a word seperator.')
parser.add_argument('-d', '--dotenv_path', type=str, required=True, help='Path name to a dotenv file.')
parser.add_argument('-a', '--app_path', type=str, required=True, help='Path to the application file to be run.')
args = parser.parse_args()
app_name = args.name
dotenv_path = args.dotenv_path
app_path = args.app_path
# ---------------------------------------------------------------------------- #

def validate_arguments(raw_values:dict) -> dict:
    '''Takes argparse arguments, validates, and returns acceptable values in a dict'''
    raw_app_name = raw_values['app_name']
    raw_app_path = raw_values['app_path']
    raw_dotenv_path = raw_values['dotenv_path']
    
    data = {"valid": False, "msg":"", "values":{"app_name":None, "app_path":None , "dotenv_path":None}}
    if not os.path.exists(raw_dotenv_path):
        data['msg'] = f"Dot Env Path does not exist: {raw_dotenv_path}"
    elif not os.path.exists(raw_app_path):
        data['msg'] = f"App Path does not exist: {raw_app_path}"
    else:
        data['valid'] = True; data['msg'] = "valid"
        data['values']['app_name'] = raw_app_name.lower().replace("_", "-").replace(" ", "_")
        data['values']['app_path'] = raw_app_path
        data['values']['dotenv_path'] = raw_dotenv_path
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
            if app['app_name'] == values['app_name'] and app['dotenv_path'] == values['dotenv_path']:
                file_data.close()
                return True, "JSON data loaded successfully."
        return False, f"Application data is not loaded successfully. Something went wrong.\n {app}"

def main(raw_values:dict):
    '''Excution procedures for script.'''
    
    # Validate if arguments exist and are acceptable values
    argument_validation_data = validate_arguments(raw_values)
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
    values = {"app_name": app_name, "app_path": app_path, "dotenv_path": dotenv_path}
    main(raw_values=values)