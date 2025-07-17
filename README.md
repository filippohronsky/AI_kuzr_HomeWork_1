**Vypracovanie domácej úlohy č. 1

# 🚀 Ukážka použitia pre Cisco Catalyst Center API volanie

**Spustenie skriptu:**

```bash
python3 main_openai.py

Čo sa stane po spustení?
	•	Skript odošle požiadavku na OpenAI.
	•	Automaticky sa zavolá funkcia get_dnac_devices, ktorá získa zoznam zariadení z Catalyst Center.
	•	Výstup je prehľadne zobrazený v tejto forme:
Tu je zoznam zariadení z Catalyst Center:

1. **Hostname:** sw1, **IP adresa:** 10.10.20.175
2. **Hostname:** sw2, **IP adresa:** 10.10.20.176
3. **Hostname:** sw3, **IP adresa:** 10.10.20.177
4. **Hostname:** sw4, **IP adresa:** 10.10.20.178

☑️ Príklad zobrazuje, ako API zavolá vlastnú funkciu (get_dnac_devices), získa dáta zo zariadení a výsledok prepíše do používateľsky čitateľného zoznamu.

ℹ️ Poznámka:
Ak sa zobrazí varovanie InsecureRequestWarning kvôli neoverenému HTTPS pripojeniu, odporúčame pre produkciu použiť platný certifikát.
Príklad ukazuje, ako vie API automaticky volať funkcie a odpoveď prepísať do používateľsky čitateľnej podoby.

