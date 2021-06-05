import time
from datetime import datetime

from playsound import playsound
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from communication_controller import CommunicationController


class WebController:

    @staticmethod
    def check_impftermin(driver, dataset, config):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Öffne Webseite basierend auf URL und PLZ
        url = f"https://{dataset.url}/impftermine/service?plz={dataset.plz}"
        print(f"\nÖffne Webseite für \"{dataset.name}\" (Vermittlungscode: {dataset.code}): {url} (Zeit: {now})")
        try:
            driver.get(url)
        except Exception:
            print("Konnte Webseite nicht öffnen, breche ab.")
            return False

        # Prüfe ob Webseite geöffnet wurde
        if "116117" not in driver.title:
            if "Derzeit keine Onlinebuchung von Impfterminen" in driver.page_source:
                print("Derzeit keine Onlinebuchung möglich, breche ab.")
                return False
            elif "Virtueller Warteraum des Impfterminservice" in driver.page_source:
                print("Virtueller Warteraum, breche ab.")
                return False
            elif "Wartungsarbeiten" in driver.page_source:
                print("Wartungsarbeiten, breche ab.")
                return False
            else:
                print("Öffnen der Webseite ging schief, breche ab.")
                return False

        # Prüfe nochmal ob Terminbuchung möglich ist
        if "Derzeit keine Onlinebuchung von Impfterminen" in driver.page_source:
            print("Derzeit keine Onlinebuchung möglich, breche ab.")
            return False
        elif "Virtueller Warteraum des Impfterminservice" in driver.page_source:
            print("Virtueller Warteraum, breche ab.")
            return False
        elif "Wartungsarbeiten" in driver.page_source:
            print("Wartungsarbeiten, breche ab.")
            return False

        # Cookie-Banner abnicken
        time.sleep(0.5)
        print("Akzeptiere Cookie-Banner.")
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/app-root/div/div/div/div[3]/div[2]/div/div[1]/a"))).click().idea
        except TimeoutException:
            print("Cookie-Banner nicht gefunden, überspringe diesen Schritt")

        # Prüfen ob Cookie-Banner noch da ist
        if "Cookie Hinweis" in driver.page_source:
            print("Cookie-Banner ist immer noch da, breche ab.")
            return False

        ### OHNE VERMITTLUNGSCODE ###
        if dataset.code == "ohne":

            # Button für "Nein, Anspruch prüfen" anklicken
            print("Klicke auf \"Nein, Anspruch prüfen\".")
            driver.find_element_by_xpath(
                "/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[2]/span").click()

            # Button für "Ja, ich bin berechtigt" anklicken
            time.sleep(3)
            if "Gehören Sie einer der genannten Personengruppen an" in driver.page_source:

                try:
                    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,
                                                                               "/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[3]/div/div/div/div[2]/div/app-corona-vaccination-no/form/div[1]/div/div/label[1]/span"))).click()
                except TimeoutException:
                    print("Button \"Ja, ich bin berechtigt\" nicht klickbar, breche ab.")
                    return False

                # Alter eintippen
                time.sleep(0.5)
                print(f"Tippe Alter ein: {dataset.age}")
                time.sleep(0.2)
                driver.find_element_by_xpath(
                    "/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[3]/div/div/div/div[2]/div/app-corona-vaccination-no/form/div[3]/div/div/input").send_keys(
                    dataset.age)

                # Button "Schnellprüfung durchführen" anklicken
                time.sleep(0.2)
                print("Klicke auf \"Schnellprüfung durchführen\"")
                driver.find_element_by_xpath(
                    "/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[3]/div/div/div/div[2]/div/app-corona-vaccination-no/form/div[4]/button").click()

                # Prüfe ob Vermittlungscode für eingetipptes Alter verfügbar
                time.sleep(3)
                if "Unsere Schnellprüfung hat ergeben, dass Sie einen Impftermin buchen dürfen." in driver.page_source:
                    print("--> Vermittlungscode kann angefordert werden.")
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    body = f"VERMITTLUNGSCODE: Für den Eintrag \"{dataset.name}\" (Alter: {dataset.age} Jahre) kann ein Vermittlungscode angefordert werden: {url} Bitte schnell anfordern! Uhrzeit jetzt: {now}"
                    CommunicationController.send_email(notification_emails=dataset.notification_emails,
                                                       subject=f"Vermittlungscode für {dataset.name}",
                                                       config=config,
                                                       body=body)
                    CommunicationController.send_telegram_message(message_text=body, config=config, silent=False)
                    return False
                else:
                    print("Kein Vermittlungscode für eingetipptes Alter verfügbar, breche ab.")
                    return False
            else:
                print("Überhaupt keine Vermittlungscodes verfügbar, breche ab.")
                return False


        ### MIT VERMITTLUNGSCODE ###
        else:

            # Button für "Vermittlungscode bereits vorhanden" anklicken
            print("Klicke auf \"Vermittlungscode bereits vorhanden\".")
            driver.find_element_by_xpath(
                "/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[1]/span").click()

            # Code eintippen
            time.sleep(0.5)
            print(f"Tippe den Vermittlungscode ein: {dataset.code}")
            time.sleep(0.2)
            driver.find_element_by_name("ets-input-code-0").send_keys(dataset.code.split("-")[0])
            time.sleep(0.2)
            driver.find_element_by_name("ets-input-code-1").send_keys(dataset.code.split("-")[1])
            time.sleep(0.2)
            driver.find_element_by_name("ets-input-code-2").send_keys(dataset.code.split("-")[2])

            # Suchen-Button klicken
            time.sleep(0.2)
            print("Klicke auf \"Termine suchen\".")
            driver.find_element_by_xpath(
                "/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[3]/div/div/div/div[1]/app-corona-vaccination-yes/form[1]/div[2]/button").click()

            # Prüfe ob Code gültig
            time.sleep(0.5)
            if "Ungültiger Vermittlungscode" in driver.page_source:
                print("Ungültiger Vermittlungscode, breche ab.")
                return False

            # Prüfe auf "Unerwarteter Fehler"
            unerwarteter_fehler_counter = 0
            max_retries = 0
            while "Es ist ein unerwarteter Fehler aufgetreten" in driver.page_source:
                unerwarteter_fehler_counter += 1
                if (unerwarteter_fehler_counter > max_retries):
                    print(f"Unerwarteter Fehler ist {unerwarteter_fehler_counter}x aufgetreten, breche ab.")
                    return False
                print("\"Unerwarteter Fehler\", warte 3s und klicke nochmal.")
                time.sleep(3)
                driver.find_element_by_xpath(
                    "/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[3]/div/div/div/div[1]/app-corona-vaccination-yes/form[1]/div[3]/button").click()

            # Klicke auf "Termine suchen"
            time.sleep(0.5)
            print("Klicke auf \"Termine suchen\".")
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,
                                                                           "/html/body/app-root/div/app-page-its-search/div/div/div[2]/div/div/div[5]/div/div[1]/div[2]/div[2]/button"))).click()
            except TimeoutException:
                print("Fehlerhafte Weiterleitung zur Startseite, breche ab.")
                return False

            # Prüfe ob Termine verfügbar sind
            time.sleep(2)
            if "Derzeit stehen leider keine Termine zur Verfügung." in driver.page_source:
                print("Kein Impftermin verfügbar, breche ab.")
                return False

            else:
                print("Impftermin(e) verfügbar. Prüfe Datum.")
                try:
                    appointment_list = driver.find_elements_by_class_name("its-slot-pair-search-item")
                    for appointment in appointment_list:
                        dates = appointment.text.split(sep="\n")
                        date_1 = datetime.strptime(dates[0][5:23], "%d.%m.%Y - %H:%M")
                        date_tupel = [date_1]
                        print(f"Terminpaar gefunden: {date_1:%d.%m.%Y, %H:%M}")
                        if all(date > dataset.min_date for date in date_tupel):
                            print(f"Terminpaar liegt nach dem Mindest-Datum ({dataset.min_date:%d.%m.%Y}). Hurra!")
                            print(f"--> Impftermin gefunden: {date_1:%d.%m.%Y, %H:%M}")

                            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            body = f"IMPFTERMIN: Für den Eintrag \"{dataset.name}\" (Vermittlungscode: {dataset.code}) ist folgender Impftermin verfügbar: {date_1:%d.%m.%Y, %H:%M}. Der Termin verfällt in 10 Minuten wieder. Uhrzeit jetzt: {now} - bitte schnell buchen! Link: {url}"
                            print(body)
                            CommunicationController.send_email(notification_emails=dataset.notification_emails,
                                       subject=f"Impftermin verfügbar für {dataset.name}", config=config,
                                       body=body)
                            CommunicationController.send_telegram_message(message_text=body, config=config, silent=False)
                            if config["alarm_sound_file"]:
                                playsound(config["alarm_sound_file"])
                            return True

                        else:
                            print(
                                f"Terminpaar liegt vor dem Mindest-Datum ({dataset.min_date:%d.%m.%Y}), überspringe Terminpaar.")

                    print("Alle Terminpaare liegen vor dem Mindest-Datum, breche ab.")
                    return False

                except NoSuchElementException:
                    print("Konnte keine Termine auf der Seite parsen.")
                    return False