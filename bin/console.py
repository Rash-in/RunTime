import os, argparse

from module.procedures_user.new_user import new_user_procedures
from module.procedures_user.remove_user import remove_user_procedures
from module.procedures_user.validate_user import validate_user_procedures
from module.procedures_app.new_app import new_app_procedures
from module.procedures_app.remove_app import remove_app_procedures
from module.procedures_app.resetup_app import resetup_app_procedures
from module.procedures_app.validate_app import validate_app_procedures
from module.procedures_install.install import install_runtime_procedures

BIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
MODULE_FOLDER = BIN_FOLDER + "/module"

allowed_actions = [
    'install_runtime',
    'new_user',
    'remove_user',
    'validate_user',
    'new_app',
    'remove_app',
    'resetup_app',
    'validate_app'
]


parser = argparse.ArgumentParser(
    prog='console.py',
    description='Console for RunTime app. RunTime is a global folder used to run applications with a dotenv file for new dev projects.',
    epilog='''---'''
)
parser.add_argument('-a','--action', choices=allowed_actions, help='Console action item.')
args = parser.parse_args()


def main():
    if args.action:
        match args.action:
            case 'install_runtime':
                valid, msg, data = install_runtime_procedures()
            case 'new_user':
                valid, msg, data = new_user_procedures()
            case 'remove_user':
                valid, msg, data = remove_user_procedures()
            case 'validate_user':
                valid, msg, data = validate_user_procedures()
            case 'new_app':
                valid, msg, data = new_app_procedures()
            case 'remove_app':
                valid, msg, data = remove_app_procedures()
            case 'resetup_app':
                valid, msg, data = resetup_app_procedures()
            case 'validate_app':
                valid, msg, data = validate_app_procedures()
            case _:
                print("Failsafe: No action provided. Quitting setup.py")
                quit(1)
        print(f"Setup Complete? {valid}")
        print(f"Setup Message: {msg}")
        print(f"Setup Data: {data}")
        quit(0)
    elif args.print_actions:
        print(allowed_actions)
        quit(0)
    else:
        print("oh noze i broked.")
        quit(1)

if __name__ == "__main__":
    main()