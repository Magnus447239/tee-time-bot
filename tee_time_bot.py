import urllib.request
import re
import os

url = "https://rastimar.golf.is/?date=2026-09-07"

# =========================
# 1. SÆKJA SÍÐUNA
# =========================

response = urllib.request.urlopen(url)
html = response.read().decode("utf-8")

# Tökum bara Grafarholt-hlutann
grafarholt = html.split("Grafarholt", 1)[1]
grafarholt = grafarholt.split("Leirdalsvöllur", 1)[0]

# Finnum alla tíma
timasetningar = re.findall(r"\b\d{2}:\d{2}\b", grafarholt)

# Sleppum "Uppfært 18:xx"
if timasetningar:
    timasetningar = timasetningar[1:]

# Fjarlægjum tvítekin gildi
timasetningar = sorted(set(timasetningar))

# Höldum bara tímum milli 18 og 19
lausir_timar = []

for timi in timasetningar:
    if "18:00" <= timi <= "19:00":
        lausir_timar.append(timi)


# =========================
# 2. LESA GAMLA TÍMA
# =========================

skra = "sidustu_timar.txt"

gamli_timar = []

if os.path.exists(skra):
    with open(skra, "r") as f:
        gamli_timar = f.read().splitlines()


# =========================
# 3. FINNA NÝJA TÍMA
# =========================

nyir_timar = []

for timi in lausir_timar:
    if timi not in gamli_timar:
        nyir_timar.append(timi)


# =========================
# 4. PRENTA NIÐURSTÖÐU
# =========================

print("Grafarholt - 7. september")
print("Lausir tímar milli 18:00 og 19:00:")

for timi in lausir_timar:
    print(timi)

print()

if not os.path.exists(skra):
    print("Fyrsta keyrsla - vista núverandi tíma.")

elif len(nyir_timar) > 0:

    for timi in nyir_timar:
        print("🏌️ NÝR RÁSTÍMI:", timi)

else:
    print("Enginn nýr rástími.")


# =========================
# 5. VISTA NÚVERANDI TÍMA
# =========================

with open(skra, "w") as f:

    for timi in lausir_timar:
        f.write(timi + "\n")
        