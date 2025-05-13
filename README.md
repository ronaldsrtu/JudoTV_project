# Džudo sacensību dalībnieku datu analizators

## Projekta uzdevums

Šī projekta mērķis ir izveidot Python rīku, kas automatizē datu iegūšanu no **JudoTV** mājaslapas par dažādām  džudo sacensībām. Lietotājs var norādīt konkrētu sacensību nosaukumu, un ko vēlās iegūt no piedāvātā opciju saraksta. Vai arī iegūt pilnīgi visu sarakastu ar sacensībām, ar ko var tālāk strādāt.

## Projekta mērķis

Automatizēt un atvieglot piekļuvi sacensībām, lai treneriem un federācijām būtu vieglāk apstrādāt sportistu un sacensīu datus ar programmatūru.

Projekta algoritms
- Mājaslapas atvēršana un ielogošanās iekšā ar izveidotu kontu, lai piekļūtu sacensībām.
- Sagaida uzdevumu no lietotāja
- Izpilda attiecīgo funkciju (Ja nepieciešams sagaida lietotāja ievadi atkārtotu)

Izvēles opcijas:

1. Iegūt visu sacensību sarakstu
2. Iegūt cilvēku sarakstu noteiitā kateogrijā jebkurās sacensībās.
3. Iegūt TOP 10 cīkstoņus no acensībām. (Judo reitinga)
4. Iegūt sacensību valstu sarakstu.

## Izmantotās Python bibliotēkas

Projektā tiek izmantotas šādas bibliotēkas:

| Bibliotēka       | Iemesls izmantošanai |
|------------------|----------------------|
| `selenium`       | Tiek izmantots, lai automatizētu pārlūka darbības, kā lapas atvēršanu, pogu nospiešanu un datu iegūšanu no dinamiskiem elementiem, kas mainās atkarībā no lapas novietojuma.. |
| `bs4 (BeautifulSoup)` | Tiek izmantota HTML dokumenta analizēšanai. Ļauj vienkārši iegūt visus bas. nepieciešamos elementus ar filtrēšanu, piemēŗam visas sacensī|
| `csv`            | Nodrošina iespēju lasīt datus no CSV faila (`events2025.csv`), kurā glabājas informācija par visām sacensībām. |
| `time`           | Tiek izmantota, lai nodrošinātu nelielas pauzes starp darbībām, lai lapa paspētu ielādēt datus pirms nākamāš darbīas. |

## Datu struktūras

HashTable - domāts lai uzglabāt usacensības pēc to kategorijas (Cadets, Juniors...) Tas ļauj ātri meklēt un piekļūt sacensībām pēc kategorijas.

Competition klase- objekts, kas satur informāciju par vienām sacensībām. Sacensību nosaukums, datums un piekļuves saite.

CSV failā tiek saglabāti dati par visām 2025. gada sacensībām ar šādām kolonnām:

## Programmas izmantošana

1. Pārliecinieties, ka Jums ir uzstādīts `Google Chrome` pārlūkprogramma.
2. Instalējiet nepieciešamās izstrādes bibliotēkas:
   ```bash
    pip install selenium 
    pip install beautifulsoup4

