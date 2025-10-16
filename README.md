## Captive Portal Automation for NIST University

This script automates logging into the wifi captive portal for nist university. 
It works by reverse engineering the captive portal api and issuing http requests for logins and logouts like a browser.

## Usage

1. Clone this repo

```bash
git clone https://github.com/ashknl/captive-automate-requests.git captive-automate
cd captive-automate
```

2. Create an `.env` file with your wifi credentials.
The credentials should be `WIFIUSERNAME` for your username and `PASSWORD` for your password.

```
# in .env
WIFIUSERNAME=<your username>
PASSWORD=<your password>
```

3. Create a virtual environment activate it and install dependencies

```bash
python -m venv .
source bin/activate
pip install -r requirements.txt
```

4. Run the script
```
# for login
python script.py login

# for logout
python script.py logout
```