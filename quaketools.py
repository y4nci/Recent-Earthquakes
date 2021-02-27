import os
import requests
import datetime
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw


def ascii(txt):
    _dict_ = {"ö": "o", "ü": "u", "ğ": "g", "ç": "c", "ş": "s"}

    for char in _dict_:
        if char in txt:
            txt = txt.replace(char, _dict_[char])

    return txt


def determine_point(y, x, size):
    distance_from_west_end = y - 25.4
    distance_from_north_end = 42.5 - x
    width = size[0]
    height = size[1]
    distance_from_left_end = distance_from_west_end * width / 19.6
    distance_from_upper_end = distance_from_north_end * height / 7.05
    return round(distance_from_left_end), round(distance_from_upper_end)


def draw(y, x, magn, file):
    point = ImageDraw.Draw(file)
    points = determine_point(y, x, (1579, 677))
    point.ellipse((points[0] - round(magn ** 2), points[1] - round(magn ** 2), points[0] + round(magn ** 2), points[1] + round(magn ** 2)),
                  fill=(15 + round(magn * 30), 255 - round(magn * 30), 25))  # Hoping no earthquake bigger than 8 occurs


def get_earthquakes():
    os.remove("quakes.jpg")
    template = Image.open("map.jpg")
    template.save("quakes.jpg")
    template.close()

    earthquakes = []
    source = requests.get("http://www.koeri.boun.edu.tr/scripts/lst2.asp")
    soup = BeautifulSoup(source.content, "lxml")
    data = soup.find("pre").text[586:]

    with open("data", "w", encoding="utf-8") as file:
        file.write(str(datetime.datetime.now()) + "\n" + data[:-1])

    records = data.split("\n")

    for record in records:
        try:
            latit = record[21:28]
            long = record[31:38]
            magn = record[60:63]
            earthquakes.append([float(latit), float(long), float(magn)])

        except ValueError:
            pass

    file = Image.open("quakes.jpg")
    for earthquake in earthquakes:
        draw(earthquake[1], earthquake[0], earthquake[2], file)

    file.save("quakes.jpg")
    file.close()


def sort(by, order):
    with open("data", "r", encoding="utf-8") as file:
        file.readline()
        all_data = file.readlines()

    quakes = [[data[:19], "  ", data[21:28], "   ", data[31:38], "       ", data[45:49], "      ", data[55:58], "  ",
              data[60:63], "  ", data[65:68], "   ", data[71:]] for data in all_data]

    if order == "ascending": descending = False
    else: descending = True

    if by == "by date":
        quakes.sort(key=lambda x: x[0], reverse=descending)

    elif by == "by latitude":
        quakes.sort(key=lambda x: x[2], reverse=descending)

    elif by == "by longitude":
        quakes.sort(key=lambda x: x[4], reverse=descending)

    elif by == "by depth":
        quakes.sort(key=lambda x: x[6], reverse=descending)

    elif by == "by magnitude":
        quakes.sort(key=lambda x: x[10], reverse=descending)

    elif by == "by location":
        quakes.sort(key=lambda x: x[14], reverse=descending)

    quakes = ["".join(data) for data in quakes]

    if quakes[0] == '\n                         ': return "".join(quakes[1:])

    return "".join(quakes)
