'''
Created by Frederikme (TeetiFM)
'''

#added comment
from tinderbotz.session import Session
from tinderbotz.helpers.constants_helper import *
from tinderbotz.config import Config

if __name__ == "__main__":
    # creates instance of session
    session = Session()
    # set location (Don't need to be logged in for this)
    session.set_custom_location(latitude=50.879829, longitude=4.700540)
    email = Config['login']
    password = Config['password']
    # login using your google account with a verified email!
    session.login_using_google(email, password)
    session.like(amount=10, ratio="72.5%", sleep=1)
    session.dislike(amount=1)
    session.superlike(amount=1)
    session.set_distance_range(km=15)
    session.set_age_range(18, 30)

    # Allow profiles from all over the world to appear
    session.set_global(True)

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
    pickup_line = "Hey {}! Hast du Lust mit mit ne Pizza essen zu gehen oder magst du keine Pizza?"

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

        # send a funny gif
        # session.send_gif(chatid=id, gifname="")

        # send a funny song
        # session.send_song(chatid=id, songname="")

        # send instagram or other socials like facebook, phonenumber and snapchat
        # session.send_socials(chatid=id, media=Socials.INSTAGRAM, value="insta")

        # you can also unmatch
        #session.unmatch(chatid=id)

    # let's scrape some geomatches now
    for _ in range(5):
        # get profile data (name, age, bio, images, ...)
        geomatch = session.get_geomatch(quickload=False)
        # store this data locally as json with reference to their respective (locally stored) images
        session.store_local(geomatch)
        # dislike the profile, so it will show us the next geomatch (since we got infinite amount of dislikes anyway)
        session.dislike()
