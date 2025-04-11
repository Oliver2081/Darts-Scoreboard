# -------------------------------- #
# Project : Darts Scoreboard
# Author  : Oliver Spilsted
# Version : V0.3
# Created : 23/03/2025
# Modified: 11/04/2025
# -------------------------------- #

# ---- Imports ---- #
import os
import json
import questionary as q
from shutil import move

# ---- Variables ---- #
dataDir = './data/'

userData = {}
usernames = []

# ---- Functions ---- #
def loadUserFile(filePath):
	with open(filePath, 'r') as file:
		return json.load(file)

def saveUserFile(user, data):
	filePath = os.path.join(dataDir, f"{user}.json")
	with open(filePath, 'w') as file:
		json.dump(data, file, indent=4)

def loadAllUsers(directory):
	users = {}
	for filename in os.listdir(directory):
		if filename.endswith('.json'):
			filePath = os.path.join(directory, filename)
			data = loadUserFile(filePath)
			username = data.get("username")
			if username:
				users[username] = data
	return users

def refreshUserData():
	global userData, usernames
	userData = loadAllUsers(dataDir)
	usernames = list(userData.keys())

def createDefaultStats(username):
	return {
		"username": username,
		"gamesPlayed": 0,
		"wins": 0,
		"losses": 0,
		"stats": {k: 0 for k in (
			[str(n) for n in range(1, 21)] +
			[f"D{n}" for n in range(1, 21)] +
			[f"T{n}" for n in range(1, 21)] +
			["OB", "B", "miss"]
		)}
	}


def managePlayers():
	while True:
		refreshUserData()
		choice = q.select("Manage Players", choices=["Add Player","Remove Player","Rename Player",q.Separator(),"Back"]).ask()
		match choice:
			case "Add Player":
					username = q.text("Enter new username:").ask()
					if username in usernames:
						print("That username already exists.")
					else:
						data = createDefaultStats(username)
						saveUserFile(username, data)
						print(f"User '{username}' added.")
						refreshUserData()
						
			case "Remove Player":
					if not usernames:
						print("No players to remove.")
					else:
						selected = q.select("Select a player to remove:", choices=usernames).ask()
						filePath = os.path.join(dataDir, f"{selected}.json")
						os.remove(filePath)
						print(f"User '{selected}' removed.")
						refreshUserData()
						
			case "Rename Player":
					if not usernames:
						print("No players to rename.")
					else:
						selected = q.select("Select a player to rename:", choices=usernames).ask()
						newName = q.text(f"Enter new name for '{selected}':").ask()
						if newName in usernames:
							print("That name already exists.")
						else:
							# Rename the file
							oldPath = os.path.join(dataDir, f"{selected}.json")
							newPath = os.path.join(dataDir, f"{newName}.json")
							
							data = userData[selected]
							data["username"] = newName
							
							with open(newPath, 'w') as file:
								json.dump(data, file, indent=4)
								
							os.remove(oldPath)
							print(f"User '{selected}' renamed to '{newName}'.")
							refreshUserData()
							
			case "Back":
				break

def mainMenu():
	while True:
		refreshUserData()
		choice = q.select(
			"Main Menu - Darts Scoreboard",
			choices=[
				"Play",
				"Manage Players",
				q.Separator(),
				"Quit"
			]
		).ask()

		if choice == "Play":
			playGame()
		elif choice == "Manage Players":
			managePlayers()
		elif choice == "Quit":
			break

def playGame():
	if not usernames:
		print("No players available. Add players first.")
		return
	selectedPlayers = q.checkbox("Select Players:", usernames).ask()
	if not selectedPlayers:
		print("No players selected.")
		return
	print(f"\nPlayers selected ({len(selectedPlayers)}):")
	for player in selectedPlayers:
		print(f"- {player}")
		
	
	# You can add game logic here

# ---- Start Program ---- #
if __name__ == "__main__":
	mainMenu()
