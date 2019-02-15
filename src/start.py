#!/usr/bin/env python3

#         Python Stream Deck Library
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

import StreamDeck.StreamDeck as StreamDeck
import threading
from I3.I3Helper import I3Helper


# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.
def update_key_image(deck, key, state):
    im = i3_helper.get_key_image(key, state)

    deck.set_key_image(key, im)


def handle_key_press_workspace(key, state):
    # Switch workspace
    i3_helper.go_to_workspace(key)


# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.
def key_change_callback(deck, key, state):
    # Print new key state
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

    # Update the key image based on the new key state
    update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state
    if state:
        if key < 11:
            handle_key_press_workspace(key, state)


if __name__ == "__main__":
    manager = StreamDeck.DeviceManager()
    decks = manager.enumerate()

    # Hack, for now just working with one Deck
    i3_helper = I3Helper(decks[0])

    print("Found {} Stream Decks.".format(len(decks)), flush=True)

    for deck in decks:
        deck.open()
        deck.reset()

        deck.set_brightness(50)

        # Set initial key images
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        # Register callback function for when a key state changes
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed)
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
