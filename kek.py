# Hit run at the top!
# This program will not save your reddit login details.

## CONFIGURATION ##
center_x = 497
center_y = 414

radius = 9
###################

import math
import sys
import random
import time

import requests
from PIL import Image
from requests.adapters import HTTPAdapter

username = input("Username: ")
password = input("Password: ")


session = requests.Session()
session.mount('https://www.reddit.com', HTTPAdapter(max_retries=5))
session.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36"
response = session.post("https://www.reddit.com/api/login/{}".format(username), data={"user": username, "passwd": password, "api_type": "json"})
json = response.json()["json"]
if json["errors"]:
    print("Could not log in:", json["errors"])
    exit()
session.headers['x-modhash'] = json["data"]["modhash"]
print("Logged in with username {}".format(username))


def place_pixel(ax, ay):
    new_color = 0

    print("Checking pixel at {},{}. Target colour: {}".format(ax, ay, new_color))

    while True:
        response = session.get("http://reddit.com/api/place/pixel.json?x={}&y={}".format(ax, ay), timeout=5)
        if response.status_code == 200:
            data = response.json()
            break
        else:
            print("ERROR: ", response, response.text)
        time.sleep(5)

    old_color = data["color"] if "color" in data else 0
    if old_color == new_color:
        placed_by = data["user_name"] if "user_name" in data else "<nobody>"
        print("Pixel at {},{} is already empty (placed by {}), skipping".format(ax, ay, placed_by))
    else:
        print("Placing pixel colour {} at {},{}".format(new_color, ax, ay))
        r = session.post("https://www.reddit.com/api/place/draw.json",
                   data={"x": str(ax), "y": str(ay), "color": str(new_color)})

        secs = float(response.json()["wait_seconds"])
        if "error" not in response.json():
            print("Placed empty pixel! - waiting {} seconds".format(secs))
        else:
            print("Cooldown already active - waiting {} seconds".format(int(secs)))
        time.sleep(secs + 2)

        if "error" in response.json():
            place_pixel(ax, ay)


while True:
    x = random.randint(center_x - radius, center_x + radius)
    y = random.randint(center_y - radius, center_y + radius)

    # Reject coordinates outside the circle
    if math.hypot(x - center_x, y - center_y) > radius:
        continue
	
    place_pixel(x, y)
