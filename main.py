import requests
import base64
import time
import os
from dotenv import load_dotenv


class Avgang:
    def __init__(self, linje, destination, tid):
        self.linje = linje
        self.destination = destination
        self.tid = tid

    def __str__(self):
        return f"Linje {self.linje} mot {self.destination} går om {self.tid}"


class VasttrafikAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        # Detta är den nya basen för version 4
        self.base_url = "https://ext-api.vasttrafik.se/pr/v4"
        self.token_url = "https://ext-api.vasttrafik.se/token"

    def hämta_token(self):
        auth_str = f"{self.client_id}:{self.client_secret}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        try:
            response = requests.post(
                self.token_url, headers=headers, data=data)
            print(f"Statuskod: {response.status_code}")

            if response.status_code == 200:
                return response.json()["access_token"]
            else:
                print(f"Svar: {response.text}")
                return None
        except Exception as e:
            print(f"Kunde inte ansluta till Västtrafik: {e}")
            return None

    def hämta_avgångar(self):
        avgang1 = Avgang("1", "Östra Sjukhuset", "2min")
        avgang2 = Avgang("7", "Bergsjön", "5min")
        return (avgang1, avgang2)

    def hämta_avgångar_från_api(self, token, stop_id):
        # I v4 behöver vi ibland skicka med tid, men vi börjar med att bara
        # anpassa URL:en till den mest grundläggande formen
        url = f"{self.base_url}/stop-areas/{stop_id}/departures"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"  # Vi lägger till att vi förväntar oss JSON
        }

        response = requests.get(url, headers=headers)

        # Denna print hjälper oss att se exakt vad som skickas
        print(f"Anropar: {url}")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Status: {response.status_code}")
            print(f"Svar: {response.text}")
            return None


class SpartavlaApp:
    def __init__(self, id, secret):
        self.api = VasttrafikAPI(id, secret)

    def visa_tavla(self, rådata):
        print("\n--- SMARAGDGATAN REALITIDSTAVLA ---")

        if not rådata or "results" not in rådata:
            print("Kunde inte hämta data.")
            return

        for vagn in rådata["results"]:
            linje = vagn["serviceJourney"]["line"]["shortName"]
            destination = vagn["serviceJourney"]["direction"]

            # HÄR ÄR FIXEN:
            # Vi försöker ta estimatedTime, om den saknas tar vi plannedTime
            full_tid = vagn.get("estimatedTime") or vagn.get("plannedTime")

            if full_tid:
                klockslag = full_tid[11:16]
                print(f"Linje {linje} mot {destination} går kl {klockslag}")
                print("------------------------------")


# HÄR lägger du in dina riktiga nycklar som du sparade förut
load_dotenv()
ID = os.getenv("VT_ID")
SECRET = os.getenv("VT_SECRET")

# --- STARTA APPLIKATIONEN ---
# Skapa appen en gång utanför loopen
app = SpartavlaApp(ID, SECRET)
smaragdgatan_id = "9021014006040000"

while True:
    token = app.api.hämta_token()

    if token:
        rådata = app.api.hämta_avgångar_från_api(token, smaragdgatan_id)
        app.visa_tavla(rådata)

        # Vänta 60 sekunder innan nästa uppdatering
        print("\nUppdateras om 60 sekunder...")
        time.sleep(60)
    else:
        print("Kunde inte hämta token. Försöker igen om 60 sekunder...")
        time.sleep(60)
