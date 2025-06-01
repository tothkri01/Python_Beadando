from abc import ABC, abstractmethod
from datetime import date

# --- Absztrakt Járat osztály ---
class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar

    @abstractmethod
    def jarat_info(self):
        pass

# --- BelföldiJarat osztály ---
class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar, tavolsag_km):
        super().__init__(jaratszam, celallomas, jegyar)
        self.tavolsag_km = tavolsag_km

    def jarat_info(self):
        return f"Belföldi | Járatszám: {self.jaratszam}, Cél: {self.celallomas}, Távolság: {self.tavolsag_km} km, Jegyár: {self.jegyar} Ft"

# --- NemzetkoziJarat osztály ---
class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar, orszag):
        super().__init__(jaratszam, celallomas, jegyar)
        self.orszag = orszag

    def jarat_info(self):
        return f"Nemzetközi | Járatszám: {self.jaratszam}, Cél: {self.celallomas} ({self.orszag}), Jegyár: {self.jegyar} Ft"

# --- JegyFoglalás osztály ---
class JegyFoglalas:
    def __init__(self, jarat, datum: date):
        self.jarat = jarat
        self.datum = datum

    def __str__(self):
        return f"{self.jarat.jaratszam} | {self.jarat.celallomas} | {self.datum} | {self.jarat.jegyar} Ft"

# --- LégiTársaság osztály ---
class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []

    def jarat_hozzaadas(self, jarat):
        self.jaratok.append(jarat)

    def jegy_foglalasa(self, jaratszam, datum):
        jarat = next((j for j in self.jaratok if j.jaratszam == jaratszam), None)
        if not jarat:
            return "❌ Nincs ilyen járatszám."
        if datum < date.today():
            return "❌ Csak jövőbeli dátumra lehet foglalni."
        if any(f.jarat.jaratszam == jaratszam and f.datum == datum for f in self.foglalasok):
            return "❌ Erre a járatra már van foglalás ezen a napon."
        uj_foglalas = JegyFoglalas(jarat, datum)
        self.foglalasok.append(uj_foglalas)
        return f"✅ Foglalás sikeres. Ár: {jarat.jegyar} Ft"

    def foglalas_lemondasa(self, jaratszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.jarat.jaratszam == jaratszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return "✅ Foglalás lemondva."
        return "❌ Nem található ilyen foglalás."

    def listaz_foglalasok(self):
        if not self.foglalasok:
            return "ℹ️ Nincsenek aktuális foglalások."
        return "\n".join(str(f) for f in self.foglalasok)

    def listaz_jaratok(self):
        return "\n".join(j.jarat_info() for j in self.jaratok)

# --- Konzolos felhasználói interfész ---
def main():
    legitarsasag = LegiTarsasag("SkyWings")

    # Előre feltöltött járatok
    legitarsasag.jarat_hozzaadas(BelfoldiJarat("B30356", "Debrecen", 12000, 230))
    legitarsasag.jarat_hozzaadas(NemzetkoziJarat("N34698", "London", 45000, "Egyesült Királyság"))
    legitarsasag.jarat_hozzaadas(BelfoldiJarat("B30332", "Pécs", 15000, 200))
    legitarsasag.jarat_hozzaadas(NemzetkoziJarat("N34657", "Frankfurt", 32000, "Németország"))
    legitarsasag.jarat_hozzaadas(NemzetkoziJarat("N34627", "Bécs", 25000, "Osztrákia"))
    legitarsasag.jarat_hozzaadas(NemzetkoziJarat("N46709", "Antalya", 42000, "Törökország"))



    while True:
        print("\n--- REPÜLŐJEGY FOGLALÁSI RENDSZER ---")
        print("1. Járatok listázása")
        print("2. Jegy foglalása")
        print("3. Foglalás lemondása")
        print("4. Aktuális foglalások listázása")
        print("0. Kilépés")
        valasz = input("Választás: ")

        if valasz == "1":
            print("\n-- Elérhető járatok --")
            print(legitarsasag.listaz_jaratok())
        elif valasz == "2":
            jaratszam = input("Járatszám: ").upper()
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            try:
                ev, ho, nap = map(int, datum.split("-"))
                datum_obj = date(ev, ho, nap)
                print(legitarsasag.jegy_foglalasa(jaratszam, datum_obj))
            except ValueError:
                print("❌ Hibás dátumformátum.")
        elif valasz == "3":
            jaratszam = input("Járatszám: ").upper()
            datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
            try:
                ev, ho, nap = map(int, datum.split("-"))
                datum_obj = date(ev, ho, nap)
                print(legitarsasag.foglalas_lemondasa(jaratszam, datum_obj))
            except ValueError:
                print("❌ Hibás dátumformátum.")
        elif valasz == "4":
            print("\n-- Aktuális foglalások --")
            print(legitarsasag.listaz_foglalasok())
        elif valasz == "0":
            print("👋 Viszlát!")
            break
        else:
            print("❗ Érvénytelen opció.")

if __name__ == "__main__":
    main()