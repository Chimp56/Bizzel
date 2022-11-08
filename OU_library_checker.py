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
# driver.get(url)


def save_html(html, path):
    with open(path, 'a') as f:
        f.write(html)
        
        
# save_html(r.content, 'google_com')

def open_html(path):
    with open(path, 'rb') as f:
        return f.read()
    
    
# html = open_html('google_com')

# more_buttons = driver.find_elements_by_class_name("moreLink")
# for x in range(len(more_buttons)):
#   if more_buttons[x].is_displayed():
#       driver.execute_script("arguments[0].click();", more_buttons[x])
#       time.sleep(1)
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
        # re
        # print(review_selector.get('style', 'No title'))
            slot = time_slot.find('a')
            times.append(slot.get('title', 'no'))
        # print(times, "\n\n")
        rooms.append(times)
    return rooms

def is_library_busy(reservations):
    availableCount = 0
    avialable_places = []
    for i in range (len(reservations)):
        for j in range(3):
            try:
                if " Available" in reservations[i][j]:
                    avialable_places.append(reservations[i][j])
                    availableCount += 1
            except:
                pass
    if availableCount > 2:
        return "Not Busy", avialable_places        
    return "Busy", avialable_places


# print(is_library_busy(reservations))

while True:
    t = st.empty()
    t.empty()

    reservations = setBooking(driver)
    is_busy, places = is_library_busy(reservations)
    with t.container():
        printString = is_busy + "\n\n"
        # st.write(is_busy)
        for i in places:
            printString = printString + i + "\n"
        t.write(printString)
    
    
    time.sleep(60)
# setBooking(driver)

