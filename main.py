
class Avgang:
    def __init__(self, linje, destination, tid):
        self.linje = linje
        self.destination = destination
        self.tid = tid

    def __str__(self):
        return f"Linje {self.linje} mot {self.destination} går om {self.tid}"


class VasttrafikAPI:
    def __init__(self):
        self.base_url = "https://api.vasttrafik.se"

    def hämnta_avgångar(self):
        avgang1 = Avgang("1", "Östra Sjukhuset", "2min")
        avgang2 = Avgang("7", "Bergsjön", "5min")
        return (avgang1, avgang2)


class SpartavlaApp:
    def __init__(self):
        self.api = VasttrafikAPI()

    def visa_tavla(self):
        print("--- SMARAGDGATAN SPÅRTAVLA ---")
        avgångar = self.api.hämnta_avgångar()

        for vagn in avgångar:
            print(vagn)
            print("------------------------------")


app = SpartavlaApp()
app.visa_tavla()
