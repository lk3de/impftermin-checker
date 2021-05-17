#!/usr/bin/python3

import sys
import time
from datetime import datetime
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from web_controller import WebController


class Dataset:
    def __init__(self,
                name,
                plz,
                url,
                age = 99,
                code = "ohne",
                min_date = datetime(1970, 1, 1, 0, 0, 0),
                notification_emails = ["nospam@example.org"]):
        self.name = name
        self.code = code
        self.plz = plz
        self.url = url
        self.age = age
        self.min_date = min_date
        self.notification_emails = notification_emails

if __name__ == "__main__":

    # Config-Datei öffnen
    with open("config.json", encoding="utf-8") as config_file:
        config = json.load(config_file)

    # Firefox-Driver anlegen
    options = FirefoxOptions()
    # options.add_argument("-devtools")
    profile = FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.cookie.cookieBehavior", 1)
    driver = webdriver.Firefox(options=options, firefox_profile=profile)

    # Dauerschleife über alle Datasets in Config-Datei
    # Jeweils x Sekunden Pause nach Durchlaufen aller Datasets
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n\nEs ist {now}, starte nächsten Versuch:")



        for dataset in config["datasets"]:

            data = Dataset(name=dataset["name"], url=dataset["url"], plz=dataset["plz"],
                           notification_emails=dataset["notification_emails"])

            if "code" in dataset:
                data.code = dataset["code"]
            else:
                data.code = "ohne"

            if "min_date" in dataset:
                data.min_date = datetime.strptime(dataset["min_date"], "%Y-%m-%d")
            else:
                data.min_date = datetime(1970, 1, 1, 0, 0, 0)

            if "age" in dataset:
                data.age = dataset["age"]
            else:
                data.age = 99

            if WebController.check_impftermin(driver=driver, dataset=data, config=config):
                sys.exit(0)

            # Warte 1s vor dem nächsten Dataset
            print(f"Warte {config['wait_time_between_each_dataset']}s vor dem nächsten Code.")
            time.sleep(config["wait_time_between_each_dataset"])

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nEs ist {now}, warte {config['wait_time_between_each_run']}s vor dem nächsten Lauf.")

        time.sleep(config["wait_time_between_each_run"])
        print("Wartezeit abgelaufen.")
