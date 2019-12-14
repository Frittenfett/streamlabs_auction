# ---------------------------------------
#   Import Libraries
# ---------------------------------------
import json
import codecs
import os
import clr
import time
clr.AddReference("IronPython.Modules.dll")


# ---------------------------------------
#   [Required]  Script Information
# ---------------------------------------
ScriptName = "Auction"
Website = "https://www.twitch.tv/frittenfettsenpai"
Description = "Auction System. Let the biggest bid win whatever you want."
Creator = "frittenfettsenpai"
Version = "1.1.0"

# ---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# ---------------------------------------
def Init():
    global settings, bidMaxAmount, bidMaxUser, bidEnabled, activeFor, lockCountdownConflict
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
            "minimumBidIncrease": 100,
            "languageBidNotRunning": "An active bid is currently not running!",
            "languageBidAlreadyStarted": "Bid is already in progress. Stop the bid first!",
            "languageBidGameStarted": "{0} has opened an auction for {1} seconds. Type {2} <1-9999> to place a bid!",
            "languageBidWithLowestBid": "The lowest bid has to be {0} {1}!",
            "languageBidGameClosed": "{0} has closed the auction.",
            "languageNewBidLeader": "{0} is now leading with {1} {2}.",
            "languageCountdownNobody": "{0} seconds left... Nobody did a bid yet.",
            "languageCountdownNormal": "{0} seconds left... {1} is on the lead with {2} {3}.",
            "languageCountdownFinal": "Last {0} seconds!! {1} is leading with {2} {3}.",
            "languageWon": "{0} has won this auction with a bid of {1} {2}. Congratulations.",
            "languageNobodyWon": "Nobody did a bid. Sadly, nobody wins :(",
            "languageMinimumBid": "The bid value has to be at least {0} {1} higher! Next minimum possible bid: {2} {1}!"
        }
    bidMaxAmount = 0
    bidEnabled = 0
    lockCountdownConflict = 0
    activeFor = -312
    bidMaxUser = ""
    return


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    global settings, bidMaxAmount, bidMaxUser, bidEnabled, activeFor, lockCountdownConflict
    if data.IsChatMessage():
        user = data.User
        username = Parent.GetDisplayName(user)
        if bidEnabled == 1 and data.GetParam(0) == settings["commandBid"] and data.GetParamCount() > 1:
            userBid = int(data.GetParam(1))
            if Parent.GetPoints(user) >= userBid and userBid > bidMaxAmount:
                if settings['minimumBidIncrease'] > 0 and userBid < bidMaxAmount + settings['minimumBidIncrease']:
                    Parent.SendTwitchMessage(settings["languageMinimumBid"].format(str(settings['minimumBidIncrease']), Parent.GetCurrencyName(), str(bidMaxAmount + settings['minimumBidIncrease'])))
                    return
                bidMaxAmount = userBid
                bidMaxUser = user
                if activeFor < settings["finalCountdownStart"]:
                    activeFor = settings["finalCountdownStart"]
                    lockCountdownConflict = 1
                else:
                    Parent.SendTwitchMessage(settings["languageNewBidLeader"].format(username, bidMaxAmount, Parent.GetCurrencyName()))
        elif data.GetParam(0) == settings["commandStartBid"] and Parent.HasPermission(user, "Caster", ""):
            if bidEnabled == 1:
                Parent.SendStreamWhisper(user, settings["languageBidAlreadyStarted"])
            else:
                if data.GetParamCount() > 1:
                    bidMaxAmount = int(data.GetParam(1))
                if data.GetParamCount() > 2:
                    activeFor = int(data.GetParam(2))
                else:
                    activeFor = settings["defaultCountdown"]
                Parent.SendTwitchMessage(settings["languageBidGameStarted"].format(user, activeFor, settings["commandBid"]))
                if bidMaxAmount > 0:
                    Parent.SendTwitchMessage(settings["languageBidWithLowestBid"].format(str(bidMaxAmount), Parent.GetCurrencyName()))
                bidEnabled = 1
        elif data.GetParam(0) == settings["commandStopBid"] and Parent.HasPermission(user, "Caster", ""):
            if bidEnabled == 0:
                Parent.SendStreamWhisper(user, settings["languageBidNotRunning"])
            else:
                reset_game()
                Parent.SendTwitchMessage(settings["languageBidGameClosed"].format(username))
    return


#---------------------------------------
#    [Required] Tick Function
#---------------------------------------
def Tick():
    global settings, bidMaxAmount, bidMaxUser, bidEnabled, activeFor, lockCountdownConflict
    if bidEnabled == 0 or activeFor == -312:
        return

    if activeFor > 0:
        if activeFor == 30 or activeFor == 60 or activeFor == settings["finalCountdownStart"]:
            if bidMaxUser != "":
                bitMaxUsername = Parent.GetDisplayName(bidMaxUser)
                if activeFor == settings["finalCountdownStart"]:
                    Parent.SendTwitchMessage(settings["languageCountdownFinal"].format(activeFor, bitMaxUsername, bidMaxAmount,Parent.GetCurrencyName()))
                    activeFor = activeFor - 1
                    time.sleep(2)  # Sending messages may take a while
                    lockCountdownConflict = 0
                else:
                    Parent.SendTwitchMessage(settings["languageCountdownNormal"].format(activeFor, bitMaxUsername, bidMaxAmount, Parent.GetCurrencyName()))
            else:
                Parent.SendTwitchMessage(settings["languageCountdownNobody"].format(activeFor))
    else:
        end_game()
    time.sleep(1)
    if lockCountdownConflict == 0:
        activeFor = activeFor - 1
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
        reset_game()
    return


def reset_game():
    global bidMaxAmount, bidMaxUser, bidEnabled, activeFor, lockCountdownConflict
    bidEnabled = 0
    bidMaxAmount = 0
    lockCountdownConflict = 0
    activeFor = -312
    bidMaxUser = ""
    return
