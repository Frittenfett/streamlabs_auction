# ---------------------------------------
#   Import Libraries
# ---------------------------------------
import json
import codecs
import re
import os
import clr
clr.AddReference("IronPython.Modules.dll")
import urllib
import time
import random

# ---------------------------------------
#   [Required]  Script Information
# ---------------------------------------
ScriptName = "Auction"
Website = "https://www.twitch.tv/frittenfettsenpai"
Description = "Auction System. Right click and add api key!"
Creator = "frittenfettsenpai"
Version = "0.0.2"

# ---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# ---------------------------------------
def Init():
    global settings, bidMaxAmount, bidMaxUser, bidEnabled, activeFor
    settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")

    try:
        with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8")
    except:
        settings = {
            "commandBid": "!bid",
            "commandStartBid": "!startBid",
            "commandStopBid": "!stopBid",
            "languageBidNotRunning": "An active bid is currently not running!",
            "languageBidAlreadyStarted": "Bid is already in progress. Stop the bid first!",
            "languageBidNoCooldownParam": "Please use the correct syntax: {0} <1-999 seconds>",
            "languageBidGameStarted": "{0} has opend an auction. Type {1} <1-9999> to place a bid!",
            "languageBidGameClosed": "{0} has closed the auction.",
            "languageNewBidLeader": "{0} is now leading with {1} {2}."
        }
    bidMaxAmount = 0
    bidEnabled = 0
    activeFor = 0
    bidMaxUser = ""
    return


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    global settings, bidMaxAmount, bidMaxUser, bidEnabled, activeFor
    if data.IsChatMessage():
        user = data.User
        username = Parent.GetDisplayName(user)
        if (bidEnabled == 1 and data.GetParam(0).lower() == settings["commandBid"] and data.GetParamCount() > 1):
            userBid = int(data.GetParam(1))
            if (Parent.GetPoints(user) > userBid and userBid > bidMaxAmount):
                bidMaxAmount = userBid
                bidMaxUser = user
                Parent.SendTwitchMessage(settings["languageNewBidLeader"].format(username, bidMaxAmount, Parent.GetCurrencyName()))
        elif (data.GetParam(0).lower() == settings["commandStartBid"]):
            if (bidEnabled == 1):
                Parent.SendStreamWhisper(user, settings["languageBidAlreadyStarted"])
            else:
                if data.GetParamCount() <= 1:
                    Parent.SendStreamWhisper(user, settings["languageBidNoCooldownParam"].format(settings["commandStartBid"]))
                else:
                    bidEnabled = 1
                    bidMaxAmount = 0
                    bidMaxUser = ""
                    activeFor = int(data.GetParam(1))
                    Parent.SendTwitchMessage(settings["languageBidGameStarted"].format(user, settings["commandBid"]))
                    start_game()
        elif (data.GetParam(0).lower() == settings["commandStopBid"]):
            if (bidEnabled == 0):
                Parent.SendStreamWhisper(user, settings["languageBidNotRunning"])
            else:
                bidEnabled = 0
                bidMaxAmount = 0
                activeFor = 0
                bidMaxUser = ""
                Parent.SendTwitchMessage(settings["languageBidGameClosed"].format(username))
    return


#---------------------------------------
#    [Required] Tick Function
#---------------------------------------
def Tick():
    return



def start_game():
    return

def end_game():
    # Parent.RemovePoints(user, settings["costs"])
    return

