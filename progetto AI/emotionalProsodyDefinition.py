#!/usr/bin/env python3

from furhat_remote_api import FurhatRemoteAPI

# Emotional prosody library, contains the voice for emotions:
# 1. Anger
# 2. Disgust
# 3. Surprise
# 4. Fear
# 5. Happiness
# 6. Sadness

# Values for prosody parameters:
# Speed range: 20-400
# Pitch range: 20-200
# Volume range: 20-65535

furhat = FurhatRemoteAPI("100.76.1.129")


def set_ip_furhat(ip_furhat):
    global furhat
    # Create an instance of the FurhatRemoteAPI class,
    # providing the address of the robot or the SDK running the virtual robot
    furhat = FurhatRemoteAPI(ip_furhat)


# Voice of emotion: Anger
# Prosody parameters: Speed=fast;  Pitch=low;  Volume=high
# Usage: emotionalProsodyDefinition.prosody_anger("Frase da far pronunciare al robot")
def prosody_anger(sentence):
    spd = "200"  # "350"
    pit2vct = "100"  # "95"
    Vol = "65535"
    furhat.say(text="\spd=%s\ \pit2vct=%s\ \Vol=%s\ %s" % (spd, pit2vct, Vol, sentence), blocking="true")


# Voice of emotion: Disgust
# Prosody parameters: Speed=medium;  Pitch=low;  Volume=soft
# Usage: emotionalProsodyDefinition.prosody_disgust("Frase da far pronunciare al robot")
def prosody_disgust(sentence):
    spd = "200"  # "180"
    pit2vct = "100"  # "95"
    Vol = "40000"
    furhat.say(text="\spd=%s\ \pit2vct=%s\ \Vol=%s\ %s" % (spd, pit2vct, Vol, sentence), blocking="true")


# Voice of emotion: Surprise
# Prosody parameters: Speed=slow;  Pitch=high;  Volume=medium
# Usage: emotionalProsodyDefinition.prosody_surprise("Frase da far pronunciare al robot")
def prosody_surprise(sentence):
    spd = "200"  # "130"
    pit2vct = "100"  # "105"
    Vol = "50000"
    furhat.say(text="\spd=%s\ \pit2vct=%s\ \Vol=%s\ %s" % (spd, pit2vct, Vol, sentence), blocking="true")


# Voice of emotion: Fear
# Prosody parameters: Speed=fast;  Pitch=high;  Volume=high
# Usage: emotionalProsodyDefinition.prosody_fear("Frase da far pronunciare al robot")
def prosody_fear(sentence):
    spd = "200"  # "300"
    pit2vct = "100"
    Vol = "65535"
    furhat.say(text="\spd=%s\ \pit2vct=%s\ \Vol=%s\ %s" % (spd, pit2vct, Vol, sentence), blocking="true")


# Voice of emotion: Happiness
# Prosody parameters: Speed=medium;  Pitch=high;  Volume=high
# Usage: emotionalProsodyDefinition.prosody_happiness("Frase da far pronunciare al robot")
def prosody_happiness(sentence):
    spd = "200"  # "230"
    pit2vct = "100"  # "105"
    Vol = "65535"
    furhat.say(text="\spd=%s\ \pit2vct=%s\ \Vol=%s\ %s" % (spd, pit2vct, Vol, sentence), blocking="true")


# Voice of emotion: Sadness
# Prosody parameters: Speed=slow;  Pitch=low;  Volume=soft
# Usage: emotionalProsodyDefinition.prosody_sadness("Frase da far pronunciare al robot")
def prosody_sadness(sentence):
    spd = "200"  # "130"
    pit2vct = "100"  # "95"
    Vol = "40000"
    furhat.say(text="\spd=%s\ \pit2vct=%s\ \Vol=%s\ %s" % (spd, pit2vct, Vol, sentence), blocking="true")
