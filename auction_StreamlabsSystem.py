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
Version = "0.0.1"

# ---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# ---------------------------------------
def Init():
	global settings, bidMaxAmount, bidMaxUser, bidEnabled
	settings = {
		"commandBid": "!bid",
		"commandStartBid": "!startBid",
		"commandStopBid": "!stopBid",
		"currencyName": "fritten"
	}
	bidMaxAmount = 0
	bidEnabled = 0
	bidMaxUser = ""
	return


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
	global settings, bidMaxAmount, bidMaxUser, bidEnabled
	if data.IsChatMessage():
		user = data.User
		if (bidEnabled == 1 and data.GetParam(0).lower() == settings["commandBid"] and data.GetParamCount() > 1):
			userBid = int(data.GetParam(1))
			#Parent.RemovePoints(user, settings["costs"])
			if (Parent.GetPoints(user) > userBid and userBid > bidMaxAmount):
				bidMaxAmount = userBid
				bidMaxUser = user
				Parent.SendTwitchMessage("{0} is now leading with {1} {2}".format(user, bidMaxAmount, settings["currencyName"]))
				#Parent.AddUserCooldown(ScriptName, settings["command"], user, settings["userCooldown"])
		elif (data.GetParam(0).lower() == settings["commandStartBid"]):
			if (bidEnabled == 1):
				Parent.SendStreamWhisper(user, "Bid is already in progress. Stop the bid first!")
			else:
				bidEnabled = 1
				bidMaxAmount = 0
				bidMaxUser = ""
				start_game()
		elif (data.GetParam(0).lower() == settings["commandStopBid"]):
			if (bidEnabled == 0):
				Parent.SendStreamWhisper(user, "An active bid is currently not running!")
			else:
				bidEnabled = 0
				bidMaxAmount = 0
				bidMaxUser = ""
	return


#---------------------------------------
#	[Required] Tick Function
#---------------------------------------
def Tick():
	return



def start_game():
	Parent.SendTwitchMessage("Started Game")
	return

