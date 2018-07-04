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
Version = "0.0.3"

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
            "finalCountdownStart": 10,
            "defaultCountdown": 120,
            "languageBidNotRunning": "An active bid is currently not running!",
            "languageBidAlreadyStarted": "Bid is already in progress. Stop the bid first!",
            "languageBidGameStarted": "{0} has opened an auction for {1} seconds. Type {2} <1-9999> to place a bid!",
            "languageBidGameClosed": "{0} has closed the auction.",
            "languageNewBidLeader": "{0} is now leading with {1} {2}.",
            "languageCountdownNobody": "{0} seconds left... Nobody did a bid yet.",
            "languageCountdownNormal": "{0} seconds left... {1} is on the lead with {2} {3}.",
            "languageCountdownFinal": "Last {0} seconds!! {1} is leading with {2} {3}.",
            "languageWon": "{0} has won this auction with a bid of {1} {2}. Congratulations.",
            "languageNobodyWon": "Nobody did a bid. Sadly, nobody wins :(",
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
        if (bidEnabled == 1 and data.GetParam(0) == settings["commandBid"] and data.GetParamCount() > 1):
            userBid = int(data.GetParam(1))
            if (Parent.GetPoints(user) >= userBid and userBid > bidMaxAmount):
                bidMaxAmount = userBid
                bidMaxUser = user
                if activeFor < settings["finalCountdownStart"]:
                    activeFor = settings["finalCountdownStart"]
                Parent.SendTwitchMessage(settings["languageNewBidLeader"].format(username, bidMaxAmount, Parent.GetCurrencyName()))
        elif (data.GetParam(0) == settings["commandStartBid"]):
            if (bidEnabled == 1):
                Parent.SendStreamWhisper(user, settings["languageBidAlreadyStarted"])
            else:
                if data.GetParamCount() > 1:
                    activeFor = int(data.GetParam(1))
                else:
                    activeFor = settings["defaultCountdown"]
                Parent.SendTwitchMessage(settings["languageBidGameStarted"].format(user, activeFor, settings["commandBid"]))
                start_game()
        elif (data.GetParam(0) == settings["commandStopBid"]):
            if (bidEnabled == 0):
                Parent.SendStreamWhisper(user, settings["languageBidNotRunning"])
            else:
                reset_game()
                Parent.SendTwitchMessage(settings["languageBidGameClosed"].format(username))
    return


#---------------------------------------
#    [Required] Tick Function
#---------------------------------------
def Tick():
    return



def start_game():
    global settings, bidMaxAmount, bidMaxUser, bidEnabled, activeFor
    bidEnabled = 1
    bidMaxAmount = 0
    bidMaxUser = ""
    while activeFor > 0 and bidEnabled == 1:
        if activeFor == 30 or activeFor == 60 or activeFor == settings["finalCountdownStart"]:
            if bidMaxUser != "":
                bitMaxUsername = Parent.GetDisplayName(bidMaxUser)
                if activeFor == settings["finalCountdownStart"]:
                    Parent.SendTwitchMessage(settings["languageCountdownFinal"].format(activeFor, bitMaxUsername, bidMaxAmount,Parent.GetCurrencyName()))
                else:
                    Parent.SendTwitchMessage(settings["languageCountdownNormal"].format(activeFor, bitMaxUsername, bidMaxAmount, Parent.GetCurrencyName()))
            else:
                Parent.SendTwitchMessage(settings["languageCountdownNobody"].format(activeFor))
        time.sleep(1)
        activeFor = activeFor - 1
    if bidEnabled == 1:
        end_game()
    return


def end_game():
    global settings, bidMaxAmount, bidMaxUser, bidEnabled, activeFor
    if bidMaxUser != "":
        Parent.RemovePoints(bidMaxUser, bidMaxAmount)
        bitMaxUsername = Parent.GetDisplayName(bidMaxUser)
        Parent.SendTwitchMessage(settings["languageWon"].format(bitMaxUsername, bidMaxAmount, Parent.GetCurrencyName()))
        reset_game()
    else:
        Parent.SendTwitchMessage(settings["languageNobodyWon"])
    return


def reset_game():
    global bidMaxAmount, bidMaxUser, bidEnabled, activeFor
    bidEnabled = 0
    bidMaxAmount = 0
    activeFor = 0
    bidMaxUser = ""
    return
