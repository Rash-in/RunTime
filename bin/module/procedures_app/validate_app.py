import argparse


def validate_app_procedures():
    '''Used if function is imported.'''

def main():
    '''Used if file is called directly'''
    
    parser = argparse.ArgumentParser(
        prog='validate_app.py',
        description='Procedures to validate an installed application',
        epilog='''---'''
    )
    parser.add_argument('-a', '--app_name', type=str, required=True, help='Name of the application to be installed.')
    args = parser.parse_args()
    app_name = args.app_name


if __name__ == "__main__":
    main()