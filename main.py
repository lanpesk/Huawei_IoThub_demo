import json
import requests
import os
import time

cert_path = r"cert/client.crt"  # the two file maybe useless
key_path = r"cert/client.key"


def GetToken(username: str, password: str, domains: str, url: str, scope="cn-north-4"):
    '''
    get user IMA token by username and password, the params explains refer to:https://support.huaweicloud.com/api-iam/iam_30_0001.html
    :param username: IMA username
    :param password: IMA password
    :param domains:  which account that IMA subordinated
    :param url: requests destination
    :param scope: region the product in
    :return: the token
    '''

    header = {"Content-Type": "application/json;charset=utf8"}

    # the body json format
    body = {
        "auth": {
            "identity": {
                "methods": ["password"],  # use api : KeystoneCreateUserTokenByPassword
                "password": {
                    "user": {
                        "name": username,
                        "password": password,
                        "domain": {
                            "name": domains
                        }
                    }
                }
            },
            "scope": {
                "project": {
                    "name": scope
                }
            }
        }
    }

    body = json.dumps(body)
    response = requests.post(url, data=body, headers=header, cert=(cert_path, key_path))

    if response.status_code != 201:
        print(f"Get Token faild, status code: {response.status_code}")
        return

    token = response.headers["X-Subject-Token"]
    print("Get Token Successful")
    return token


def GetDeviceProperties(project_id: str, device_id: str, service_id: str, url: str, token: str):
    '''
    Get the specify device message
    :param project_id: the device project id,refer to https://support.huaweicloud.com/api-iothub/iot_06_v5_1001.html
    :param device_id: the device id, you can get in your huawei clound console
    :param service_id: the product that devices combine, this is in your product schema.
    :param url: iot interface url, refer to https://support.huaweicloud.com/devg-iothub/iot_02_1004.html
    :param token: the user token
    :return: if success, return message.
    '''

    header = {"Content-Type": "application/json;charset=utf8", "X-Auth-Token": token}
    uri = f"/v5/iot/{project_id}/devices/{device_id}/properties?service_id={service_id}"
    url += uri

    response = requests.get(url, headers=header, cert=(cert_path, key_path))

    if response.status_code != 200:
        print(f"Get Device Properties faild, status code {response.status_code}, plesae check.")
        print(response.text)
        return

    return response.text


def ShowDeviceList(project_id: str, url: str, token):
    '''
    return the devices list, refer to https://support.huaweicloud.com/api-iothub/iot_06_v5_0048.html
    :param project_id: the device project id,refer to https://support.huaweicloud.com/api-iothub/iot_06_v5_1001.html
    :param url: iot interface url, refer to https://support.huaweicloud.com/devg-iothub/iot_02_1004.html
    :return: if success, return devices detail list
    '''

    header = {"Content-Type": "application/json;charset=utf8", "X-Auth-Token": token}
    url += f"/v5/iot/{project_id}/devices"

    response = requests.get(url, headers=header, cert=(cert_path, key_path))

    if response.status_code != 200:
        print(f"Get Device list error, please check, response code {response.status_code}")
        print(response.text)
        return

    return response.text


def CreateDeviceCommand(project_id: str, device_id: str, url: str, token, service_id: str, command_name: str,
                        paras: dict):
    '''
    Create a command ,and send to device.
    :param project_id: the device project id,refer to https://support.huaweicloud.com/api-iothub/iot_06_v5_1001.html
    :param device_id: the device id, you can get in your huawei clound console
    :param url: iot interface url, refer to https://support.huaweicloud.com/devg-iothub/iot_02_1004.html
    :param token: user token
    :param service_id: the product that devices combine, this is in your product schema.
    :param command_name: the command name in your product
    :param paras: command's params
    :return: true, if sccuess
    '''

    header = {"Content-Type": "application/json;charset=utf8", "X-Auth-Token": token}
    url += f"/v5/iot/{project_id}/devices/{device_id}/commands"

    body = {
        "service_id": service_id,
        "command_name": command_name,
        "paras": paras
    }
    body = json.dumps(body)

    response = requests.post(url, data=body, headers=header, cert=(cert_path, key_path))

    if response.status_code != 200:
        print(f"Create command error, status code {response.status_code}, please check")
        print(response.text)
        return

    print(f"Command release successful!")
    return response.text


if __name__ == "__main__":

    # token fetch
    newToken = False
    if os.path.exists(r"token"):
        if time.time() - os.path.getmtime(r"token") >= 24 * 60 * 60:  # the token vaild until 24h
            print("The exist token is expired, fetch new token?(yes/no)\n>")
            if input() == "yes":
                newToken = True
        else:
            print("The token is in force, no token need fetched.")
    else:
        print("no token file find, fetch new token?(yes/no)\n>")
        if input() == "yes":
            newToken = True
        else:
            with open(r"token", "w") as fp:  # create a blank file
                pass

    IMA_username = "..."
    IMA_password = "..."
    domain_user = "..."
    token_access_point = "..."

    if newToken:
        token = GetToken(IMA_username, IMA_password, domain_user, token_access_point)
        print("Writing new token...")
        with open(r"token", "w") as fp:
            fp.write(token)
        print("Writing done.")
    else:
        print("Reading token...")
        token = open(r"token", "rb").read().decode("utf-8")
        print("Reading token done.")

    # the main interface
    interface = "1. show the devices list\n" \
                "2. get Device Properties\n" \
                "3. create Device Command\n" \
                "4. get a new token\n" \
                "5. exit"

    project_id = "..."
    device_id = "..."
    iot_app_access_point = "..."
    service_id = "..."

    command_names = []  # not implement

    # "message" loop
    while True:
        print(interface)
        choice = input(">")

        if choice == "1":
            res = ShowDeviceList(project_id, iot_app_access_point, token)
            print(json.dumps(json.loads(res), indent=4, separators=(
            ',', ':')))  # this is just a showing, you can add more process using the response res

        if choice == "2":
            res = GetDeviceProperties(project_id, device_id, service_id, iot_app_access_point, token)
            print(json.dumps(json.loads(res), indent=4, separators=(',', ':')))

        if choice == "3":
            res = CreateDeviceCommand(project_id, device_id, iot_app_access_point, token, service_id,
                                      input("input the command name:\n>"),
                                      paras=eval(input("input the command params:(in dict format)\n>")))
            # the paras format like : {"value":10, "type":"switch"}
            print(json.dumps(json.loads(res), indent=4, separators=(',', ':')))

        if choice == "4":
            token = GetToken(IMA_username, IMA_password, domain_user, token_access_point)
            print("Writing new token...")
            with open(r"token", "w") as fp:
                fp.write(token)
            print("Writing done.")

        if choice == "5":
            exit(0)
