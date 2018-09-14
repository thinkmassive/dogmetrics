##########################
# Hoover.dog Daily Tracker
# by alex@thinkmassive.org
##########################

import sys
import time

# Setup GPIO
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(90)
sense.clear()

# Setup datastore
import pickledb
db = pickledb.load('dogstat.db', True)

# Setup calendar
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')
sys.stdout.write("today: " + str(today) + "\n")

# Initialize daily data
today_walks_key = today+'_walks'
today_meals_key = today+'_meals'
today_meds_key = today+'_meds'
today_walks = db.get(today_walks_key)
today_meals = db.get(today_meals_key)
today_meds = db.get(today_meds_key)

if not today_walks:
  db.set(today_walks_key, 0)
if not today_meals:
  db.set(today_meals_key, 0)
if not today_meds:
  db.set(today_meds_key, 0)

sys.stdout.write("Loaded from db: walks="+str(today_walks)+" meals="+str(today_meals)+" meds="+str(today_meds)+"\n")

# Functions
def display_walks():
  global today_walks_key
  today_walks = db.get(today_walks_key)
  sys.stdout.write("walks" + str(today_walks) + "\n")
  sense.show_message("walks: ", scroll_speed=0.04)
  sense.show_letter(str(today_walks))
  time.sleep(1)
  sense.clear()

def display_meals():
  global today_meals_key
  today_meals = db.get(today_meals_key)
  sys.stdout.write("meals: " + str(today_meals) + "\n")
  sense.show_message("meals", scroll_speed=0.04)
  sense.show_letter(str(today_meals))
  time.sleep(1)
  sense.clear()

def display_meds():
  global today_meds_key
  today_meds = db.get(today_meds_key)
  sys.stdout.write("meds: " + str(today_meds) + "\n")
  sense.show_message("meds", scroll_speed=0.04)
  sense.show_letter(str(today_meds))
  time.sleep(1)
  sense.clear()

def display_all(t):
  display_walks()
  display_meals()
  display_meds()

def inc_walks():
  global today_walks_key
  today_walks = db.get(today_walks_key)
  today_walks += 1
  db.set(today_walks_key, today_walks)
  display_walks()

def inc_meals():
  global today_meals_key
  today_meals = db.get(today_meals_key)
  today_meals += 1
  db.set(today_meals_key, today_meals)
  display_meals()

def inc_meds():
  global today_meds_key
  today_meds = db.get(today_meds_key)
  today_meds += 1
  db.set(today_meds_key, today_meds)
  display_meds()

sense.stick.direction_up = inc_meals
sense.stick.direction_right = inc_walks
sense.stick.direction_down = inc_meds
sense.stick.direction_left = display_all
sense.stick.direction_middle = display_all

while True:
  sense.stick.wait_for_event()
