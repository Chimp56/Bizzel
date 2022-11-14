import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import streamlit as st

# sets up the webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

# link to the reservations for Bizzel's Library rooms
url = 'https://libcal.ou.edu/reserve/groupstudyrooms'
    
# retrieves the studyrooms bookings and returns it as a list
def getBooking(driver):
    # goes to the link
    driver.get(url)
    # retrieves source code of the website
    page_source = driver.page_source
    # parses the source code into something interactable
    soup = BeautifulSoup(page_source, 'xml')
    # lists to store data in
    rooms = []
    times = []

    # gets current booking status for every rooms
    # each element in rooms is a list of times for each room
    rows = soup.find_all('div', class_='fc-timeline-events fc-scrollgrid-sync-inner')
    for row in rows:
        times = []
        time_slots = row.find_all('div', class_='fc-timeline-event-harness')
        for time_slot in time_slots:
            slot = time_slot.find('a')
            times.append(slot.get('title', 'no'))
        rooms.append(times)
    return rooms

# determines whether library is busy or not and returns a list of of available rooms
def is_library_busy(reservations):
    availableCount = 0
    avialable_places = []
    # loops through the previously retrieved list to check for available rooms and time slots
    for i in range (len(reservations)):
        for j in range(3):
            try:
                if " Available" in reservations[i][j]:
                    avialable_places.append(reservations[i][j])
                    availableCount += 1
            except:
                pass
    # not busy if there are 3 or more 30 minute time slots available in the next 1 and a half hours 
    if availableCount > 2:
        return "Not Busy", avialable_places        
    return "Busy", avialable_places


# homepage = 'https://sites.google.com/d/1d4ciRnNkLIREEqSyKLK17wt8hy_KaqRU/p/1G0PwWL8LhKhYEe_2HUjWKM-NXLsgAGug/'
t = st.empty()
n = st.empty()
while True:
    t.empty()
    n.empty()

    reservations = getBooking(driver)
    is_busy, places = is_library_busy(reservations)
    
    t.write(is_busy + "\n\n")
    printString = ""
    for i in places:
        printString += "\n" + i + "\n\t\t   "
    try:
        n.write(printString)
    except:
        n.write("Little to no space available")
    # link = '[Back to homepage](https://sites.google.com/d/1d4ciRnNkLIREEqSyKLK17wt8hy_KaqRU/p/1G0PwWL8LhKhYEe_2HUjWKM-NXLsgAGug/)'
    # st.markdown(link, unsafe_allow_html=True)
    
    
    time.sleep(60)

