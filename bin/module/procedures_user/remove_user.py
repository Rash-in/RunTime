import argparse



def remove_user_procedures():
    '''Used if function is imported.'''

def main():
    '''Used if file is called directly'''
    
    parser = argparse.ArgumentParser(
        prog='remove_user.py',
        description='Procedures to remove an installed user.',
        epilog='''---'''
    )
    parser.add_argument('-u', '--github_user', type=str, required=True, help='Github username as listed in Github')
    args = parser.parse_args()
    user = args.github_user
    
    

if __name__ == "__main__":
    main()