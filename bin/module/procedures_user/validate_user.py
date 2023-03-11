import argparse
from typing import Union

def validate_user_procedures(user_data:dict) -> Union[bool, str]:
    '''Used if function is imported. Returns whether it is complete and a message'''
    if not user_data or user_data is None:
        return False, "Validation: No user_data provided", None
    elif not user_data['github_user'] or not user_data['github_pat']:
        return False, "Validation: user_data does not contain either github_user or github_pat keys.", None
    else:
        return True, "Validation Successful", {'valid_user':user_data['github_user'], 'valid_pat':user_data['github_pat']}

def main():
    '''Used if file is called directly'''
    
    parser = argparse.ArgumentParser(
        prog='validate_user.py',
        description='Procedures to validate an installed user.',
        epilog='''---'''
    )
    parser.add_argument('-u', '--github_user', type=str, required=True, help='Github Username')
    parser.add_argument('-p', '--github_pat', type=str, required=True, help='Github Personal Access Token')
    args = parser.parse_args()
    user = args.github_user
    pat = args.github_pat
    
    user_data = { "github_user": user, "github_pat": pat}
    isProceduresComplete, procedures_msg, user_data = validate_user_procedures(user_data)
    print(f"{isProceduresComplete} / {procedures_msg} / {user_data}")
    quit()

if __name__ == "__main__":
    main()