#!/usr/bin/python3

import sys
import time
import json
from datetime import datetime
from random import randrange

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

    if config["use_chrome"]:
        driver = WebController.create_chromedriver()
    else:
        driver = WebController.create_firefoxdriver()


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

            # Warte vor dem nächsten Dataset
            wait_time_dataset = config['wait_time_between_each_dataset'] + randrange(5)
            print(f"Warte {wait_time_dataset}s vor dem nächsten Code.")
            time.sleep(wait_time_dataset)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        wait_time_run = config['wait_time_between_each_run'] + randrange(45)
        print(f"\nEs ist {now}, warte {wait_time_run}s vor dem nächsten Lauf.")
        time.sleep(wait_time_run)
        print("Wartezeit abgelaufen.")
