# CookieProfileCreator
This is an alternative to Roblox Account Manager, which has been apparently infested with a trojan. Enjoy this simple UI that lets you get into a game on your alt account quickly. For safety reasons, it only opens the game, than just making you immediately join it. 100% of the code has been generated by ChatGPT

To begin, you obviously need to download Python, which will handle all of the things in the python script.

After you installed Python, open a Command Prompt and install all necessary libraries with these commands:

`pip install selenium`
`pip install tkinter`
`pip install webdriver-manager`
`pip install requests`

Because it uses selenium as a library, and the script creates an empty Chromium session, you will probably need to also install the Chromium browser.

After you're done with all of this, you can download the files: `script.py` and `run.bat` and create a new folder for it, where the stuff will be and all of the data it will have saved for you that can be edited.
How it works: You need to edit the run.bat file and correct the directory for the `script.py` file

This is how your folder should look:
"Roblox Profile Manager"
  "run.bat" (in the 2nd line, there is python "D:\Documents\Roblox Account Profiles\script.py", you need to correct the directory for where your script.py is)
  "script.py"
  "roblox_game_ids.json" (if you had saved a game before)
  "roblox_profiles.json" (if you had saved an account before)

Because there are no buttons to rename or remove accounts/games, follow these instructions on how to do it manually:

1. Open a `.json` file
2. You will see a json table with your account/game name and the cookie/id
This is how json tables are formatted for this and how you will be able to edit it
{
  "NAME": "COOKIE OR ID GOES HERE", <- this comma is necessary, you need to seperate each profile with a comma
  "NAME2": "COOKIE OR ID GOES HERE"
}
To rename, it's straightforward! - you just have to edit the account name, and you can also change your account cookie.
