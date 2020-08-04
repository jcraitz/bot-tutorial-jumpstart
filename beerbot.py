#!/usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from Twitter Bot Starter Kit: Bot 3

# This bot tweets a random beer

# random beers come from https://api.punkapi.com/v2/beers/random

import requests, os
from random import randint
from credentials import *
import tweepy
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
beer_base_url = 'https://api.punkapi.com/v2/beers/'

def tweet_msg(msg):
   api.update_status(status=msg)

def tweet_image(url, message):
   filename = 'temp.jpg'
   request = requests.get(url, stream=True)
   if request.status_code == 200:
      with open(filename, 'wb') as image:
         for chunk in request:
            image.write(chunk)
   
      api.update_with_media(filename, status=message)
      os.remove(filename)
   else:
      print("Unable to download image")

# gather some corpora from GitHub using requests; these are in JSON format
random_beer_response = requests.get(beer_base_url + 'random')

# Extract a Python-readable list from each response
beer_raw = random_beer_response.json()[0]
params = ['id','name','tagline','image_url','food_pairing']
beerDict = { key: beer_raw[key] for key in params }

tweet_text = 'Your random beer pairing. \n\n\
   Beer: {0}\n\
   Type: {1}\n\
   Pair it with {2}.\n\n\
   Details here: {3}\n\
   Thanks to the punkapi.' \
   .format(beerDict['name'], beerDict['tagline'], beerDict['food_pairing'][0], beer_base_url+str(beerDict['id']))
      
if beerDict['image_url'] == "https://images.punkapi.com/v2/keg.png":
   tweet_msg(tweet_text)
else:
   tweet_image(beerDict['image_url'],tweet_text)

print(tweet_text)
