"""
Captive-requests: v0.1
This is a script to automate login to captive portals of my university

author: ashknl
"""

import subprocess
import socket
import re
import sys
import os
import requests
from requests import adapters
from urllib3.poolmanager import PoolManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


# # from https://github.com/encode/httpx/discussions/2635
# class InterfaceAdapter(adapters.HTTPAdapter):

#     def __init__(self, **kwargs):
#         self.iface = kwargs.pop("iface", None)
#         super(InterfaceAdapter, self).__init__(**kwargs)

#     def _socket_options(self):
#         if self.iface is None:
#             return []
#         else:
#             return [(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.iface)]

#     def init_poolmanager(self, connections, maxsize, block=False):
#         self.poolmanager = PoolManager(
#             num_pools=connections,
#             maxsize=maxsize,
#             block=block,
#             socket_options=self._socket_options(),
#         )


# def get_iface_connected_to_ssid(ssid_name: str) -> str | None:
#     try:
#         proc = subprocess.Popen(
#             ["iwconfig"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
#         )
#         (out, err) = proc.communicate()
#         out = out.decode("utf-8")

#         # parse each line for ssid
#         for line in out.split("\n"):
#             match = re.search(f'ESSID:"{ssid_name}"', line)
#             if match:
#                 return line.split(" ")[0]

#     except ChildProcessError:
#         print("error occured", ChildProcessError.strerror)
#         return


# def is_logged_out(session):
#     response = session.get("http://neverssl.com", verify=False).text

#     if response.find("https://172.19.16.1:1003/fgtauth") != -1:
#         return True


# def run():
#     iface = get_iface_connected_to_ssid("NIST-Boys-Hostel")
#     print(iface)

#     URL = "https://172.19.16.1:1003/"

#     session = requests.Session()
#     for prefix in ("http://", "https://"):
#         # set ETH999 interface here
#         session.mount(prefix, InterfaceAdapter(iface=iface.encode("utf-8`")))

#     if is_logged_out(session):
#         text = session.get(f"{URL}login?69696969", verify=False).text

#         soup = BeautifulSoup(text, "html.parser")
#         redirect_url = soup.find("input", attrs={"name": "4Tredir"})
#         magic = soup.find("input", attrs={"name": "magic"})

#         data = {
#             "4Tredir": redirect_url["value"],
#             "magic": magic["value"],
#             "username": os.environ.get("WIFIUSERNAME"),
#             "password": os.environ.get("PASSWORD"),
#         }

#         print(data)

#         print(f"making login request with magic {magic['value']}")
#         response = session.post(
#             URL,
#             data=data,
#             headers={
#                 "Content-Type": "application/x-www-form-urlencoded",
#                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
#                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             },
#             verify=False,
#         )

#         # verify login
#         if not is_logged_out(session) and response.status_code == 200:
#             print("Logged in successfully")
#         else:
#             print("Could not login. Error")

#     else:
#         print("Already Logged in...")


# run()


# check if connected to internet. connectivity-check.ubuntu.com returns a 0 length response if connected to internet
def is_connected() -> bool:
    r = requests.get("http://connectivity-check.ubuntu.com")
    if len(r.text) == 0:
        return True

    return False


# get captive_portal_url
def get_portal_url() -> str:
    r = requests.get("http://connectivity-check.ubuntu.com")
    text = r.text
    portal_url = re.search("https://172.19.16.1:1003/.*;", text).group()

    portal_url = portal_url[: len(portal_url) - 2]

    return portal_url


# get magic token from portal
def get_request_data(portal_url: str) -> dict:
    r = requests.get(portal_url, verify=False)
    text = r.text

    soup = BeautifulSoup(text, "html.parser")
    redirect_url = soup.find("input", attrs={"name": "4Tredir"})
    magic = soup.find("input", attrs={"name": "magic"})

    data = {
        "4Tredir": redirect_url["value"],
        "magic": magic["value"],
        "username": os.environ.get("WIFIUSERNAME"),
        "password": os.environ.get("PASSWORD"),
    }

    return data


def make_login_request(request_data: dict) -> int:
    URL = "https://172.19.16.1:1003/"

    response = requests.post(
        URL,
        data=request_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        verify=False,
    )

    return response.status_code


def login():
    try:
        print("checking if connected....")

        if is_connected():
            print("Already connected. Exiting!")
            return
        else:
            print("Getting portal url....")
            # get portal url
            portal_url = get_portal_url()

            request_data = get_request_data(portal_url=portal_url)

            login_status = make_login_request(request_data=request_data)

            print(login_status)
            print("connected to internet?", is_connected())

    except requests.ConnectionError:
        print("Conneciton Error. Check wifi connection")


def logout():
    r = requests.get("https://172.19.16.1:1003/logout?1234",verify=False)
    print("Logged out.....")


def main():
    if len(sys.argv) < 2:
        print("give login or logout commands")

    else:
        command = sys.argv[1]
        if command == "login":
            login()
        
        if command == "logout":
            logout()


main()
