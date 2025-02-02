import stdiomask
import os
import pickle


def user_input_data():
    return {'client_id': input('Reddit client_id: '),
            'Reddit client_secret': stdiomask.getpass('Reddit client_secret: '),
            'user_agent': 'daily-hamtaro by u/imrazsek-developer', 'username': input('Reddit Username: '),
            'password': stdiomask.getpass()}


def get_credentials():
    # Check previously auth.
    if os.path.exists('auth.pickle'):
        # Read auth file
        with open('auth.pickle', 'rb') as auth:
            credentials = pickle.load(auth)
    else:
        # User must introduce auth data.
        credentials = user_input_data()
        # Insert data to auth file for next execution.
        auth_file = open('auth.pickle', 'wb')
        pickle.dump(credentials, auth_file)

    return credentials
