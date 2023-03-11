import argparse, json
from typing import Union

from .validate_user import validate_user_procedures



def retrieve_input() -> Union[bool, str, dict|None]:
    print("# ---------------------------------------------------------------------------- #")
    print("# ---------------------------- NEW USER PROCEDURES --------------------------- #")
    print("# ---------------------------------------------------------------------------- #")
    
    github_user = input("\nEnter your Github username: ")
    github_pat = input("\nEnter your Github personal access token: ")

    user_values = {
        "github_user": github_user,
        "github_pat": github_pat
    }
    print(json.dumps(user_values, indent=4))

    acceptance = input("\nAccept (y/n): ")
    yes = ['y', 'Y', 'Yes', 'YES']
    if acceptance not in yes:
        return False, "User declined acceptance", None
    else:
        return True, "User accepted values", user_values

def new_user_procedures(user:str=False, pat:str=False):
    '''Used if function is imported.'''
    if not user or not pat:
        isUserInput, user_input_msg, user_data = retrieve_input()
        if not isUserInput:
            return isUserInput, user_input_msg, user_data
    else:
        user_data = {"github_user": user, "github_pat": pat}
    
    isValid, valid_msg, validated_data = validate_user_procedures(user_data=user_data)
    if not isValid:
        return isValid, valid_msg, validated_data

    valid_user = validated_data['valid_user']; valid_pat = validated_data['valid_pat']
    return True, "Validation Successful", {'valid_user':valid_user, "valid_pat": valid_pat}
    
    #isProceduresComplete = False; procedures_msg = "I am a return message for new_user_procedures"
    #return  isProceduresComplete, procedures_msg

def main():
    '''Used if file is called directly'''
    
    parser = argparse.ArgumentParser(
        prog='new_user.py',
        description='Procedures to setup a new user.',
        epilog='''---'''
    )
    parser.add_argument('-u', '--github_user', type=str, required=True, help='Github Username')
    parser.add_argument('-p', '--github_pat', type=str, required=True, help='Github Personal Access Token')
    args = parser.parse_args()
    user = args.github_user
    pat = args.github_pat
        
    isProceduresComplete, procedures_msg, user_data = new_user_procedures(user=user, pat=pat)
    print(f"{isProceduresComplete} / {procedures_msg} / {user_data}")
    quit()

if __name__ == "__main__":
    main()