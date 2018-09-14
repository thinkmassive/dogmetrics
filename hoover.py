##########################
# Hoover.dog Daily Tracker
# by alex@thinkmassive.org
##########################

import sys
import time
import threading
from datetime import datetime
import pickledb

# Globals

today = datetime.today().strftime('%Y-%m-%d')
today_walks_key = today+'_walks'
today_meals_key = today+'_meals'
today_meds_key = today+'_meds'
last_walk_key = 'last_walk'
last_meal_key = 'last_meal'
last_meds_key = 'last_meds'


# Logging

def log(msg):
  sys.stdout.write(msg + "\n")
  sys.stdout.flush()


# SenseHAT

from sense_hat import SenseHat
sense = SenseHat()
sense.low_light = True
sense.set_rotation(90)
sense.clear()


# Daily rotation

def update_today():
  log('update_today: started')
  global today
  global today_walks_key, today_meals_key, today_meds_key
  global last_walk_key, last_meal_key, last_meds_key

  today = datetime.today().strftime('%Y-%m-%d')
  msg = "today: " + str(today)
  log(msg)
  sense.show_message(msg, scroll_speed=0.05)

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
  log(msg)
  sense.show_message(msg, scroll_speed=0.03)
  log('update_today: ending')


# Stats Display

def display_walks():
  global today_walks_key
  today_walks = db.get(today_walks_key)
  log("walks: " + str(today_walks))
  sense.show_message("walks", scroll_speed=0.05)
  sense.show_letter(str(today_walks))
  time.sleep(1)
  sense.clear()

def display_meals():
  global today_meals_key
  today_meals = db.get(today_meals_key)
  log("meals: " + str(today_meals))
  sense.show_message("meals", scroll_speed=0.05)
  sense.show_letter(str(today_meals))
  time.sleep(1)
  sense.clear()

def display_meds():
  global today_meds_key
  today_meds = db.get(today_meds_key)
  log("meds: " + str(today_meds))
  sense.show_message("meds", scroll_speed=0.05)
  sense.show_letter(str(today_meds))
  time.sleep(1)
  sense.clear()

def display_last_walk():
  global last_walk_key
  msg = "last walk: " + str(db.get(last_walk_key))
  log(msg)
  sense.show_message(msg, scroll_speed=0.05)

def display_last_meal():
  global last_meal_key
  msg = "last meal: " + str(db.get(last_meal_key))
  log(msg);
  sense.show_message(msg, scroll_speed=0.05)

def display_last_meds():
  global last_meds_key
  msg = "last meds: " + str(db.get(last_meds_key))
  log(msg)
  sense.show_message(msg, scroll_speed=0.05)

def display_all():
  log('display_all: started')
  display_walks()
  display_meals()
  display_meds()
  display_last_walk()
  display_last_meal()
  display_last_meds()
  log('display_all: ending')


# Stats Increment

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


# Threads

def input():
  log('input: thread started')
  try:
    sense.stick.direction_up = inc_meals
    sense.stick.direction_right = inc_walks
    sense.stick.direction_down = inc_meds
    sense.stick.direction_left = display_all
    sense.stick.direction_middle = display_all
  except:
    print('Failed to configure SenseHAT joystick')
    return 2
  while True:
    sense.stick.wait_for_event()

def cron():
  log('cron: thread started')
  global today

  while True:
    while today == str(datetime.today().strftime('%Y-%m-%d')):
      time.sleep(10)
    log('cron: calling update_today()')
    update_today()
    log('cron: returned from update_today()')


# Main Loop
db = pickledb.load('dogstat.db', True)
update_today()

t_cron = threading.Thread(name='cron', target=cron)
t_input = threading.Thread(name='input', target=input)
t_cron.start()
t_input.start()
