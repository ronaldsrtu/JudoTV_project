# 📊 Džudo sacensību dalībnieku datu analizators

## 📝 Projekta uzdevums

Šī projekta mērķis ir izveidot Python rīku, kas automatizē datu iegūšanu no **JudoTV** mājaslapas par dažādām  džudo sacensībām. Lietotājs var norādīt konkrētu sacensību nosaukumu, un ko vēlās iegūt no piedāvātā opciju saraksta. Vai arī iegūt pilnīgi visu acensību sarakstu.


Projekta algoritms
- Iejiet mājaslapā un ielogojas iekšā ar izveidotu kontu, lai piekļūtu sacensībām.
- Sagaida uzdevumu no lietotāja
- Izpilda attiecīgo funkciju (Ja nepieciešams sagaida lietotāja ievadi atkārtotu)

## 🧰 Izmantotās Python bibliotēkas

Projektā tiek izmantotas šādas bibliotēkas:

| Bibliotēka       | Iemesls izmantošanai |
|------------------|----------------------|
| `selenium`       | Tiek izmantots, lai automatizētu pārlūka darbības, kā lapas atvēršanu, pogu nospiešanu un datu iegūšanu no dinamiskiem elementiem, kas mainās atkarībā no lapas novietojuma.. |
| `bs4 (BeautifulSoup)` | Tiek izmantota HTML dokumenta analizēšanai. Ļauj vienkārši iegūt visus bas. nepieciešamos elementus ar filtrēšanu, piemēŗam visas sacensī|
| `csv`            | Nodrošina iespēju lasīt datus no CSV faila (`events2025.csv`), kurā glabājas informācija par visām sacensībām. |
| `time`           | Tiek izmantota, lai nodrošinātu nelielas pauzes starp darbībām, lai lapa paspētu ielādēt datus pirms nākamāš darbīas. |

## 📦 Datu struktūras

Projektā izmantotas vairākas lietotāja definētas datu struktūras:

- **Sacensību ieraksts (dict no CSV)** – satur sacensību nosaukumu, datumu, kategoriju un saiti.
- **Dalībnieku dati (list of dicts)** – katrs dalībnieks tiek reprezentēts kā vārdnīca ar vārdu, uzvārdu, valsti un pasaules rangu.
- **Valstu saraksts (list)** – iegūts no sacensību valstu izvēlnes, lai zinātu, kuras valstis ir pārstāvētas.

## 🚀 Programmas izmantošana

1. Pārliecinieties, ka Jums ir uzstādīts `chromedriver` un `Google Chrome`.
2. Instalējiet nepieciešamās bibliotēkas:
   ```bash
    pip install selenium 
    pip install beautifulsoup4

