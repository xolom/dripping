# Dripping auto reinvest

This tool enables automatic reinvesting for dripping with telegram bot support.
Per default reinvesting is done if there are more than 0.5% dividends.

## Configuration

Following configurations can be made:
* Infura URL
* Private key (from Metamask for instance)
* Telegram bot token (optional)
* Telegram users (user ids where the bot should send messages to)

The configuration is done inside [config/dripping_reinvest.json](config/dripping_reinvest.json) and can be stored anywhere.

## Requirements

Following tools and packages are reuired:
* Python 3.8+
* pip packages:
  * web3
  * python-telegram-bot
  * colorlog
  * strip_ansi
  * click
  * colorama

To install all dependencies run:

```
pip install web3 python-telegram-bot colorlog strip_ansi click colorama
```

Or use the `requirements.txt` file:
```
pip install -r requirements.txt
```

## Usage

It can be started with python command directly:
```
python3 -m dripping_reinvest --config config/dripping_reinvest.json
```
Or via the start script:
```
start.sh --config config/dripping_reinvest.json
```

## Telegram bot
There is also support for telegram bots. To get a bot, contact `@BotFather` in telegram in order to get a bot ID.
To get your telegram user ID, contact `@userinfobot`. Put those IDs into the configuration JSON file accordingly.

The bot supports following commands currently:
* `/drip_price` Return current DRIP price in USD
* `/get_dividends_thres` Show current dividends threshold
* `/set_dividends_thres` Set dividends threshold in percent

## Appendix

If this script runs on a Linux machine a `systemd` service can be created by creating a service file (e.g. `/etc/systemd/system/dripping.service`) with following content:
```ini
[Unit]
Description=Dripping service
After=network.target

[Service]
User=root
WorkingDirectory=/path/to/repo
ExecStart=bash start.sh
Restart=always

[Install]
WantedBy=multi-user.target
```
Then enable the service with `systemctl enable dripping` and start it with `systemctl start dripping`
