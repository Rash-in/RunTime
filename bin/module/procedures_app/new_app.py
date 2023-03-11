import argparse



def new_app_procedures():
    '''Used if function is imported.'''

def main():
    '''Used if file is called directly'''
    
    parser = argparse.ArgumentParser(
        prog='new_app.py',
        description='Procedures to setup a new app.',
        epilog='''---'''
    )
    parser.add_argument('-a', '--app_name', type=str, required=True, help='Name of the application to be installed.')
    parser.add_argument('-u', '--github_user', type=str, required=True, help='Github user that has been already installed.')
    parser.add_argument('-c', '--common_install_path', type=str, required=True, help='Local command path that exists where github repos normally get installed to.')
    args = parser.parse_args()
    app_name=args.app_name
    user=args.github_user
    common_install_path = args.common_install_path

if __name__ == "__main__":
    main()