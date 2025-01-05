# MC Server Status Discord Bot
Small Python script to get the status of a Minecraft server and modify two channel names to reflect the number of players online.

Online:

![image](https://github.com/user-attachments/assets/6386f75c-127b-40ba-b015-4c00be69cca8)

Offline:

![image](https://github.com/user-attachments/assets/b350ad31-f2bb-4627-97bc-845198b823c2)


## Usage
First, install the requirements:
```bash
pip3 install -r requirements.txt
```

Create a bot in the Discord Developer portal with the necessary permissions.

Then, create a ".env" file in the same directory as the script, setting the variables `DISCORD_TOKEN`, `STATUS_CHANNEL` (the channel that says "Server Status: Online"), `PLAYERS_CHANNEL` (the channel that says "Players Online: 15"), `SERVER_IP`, and `SERVER_PORT`.

Finally, run the script: `python3 mc-server-stat.py`. It is recommended to use a systemd service file in order to restart on failure/start on boot.
