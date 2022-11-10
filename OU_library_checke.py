import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import streamlit as st

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

url = 'https://libcal.ou.edu/reserve/groupstudyrooms'

   
def setBooking(driver):
    driver.get(url)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'xml')

    rooms = []
    times = []
    rows = soup.find_all('div', class_='fc-timeline-events fc-scrollgrid-sync-inner')
    for row in rows:
        times = []
        time_slots = row.find_all('div', class_='fc-timeline-event-harness')
        for time_slot in time_slots:
            slot = time_slot.find('a')
            times.append(slot.get('title', 'no'))
        rooms.append(times)
    return rooms

def is_library_busy(reservations):
    available_places = []
    for i in range (len(reservations)):
        for j in range(3):
            try:
                if " Available" in reservations[i][j]:
                    available_places.append(reservations[i][j])
            except:
                pass
    if len(available_places) > 2:
        return "Not Busy", available_places        
    return "Busy", available_places

t = st.empty()
n = st.empty()
while True:
    t.empty()
    n.empty()

    reservations = setBooking(driver)
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
# setBooking(driver)

