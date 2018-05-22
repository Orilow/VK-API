import requests
import argparse


def get_vk_info(name, token):
    info = None
    args = {
        'user_ids': name,
        'access_token': token,
        'fields': 'city, bdate, counters',
        'v': '5.76'
    }
    try:
        info = requests.get("https://api.vk.com/method/users.get", args)
    except requests.exceptions.SSLError as e:
        print("(SSLError):{0}".format(e))
    except requests.ConnectionError as e:
        print(e)
    return info


def get_token_from_file():
    with open("token.txt", "r", encoding="utf-8") as file:
        return file.read()


def get_auth_token(app_id):
    info = requests.get("https://oauth.vk.com/authorize?client_id={0}"
                        "&redirect_uri=https://oauth.vk.com/blank.html&scope=friends"
                        "&response_type=token&v=5.76&revoke=1".format(app_id))
    print(info.url)
    print(info.json())


if __name__ == '__main__':
    parcer = argparse.ArgumentParser()
    parcer.add_argument("name", help="user screen short name or ID")
    args = parcer.parse_args()
    if args.name:
        your_token = get_token_from_file()
        result = get_vk_info(args.name, your_token)
        print(result)