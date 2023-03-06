import os, sys, argparse, json

# Keep raised errors to just error message, not stack trace.
sys.tracebacklimit = 0

# ---------------- Control Arguments in Command Line Execution --------------- #
parser = argparse.ArgumentParser(
    prog='setup.py',
    description='Setup for application name and path to be put into a json file.',
    epilog='''---'''
)
#parser.add_argument('-n', '--name', type=str, required=True, help='Application name. lowercase and hypen used as a word seperator.')
#parser.add_argument('-r', '--repo_path', type=str, required=True, help='Path to the repo where the app is being housed.')
#parser.add_argument('-d', '--dotenv_path', type=str, required=True, help='Path name to a dotenv file.')
#parser.add_argument('-a', '--app_path', type=str, required=True, help='Path to the application file to be run.')
#parser.add_argument('-s', '--start_path', type=str, required=True, help='Path to the Start script for the application to start server.')
#parser.add_argument('-p', '--activate_path', type=str, required=True, help='Path to the activate executable in the virtual environment for the app.')
#args = parser.parse_args()
#raw_values = {
#    "app_name": args.name,              #-n
#    "repo_path":args.repo_path,         #-r
#    "dotenv_path": args.dotenv_path,    #-d 
#    "app_path": args.app_path,          #-a
#    "start_path":args.start_path,       #-s
#    "activate_path":args.activate_path, #-p
#}
# ---------------------------------------------------------------------------- #

#Values need to be same order as raw_values for str validation check
default_data = {"valid": False, "msg":"", "values":{"app_name":None, "repo_path":None , "dotenv_path":None, "app_path":None , "start_path":None, "activate_path":None}}

def validate_arguments(raw_values:dict) -> dict:
    '''Takes argparse arguments, validates, and returns acceptable values in a dict'''
    data = default_data
    
    raw_app_name = raw_values['app_name']
    raw_repo_path = raw_values['repo_path']
    raw_dotenv_path = raw_values['dotenv_path']
    raw_app_path = raw_values['app_path']
    raw_start_path = raw_values['start_path']
    raw_activate_path = raw_values['activate_path']
    
    if not os.path.exists(raw_repo_path):
        data['msg'] = f"Repo Path does not exist: {raw_repo_path}"
    elif not os.path.exists(raw_dotenv_path):
        data['msg'] = f"Dot Env Path does not exist: {raw_dotenv_path}"
    elif not os.path.exists(raw_app_path):
        data['msg'] = f"App Path does not exist: {raw_app_path}"
    elif not os.path.exists(raw_start_path):
        data['msg'] = f"Activation Path does not exist: {raw_start_path}"
    elif not os.path.exists(raw_activate_path):
        data['msg'] = f"Activation Path does not exist: {raw_activate_path}"
    else:
        data['valid'] = True; data['msg'] = "valid"
        data['values']['app_name'] = raw_app_name
        data['values']['repo_path'] = raw_repo_path
        data['values']['dotenv_path'] = raw_dotenv_path
        data['values']['app_path'] = raw_app_path
        data['values']['start_path'] = raw_start_path
        data['values']['activate_path'] = raw_activate_path
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
            str_json = str(app); str_values = str(values)
            if str_json == str_values:
                file_data.close()
                return True, "JSON data loaded successfully."
        return False, f"Application data is not loaded successfully. Something went wrong.\n {app}"

def get_input():
    print("#### SETUP.PY ####")
    print("\nNOTE: This will only be used to clone a repo. Token is not stored anywhere but in setup.py memory.\nIt's cleaned up via garbage collection when the setup.py script ends.")
    github_pat = input("\nPaste your github personal access token: ")
    github_user = input("\nEnter your Github User Name: ")

    print("\nEnter the name associated with the Repo.\n  -- i.e. if git code url is this: https://github.com/Fake-user/fake-app.git\n  -- enter: Fake-user\n")
    github_repo_user = input("Enter the Git code repo user: ")

    print("\nEnter the repo name that appears after the user.\n i.e. if the git code url is this: https://github.com/Fake-user/fake-app.git\n enter: fake-app\n")
    github_app = input("Enter the Github App: ")

    print("\nEnter the path locally where you want to clone the repo.\nEnsure that the path currently exists and RunTime folder should exist in the same directory\n i.e.: /home/me/GitRepos\n")
    install_path = input("Enter in the path where you want to install a repo: ")
    runtime_folder = f"{install_path}/RunTime"
    if not os.path.exists(runtime_folder):
        msg = "RunTime folder not under same directory. Please check and re-enter"
    if not os.path.exists(install_path):
        msg = "Path doesn't exist. Please check and re-enter"
    while not os.path.exists(install_path):
        print(msg)
        install_path = input("Enter in the path where you want to install a repo: ")

    url = f'https://{github_user}:{github_pat}@github.com/{github_repo_user}/{github_app}.git'

    print("\nBelow are the details. Please look it over and accept/decline")
    print(f"\nGit Clone URL: {url}\nInstall Path: {install_path}\n")

    acceptance = input("Accept/Decline (y/n): ")
    yes = ['y', 'Y', 'Yes', 'YES']
    if acceptance not in yes:
        print("User did not accept. Quitting setup.py"); quit()

    git_data = {"url":url, "github_user": github_user,"github_pat": github_pat, "install_path": install_path}
    install_values = {
        "install_path":install_path,
        "repo_path": f"{install_path}/{github_app}",
        "venv_path": f"{install_path}/{github_app}/.env",
        "runtime_path": f"{install_path}/RunTime",
        "src_path": f"{install_path}/{github_app}/src",
        "bin_path": f"{install_path}/{github_app}/src/bin",
        "config_path":f"{install_path}/{github_app}/src/config",
        "tests_path":f"{install_path}/{github_app}/src/tests",
        "dotenv_file_path":f"{install_path}/RunTime/envs/{github_app}.env",
        "start_file_path":f"{install_path}/{github_app}/src/bin/local_start.py",
        "activate_file_path":f"{install_path}/{github_app}/.env/bin/activate"
    }

    return git_data, install_values

def validate_runtime_folder(git_data:dict):
    runtime_path = f"{git_data['install_path']}/RunTime"
    runtime_git_url = f"https://{git_data['github_user']}:{git_data['github_pat']}@github.com/Rash-in/RunTime.git"
    if not os.path.exists(runtime_path):
        print("RunTime repo not found. Installing using git data")
        try:
            os.system(f"cd {git_data['install_path']} && git clone {runtime_git_url} >&1")
            print("RunTime repo now cloned.")
            return True, "Clone Complete"
        except RuntimeError as Err:
            return False, f"Error cloning runtime repo: {Err}"
    return True, "RunTime repo found."

def install_repo():
    git_data, install_values = get_input()
    
    isRunTimeInstalled, runtime_msg = validate_runtime_folder(git_data)
    if not isRunTimeInstalled:
        return False, runtime_msg
    
    try:
        os.system(f"cd {install_values['install_path']} && git clone {git_data['url']} >&1")
    except RuntimeError as Err:
        return False, f"Error Installling Repo: {Err}", None

    #Manual Removal of sensitive information from memory once it is no longer needed.
    #The only remaining data that remains is inside your project folder inside .git/config used for git commands only.
    git_data = None
    del git_data
    
    print("Git user info overwritten as None and deleted")

    try:
        os.system(f"mkdir -p {install_values['src_path']} {install_values['bin_path']} {install_values['config_path']} {install_values['tests_path']} >&1")
    except RuntimeError as Err:
        return False, f"Error Creating app folders: {Err}", None

    try:
        os.system(f"touch {install_values['src_path']}/main.py && touch {install_values['repo_path']}/requirements.txt >&1")
    except RuntimeError as Err:
        return False, f"Error creating main.py: {Err}", None
    
    try:
        os.system(f"cd {install_values['repo_path']} && python3 -m venv .env >&1")
    except RuntimeError as Err:
        return False, f"Error creating python virtual environment: {Err}", None
    
    try:
        os.system(f"ln -s {install_values['runtime_path']} {install_values['venv_path']} >&1")
    except RuntimeError as Err:
        return False, f"Error linking RunTime folder to virtual environment: {Err}", None

    
    return True, "Install Complete", install_values

def main():
    '''Excution procedures for script.'''
    isInstalled, install_msg, install_values = install_repo()
    if not isInstalled:
        raise RuntimeError(install_msg)


if __name__ == "__main__":
    main()