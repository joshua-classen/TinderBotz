import json
import random
import datetime
from time import sleep
from tinderbotz.session import Session
from tinderbotz.helpers.constants_helper import *
from tinderbotz.config import Config


if __name__ == "__main__":
    # creates instance of session
    session = Session()

    #login
    email = Config['login']
    password = Config['password']
    session.login_using_google(email, password)


    """
    1. get the locations in an array and scramblen this array
    2. get 15 min + random number [0, 15] min that is beetween locations changes
    3. set time for how long to be active per city
    4. set time where bot is allowed to to anything on tinder.
    """

    with open("citylocations.json", "r") as read_file:
        data = json.load(read_file)

    #todo: implement shuffle

    
    now = datetime.datetime.now()
    minTimeStart = now.replace(hour=8, minute=0, second=0, microsecond=0)
    maxTimeStop = now.replace(hour=23, minute=0, second=0, microsecond=0)


    session.set_distance_range(km=10)
    session.set_age_range(18, 30)
    session.set_global(True) # Allow profiles from all over the world to appear

    while datetime.datetime.now() >= minTimeStart and datetime.datetime.now() <= maxTimeStop:
        for city in data:
            print("Setting location to " + city)
            session.set_custom_location(latitude=data[city]['latitude'], longitude=data[city]['longitude'])
            sleep(1)
            session.like(amount=random.randint(40, 200), ratio="69.0%", sleep=random.randint(1,3))
            #session.superlike(amount=1)
            waitTime = random.randint(3,10)
            print("Wait " + str(waitTime) + " seconds to change location.")
            sleep(waitTime)
        # Getting matches takes a while, so recommended you load as much as possible from local storage
        # get new matches, with whom you haven't interacted yet
        # Let's load the first 10 new matches to interact with later on.
        # quickload on false will make sure ALL images are stored, but this might take a lot more time
        new_matches = session.get_new_matches(amount=10, quickload=False)
        # get already interacted with matches (matches with whom you've chatted already)
        messaged_matches = session.get_messaged_matches()
    
         # you can store the data and images of these matches now locally in data/matches
        # For now let's just store the messaged_matches
        for match in messaged_matches:
            session.store_local(match)

        # Pick up line with their personal name so it doesn't look spammy
        pickup_line = "Hey {}! Hast du Lust mit mir eine Pizza essen zu gehen oder magst du etwa keine Pizza?"

        # loop through my new matches and send them the first message of the conversation
        for match in new_matches:
            # store name and chatid in variables so we can use it more simply later on
            name = match.get_name()
            id = match.get_chat_id()
            print(name, id)
            # Format the match her/his name in your pickup line for a more personal approach.
            message = pickup_line.format(name)
            # send pick up line with their name in it to all my matches
            session.send_message(chatid=id, message=message)
    

    print("Now is not the right time for the bot")