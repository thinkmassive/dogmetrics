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


# Setup calendar

from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')

msg = "today: " + str(today)
sys.stdout.write(msg + "\n")
sense.show_message(msg, scroll_speed=0.05)


# Setup datastore

import pickledb
db = pickledb.load('dogstat.db', True)

today_walks_key = today+'_walks'
today_meals_key = today+'_meals'
today_meds_key = today+'_meds'
last_walk_key = 'last_walk'
last_meal_key = 'last_meal'
last_meds_key = 'last_meds'

today_walks = db.get(today_walks_key)
today_meals = db.get(today_meals_key)
today_meds = db.get(today_meds_key)
last_walk = db.get(last_walk_key)
last_meal = db.get(last_meal_key)
last_meds = db.get(last_meds_key)

if not today_walks:
  db.set(today_walks_key, 0)
if not today_meals:
  db.set(today_meals_key, 0)
if not today_meds:
  db.set(today_meds_key, 0)

msg="From db: walks="+str(today_walks)+" meals="+str(today_meals)+" meds="+str(today_meds)+" last_walk="+str(last_walk)+" last_meal="+str(last_meal)+" last_meds="+str(last_meds) 
sys.stdout.write(msg+"\n")
sense.show_message(msg, scroll_speed=0.03)


def display_walks():
  global today_walks_key
  today_walks = db.get(today_walks_key)
  sys.stdout.write("walks" + str(today_walks) + "\n")
  sense.show_message("walks", scroll_speed=0.05)
  sense.show_letter(str(today_walks))
  time.sleep(1)
  sense.clear()


def display_meals():
  global today_meals_key
  today_meals = db.get(today_meals_key)
  sys.stdout.write("meals: " + str(today_meals) + "\n")
  sense.show_message("meals", scroll_speed=0.05)
  sense.show_letter(str(today_meals))
  time.sleep(1)
  sense.clear()


def display_meds():
  global today_meds_key
  today_meds = db.get(today_meds_key)
  sys.stdout.write("meds: " + str(today_meds) + "\n")
  sense.show_message("meds", scroll_speed=0.05)
  sense.show_letter(str(today_meds))
  time.sleep(1)
  sense.clear()


def display_last_walk():
  global last_walk_key
  last_walk = db.get(last_walk_key)
  sys.stdout.write("last walk: " + str(last_walk) + "\n")
  sense.show_message("last walk: " + str(last_walk), scroll_speed=0.05)


def display_last_meal():
  global last_meal_key
  last_meal = db.get(last_meal_key)
  sys.stdout.write("last meal: " + str(last_meal) + "\n")
  sense.show_message("last meal: " + str(last_meal), scroll_speed=0.05)


def display_last_meds():
  global last_meds_key
  last_meds = db.get(last_meds_key)
  sys.stdout.write("last meds: " + str(last_meds) + "\n")
  sense.show_message("last meds: " + str(last_meds), scroll_speed=0.05)


def display_all():
  display_walks()
  display_meals()
  display_meds()
  display_last_walk()
  display_last_meal()
  display_last_meds()


def inc_walks():
  global today_walks_key
  global last_walk_key

  today_walks = db.get(today_walks_key)
  today_walks += 1
  walk_time = datetime.now().strftime('%a %H:%M')

  db.set(today_walks_key, today_walks)
  db.set(last_walk_key, walk_time)
  display_walks()


def inc_meals():
  global today_meals_key
  global last_meal_key

  today_meals = db.get(today_meals_key)
  today_meals += 1
  meal_time = datetime.now().strftime('%a %H:%M')

  db.set(today_meals_key, today_meals)
  db.set(last_meal_key, meal_time)
  display_meals()


def inc_meds():
  global today_meds_key
  global last_meds_key

  today_meds = db.get(today_meds_key)
  today_meds += 1
  meds_time = datetime.now().strftime('%a %H:%M')

  db.set(today_meds_key, today_meds)
  db.set(last_meds_key, meds_time)
  display_meds()


sense.stick.direction_up = inc_meals
sense.stick.direction_right = inc_walks
sense.stick.direction_down = inc_meds
sense.stick.direction_left = display_all
sense.stick.direction_middle = display_all


while True:
  sense.stick.wait_for_event()
