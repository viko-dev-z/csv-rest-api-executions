from github import GitHub
import math

# Endpoint: GET  https://api.github.com/users/<CSV_Data>
#

gh = GitHub(filename='get_users.csv')

users = []
endpoint = []

required_fields = []
optional_fields = []


def read_user_row(i=0):
    if gh.data['Execution Results'][i] == '':

        if gh.data['Name'][i] == '':  #row 9  will fail
            print("Name should be populated in CSV")
            exit(0)
        else:
            endpoint.append(gh.data['Name'][i])

        user = {}

        for field in required_fields:
            try:
                if gh.data[field][i] != '':
                    user[field] = gh.data[field][i]
                else:
                    print(user[field] + "should be populated in CSV")
                    exit(0)
            except AttributeError:
                pass
            except KeyError:
                pass

        for field in optional_fields:
            try:
                if gh.data[field][i] != '':
                    user[field] = gh.data[field][i]
            except AttributeError:
                pass
            except KeyError:
                pass

        users.append({
            "endpoint": endpoint,
            "data": user,
            "rows": [i]
        })

        print('Reading CSV row: #' + str(i) )
        # if this was the last entry, proceed to create the requests from the build array
        i = i + 1
        if i == gh.total_records + 1:
            gh.get_users(payload=users)
        else:
            read_user_row(i)

    else:
        print('skipping successful row')
        i = i + 1
        # if this was the last entry, proceed to create the requests from the build array
        if i == gh.total_records + 1:
            gh.get_users(payload=users)
        else:
            # continue
            read_user_row(i)
    return

read_user_row()
