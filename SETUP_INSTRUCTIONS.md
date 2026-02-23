# Rutiranje - Vehicle Routing Problem Solver

Optimizacijski algoritmi za rješavanje problema rutiranja vozila (Vehicle Routing Problem - VRP).

## Zahtjevi

- **Python 3.8+** (testirano na Python 3.12.1)
- **Operacijski sustav**: Windows, Linux, macOS

## Instalacija Zavisnosti

### Brza instalacija (preporučeno)

#### Na Linux/macOS:
```bash
chmod +x setup.sh
./setup.sh
```

#### Na Windows:
Dvostruki klik na `setup.bat` ili u command promptu:
```cmd
setup.bat
```

#### Ili direktno s pip:
```bash
python3 -m pip install -r requirements.txt
```

### Ručna instalacija

Ako iznad navedeni koraci ne rade, instalirajte pakete pojedinačno:

```bash
# Excel datoteke
pip install openpyxl xlsxwriter

# Znanstveno računanje i optimizacija
pip install numpy scipy pulp

# JSON obrada
pip install simplejson

# Vizualizacija (opcionalno)
pip install matplotlib mplleaflet
```

## Potrebne Biblioteke

| Biblioteka | Verzija | Namjena |
|-----------|---------|---------|
| openpyxl | ≥3.11.0 | Čitanje/pisanje Excel datoteka |
| xlsxwriter | ≥3.1.9 | Pisanje Excel datoteka |
| numpy | ≥1.24.0 | Numeričke operacije |
| scipy | ≥1.10.0 | Udaljenosti i matematička funkcionalnost |
| pulp | ≥2.8.0 | Linearna optimizacija |
| simplejson | ≥3.19.0 | JSON obrada |
| matplotlib | ≥3.8.0 | Vizualizacija ruta (opcionalno) |
| mplleaflet | ≥0.11.0 | Kartografska vizualizacija (opcionalno) |

## Startanje Programa

Nakon instalacije zavisnosti, pokrenite program:

```bash
python3 main.py
```

## Struktura Projekta

- **main.py** - Glavna datoteka programa
- **requirements.txt** - Lista svih potrebnih Python paketa
- **setup.sh** - Instalacijski script za Linux/macOS
- **setup.bat** - Instalacijski script za Windows
- **setup_dependencies.py** - Python instalacijski script

## Clark-Wright Algoritmi

Projekt koristi sljedeće module za rješavanje VRP:
- `clarkWright.py` - Clarke-Wright algoritam za razvoz
- `clarkWrightPovrat.py` - Clarke-Wright algoritam s povratom
- `clarkModul.py` - Clark modul za optimizaciju
- `clarkModul2.py` - Clark modul V2 s poboljšanjima

## LP Optimizacija

- `LPprogrami1.py` - Linearni program za odabir ruta
- `LPprogrami1Primjer.py` - Primjer LP programa
- `LPprogrami1aPrimjer.py` - LP program s ograničenjima

## Obrada Podataka

- `ulazniPodaciPrimjer.py` - Unos i obrada ulaznih podataka
- `postavkaUlaza.py` - Konfiguracija ulaznih parametara
- `postavkaUlazaNac.py` - Konfiguracija za nacionalne rute

## Vizualizacija

- `crtaj_rute.py` - Vizualizacija izračunatih ruta

## Verzija Python

Program je konvertovan s Python 2.7 na Python 3 s sljedećim promjenama:
- print statement → print() funkcije
- xrange → range
- __cmp__ → __lt__ metode
- Tabs → Spaces indentacija

## Licence i Zavisnosti

Provjerite licencije sljedećih biblioteka prije komercijalnog korištenja:
- PuLP - Open Source (CBC/CPLEX konfiguracija)
- SciPy - BSD licenca
- NumPy - BSD licenca
- Matplotlib - Matplotlib licenca
- openpyxl - MIT licenca

## Troubleshooting

### ModuleNotFoundError: No module named 'openpyxl'
Pokrenite instalacijski script:
```bash
python3 setup_dependencies.py
```

### PuLP solver nije dostupan
PuLP ide s CBC solverom. Za CPLEX ili CPLEX solverom, pratite upute na https://github.com/coin-or/pulp

### Problemi s datotekama na Windows
Programi koriste forward slashes (/) umjesto backslashes (\) za kompatibilnost cross-platform.

## Kontakt i Podrška

Za pitanja i probleme, kontaktirajte razvojni tim.
