# Hit run at the top!
# This program will not save your reddit login details.

## CONFIGURATION ##
tip_coord = (496, 404)
height = 21
##
center_x = 497
center_y = 414

radius = 9
##
# 0 for circle mode, 1 for triangle mode
mode = 1
# True causes the points to not be placed and the coordinates to be printed to the console.
debug = False
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
session.headers[
    "User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36"
response = session.post("https://www.reddit.com/api/login/{}".format(username),
                        data={"user": username, "passwd": password, "api_type": "json"})
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
        response = session.post("https://www.reddit.com/api/place/draw.json",
                         data={"x": str(ax), "y": str(ay), "color": str(new_color)})

        secs = float(response.json()["wait_seconds"])
        if "error" not in response.json():
            print("Placed empty pixel! - waiting {} seconds".format(secs))
        else:
            print("Cooldown already active - waiting {} seconds".format(int(secs)))
        time.sleep(secs + 2)

        if "error" in response.json():
            place_pixel(ax, ay)

# Circle mode.
# This chooses a random point within the radius to erase.
if mode == 0:
    while True:
        x = random.randint(center_x - radius, center_x + radius)
        y = random.randint(center_y - radius, center_y + radius)

        # Reject coordinates outside the circle
        if math.hypot(x - center_x, y - center_y) > radius:
            continue
        if debug:
            print(x, y)
        else:
            place_pixel(x, y)

# Triangle mode.
# This iterates through every pixel in the predefined triangle, starting at the top left, and down to bottom right.
# This assumes a 45-45-90 triangle with the right angle at the top. The top also being 2 wide.
elif mode == 1:
    while True:
        i = 0
        # Goes down the left edge
        for row in range(0, height, 1):
            x, y = tip_coord
            x -= i
            y += i
            j = 0
            # Fills in the rows. Each row is 2 tiles longer than the last.
            for column in range(0, i*2, 1):
                j += 1
                if debug:
                    print(x+j, y)
                else:
                    place_pixel(x+j, y)
            i += 1
