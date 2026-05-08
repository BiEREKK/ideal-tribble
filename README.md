# Prosty Skaner IP

Skrypt w języku Python służący do skanowania sieci lokalnej pod kątem aktywnych urządzeń (hostów) przy użyciu standardowego narzędzia systemowego `ping`.

## Cel programu
Narzędzie pozwala administratorom sieci oraz pasjonatom w łatwy sposób sprawdzić, które adresy IP w danej podsieci są aktualnie używane i odpowiadają na żądania ICMP. Program może działać automatycznie, wykrywając lokalną podsieć, lub skanować ręcznie wprowadzony zakres.

## Wymagania
* Python w wersji 3.6 lub nowszej.
* System operacyjny posiadający wbudowane narzędzie `ping` w zmiennych środowiskowych (Windows, Linux, macOS).
* Wbudowane biblioteki Pythona (nie ma potrzeby instalowania dodatkowych pakietów z `pip`).

## Argumenty CLI

| Argument | Opis |
| --- | --- |
| `--network` | Pozwala zdefiniować konkretną sieć do skanowania w formacie CIDR (np. `10.0.0.0/24`). Jeśli nie podano, program spróbuje automatycznie wykryć domyślną sieć. |
| `--output` | Ścieżka do pliku tekstowego, w którym zostaną zapisane sformatowane wyniki skanowania. |
| `-h`, `--help` | Wyświetla pomoc i opis dostępnych parametrów. |

## Przykłady uruchomienia

**1. Skanowanie automatyczne (bez argumentów)**
Program spróbuje wykryć Twoją główną kartę sieciową i automatycznie przeskanuje maskę `/24`.
```bash
python3 IPSkan.py
**2. Skanowanie konkretnej sieci**
```bash
python3 IPSkan.py --network 192.168.0.0/24
**3. Skanowanie z zapisem wyników do pliku**
python3 IPSkan.py --network 192.168.0.0/24 --output aktywne_hosty.txt
