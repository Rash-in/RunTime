import argparse



def resetup_app_procedures():
    '''Used if function is imported.'''

def main():
    '''Used if file is called directly'''
    
    parser = argparse.ArgumentParser(
        prog='resetup_app.py',
        description='Procedures to remove an installed app.',
        epilog='''---'''
    )
    parser.add_argument('-a', '--app_name', type=str, required=True, help='Name of the existing application to be installed.')
    parser.add_argument('-u', '--github_user', type=str, required=True, help='User name that setup has created previously (github_user)')
    args = parser.parse_args()
    app_name = args.app_name
    github_user = args.github_user

if __name__ == "__main__":
    main()