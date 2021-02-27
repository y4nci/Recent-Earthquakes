# Recent-Earthquakes
A Python GUI Showing Info About Recent Earthquakes In Turkey

This repository includes two .py files, earthquake.py is the main file and quaketools.py includes the tools that are crucial for the former.

*Recent Earthquakes* is more than a GUI app that operates on the information that is already present in an internet site -I mean, it does that too but that's not the point- it also produces a map of the most recent earthquakes. Below is an example:

![quakes](https://user-images.githubusercontent.com/73401941/109389706-8e669780-791e-11eb-8ce0-f922722f93ca.jpg)

Size and colour of the circles change with the magnitude of the earthquakes and indicate the location of the earthquakes. 

*Recent Earthquakes* also is helpful when it comes sorting the data by date, magnitude, depth and more.

All the credit for the data is to http://www.koeri.boun.edu.tr/scripts/lasteq.asp. I claim no rights on the raw data shown as it's absolutely not my work. 

Packages used in this repository are:

    BeautifulSoup
    PIL
    PyQt5
