import requests
import argparse
import json
import sys


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
        print("Something wrong with SSL. Try again later")
        sys.exit(1)
    except requests.ConnectionError as e:
        print("Something wrong with connection. Try again later")
        sys.exit(1)
    return info.json()


def get_token_from_file():
    with open("token.txt", "r", encoding="utf-8") as file:
        return file.read()


def get_auth_token(app_id):
    info = requests.get("https://oauth.vk.com/authorize?client_id={0}"
                        "&redirect_uri=https://oauth.vk.com/blank.html&scope=friends"
                        "&response_type=token&v=5.76&revoke=1".format(str(app_id)))
    print(info.url)


def get_mock_answer():
    with open("mock_responce.txt", "r", encoding="utf-8") as f:
        return json.load(f)

def rememver_response(resp):
    with open("mock_responce.txt", "w", encoding="utf-8") as f:
        json.dump(resp, f)



def handle_responce(raw_responce):
    result = "Here is user info I found: \n"
    result += "User ID: " + str(raw_responce["response"][0]["id"]) + "\n"
    result += "First_name: " + raw_responce["response"][0]["first_name"] + "\n"
    result += "Last Name: " + str(raw_responce["response"][0]["last_name"]) + "\n"
    result += "Birtday Date: " + raw_responce["response"][0]["bdate"] + "\n"
    result += "City: " + raw_responce["response"][0]["city"]["title"] + "\n"
    result += "Count of videos: " + str(raw_responce["response"][0]["counters"]["videos"]) + "\n"
    result += "Count of audios: " + str(raw_responce["response"][0]["counters"]["audios"]) + "\n"
    result += "Count of friends: " + str(raw_responce["response"][0]["counters"]["friends"]) + "\n"
    return result


if __name__ == '__main__':
    parcer = argparse.ArgumentParser()
    parcer.add_argument("name", help="user screen short name or ID")
    args = parcer.parse_args()
    #get_auth_token(6487258)
    if args.name:
        your_token = get_token_from_file()
        raw_response = get_vk_info(args.name, your_token)
        #remember_response(raw_response)
        # with open("mock_responce.txt", "w", encoding="utf-8") as f:
        #     json.dump(raw_responce, f)
        result = handle_responce(raw_response)
        print(result)
