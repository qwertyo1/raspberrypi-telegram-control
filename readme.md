# Raspberry PI Telegram Control bot
Control you Raspberry PI device via Telegram bot deployed on it

## Set up as a service
1. Clone repository to your Raspberry PI
2. Create configuration `cp .env.example .env`, and then update it.
   1. `bot_token` is a Telegram bot token you receive from @BotFather
3. Create virtual environment and activate it.
   ```commandline
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   To install virtualenv run:
   ```commandline
   python3 -m pip install --user virtualenv
   ```
4. Install requirements
   ```commandline
   pip install -r -requirements.txt
   ```
5. Create service configuration file `telegram-control-bot.service` in `/etc/systemd/system` changing directories to your ones:
   ```text
   [Unit]
   Description=Raspberry PI Telegram Control bot
   
   [Service]
   User=root
   WorkingDirectory=/home/user/raspberrypi-telegram-control/
   ExecStart=/home/user/raspberrypi-telegram-control/venv/bin/python main.py
   Restart=always
   RestartSec=3
   
   [Install]
   WantedBy=multi-user.target
   ```
6. Activate service:
   ```shell
   sudo systemctl daemon-reload
   sudo systemctl start telegram-control-bot.service
   sudo systemctl enable telegram-control-bot.service
   ```