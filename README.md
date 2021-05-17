# Impftermin-Checker
## Setup
### Install dependencies
Install the dependencies with:
```
pip3 install selenium python-telegram-bot playsound
```

### Install Geckodriver
The Checker uses Selenium with Firefox. For that to work, you need to have the [Geckodriver](https://github.com/mozilla/geckodriver/releases) executable in your PATH. Download the respective binary for your OS and make sure it's accessible (on Ubuntu, just run `apt-get install firefox-geckodriver`).

### Create `config.json`
Create a `config.json` based on the `config.example.json`.
For each `dataset` entry, you can decide if you already have a Vermittlungscode or not.

#### With Vermittlungscode
If you already have a code, make sure to choose the correct Impfzentrum that your code is valid for (every code is only valid for one single Impfzentrum). The Checker will then enter your code and check if an appointment is available.

For each `dataset` entry with Vermittlungscode, you can optionally state a `min_date` string in the format `YYYY-MM-DD`. This is useful e.g. if you are not yet old enough and want to book an appointment only after you are old enough. If this is present, the Checker will compare all available appointments to the given date.

##### Example:
```
{
   "name": "Erika Mustermann",
   "code": "ABCD-1234-9876",
   "plz": 12345,
   "min_date": "2021-08-31",
   "url": "001-iz.impfterminservice.de",
   "notification_emails": ["erika@mustermann.de", "nospam@example.org"]
}
```

#### Without Vermittlungscode
If you don't have a code yet, please only enter **one** `dataset` per Impfzentrum. The Checker will then query that Impfzentrum if there are any free appointments in general.

For each `dataset`entry without Vermittlungscode, you can optionally state an `age`. The checker will then check if a Vermittlungscode is available for the given age. If you don't state an `age`, the checker will search with `age = 99`.

##### Example:
```
{
   "name": "Impfzentrum Stuttgart Liederhalle",
   "plz": 70174,
   "url": "002-iz.impfterminservice.de",
   "age": 40,
   "notification_emails": ["erika@mustermann.de"]
}
```

#### Alternative option to get a Vermittlungscode instantly (Windows-only)
Download and install [Fiddler Classic](https://www.telerik.com/fiddler/fiddler-classic), which works as a proxy and allows you to intercept the server's response before it reaches the browser. Open it and go to Tools -> Options -> HTTPS. Activate the checkbox "Decrypt HTTPS traffic" and confirm the pop-up messages that appear. This will install the Fiddler root certificate into your Windows certificate trust store. **Remark: Fiddler will be able to act as [MITM](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) and decrypt all HTTPS traffic of any application as of here!** Then go to Rules -> Customize Rules to open the Fiddler ScriptEditor. Inside the function `OnBeforeResponse`, add the following snippet and save it:
```
if (oSession.uriContains("impfterminservice") && oSession.uriContains("termincheck")) {
    oSession.utilSetResponseBody('{"termineVorhanden":true,"vorhandeneLeistungsmerkmale":["L921"]}')
}
```
After that, you can use Chrome or Edge (Firefox doesn't work because it has its own trust store) manually to open the Impterminservice page and request a Vermittlungscode. The snippet above will modify the server's response before it reaches the local local browser frontend, making it think that a Vermittlungscode can be generated. Enter your data and receive your code instantly.


#### Resources to build your `config.json`
* You can find all Impfzentrum URLs + PLZs here: https://www.impfterminservice.de/assets/static/impfzentren.json
* Enter your SMTP credentials to get notified via email.
* Create a Telegram Bot using the [Botfather](https://telegram.me/botfather) and enter your Chat ID(s) (use the [IDBot](https://telegram.me/myidbot) to get your ID) to get notified via Telegram.
* For documentation reasons - you can find the available Impfstoffe here: https://001-iz.impfterminservice.de/assets/static/its/vaccination-list.json
* Remark: If you get lots of "Unbekannter Fehler ist aufgetreten" (= HTTP 429 Too Many Requests), increase the waiting time between each run.

## Run
Run the Checker using
```
python3 impftermin_checker.py
```

Using the `selenium` framework, the Checker will then remote-control a Firefox to simulate a user checking for appointments and Vermittlungscodes.
If there's an appointment available, it will stop, play an alarm sound, leave the browser window open and notify you via email and Telegram.
If there's a Vermittlungscode, it will notify you via email and Telegram, but will not stop nor play an alarm sound.


## Open Todos
* ~Implement the search for an appointment without having a Vermittlungscode~
* Create an individual Telegram notification configuration for each `dataset` entry, instead of one global configuration (similar to email notifications).
* ~Refactor the `check_impftermin` function, probably also the `send_email` and `send_telegram_notification` functions, to class functions instead of global functions.~
## Backlog ideas
* ~Send notifications via Telegram Bot~
