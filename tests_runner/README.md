https://bytemeta.vip/repo/wapiti-scanner/wapiti/issues/268

try: poetry env use python3.11.0 or the full path to that python version

https://tecadmin.net/how-to-install-python-3-11-on-ubuntu/

https://linuxsecurity.com/features/complete-guide-to-using-wapiti-web-vulnerability-scanner-to-keep-your-web-applications-websites-secure

https://nabla-c0d3.github.io/sslyze/documentation/installation.html

```
poetry export -f requirements.txt --output requirements.txt
```

## namp test config

| opcja               | co robi                                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -v                  | Ustawia tryb verbose (rozszerzony), co oznacza, że ​​nmap będzie wypisywać więcej informacji podczas działania.                                                |
| -oX <filename>      |                                                                                                                                                                |
| --host-timeout=720s | Ustala maksymalny czas oczekiwania na odpowiedzi od hosta na 720s                                                                                              |
| -Pn                 | Wyłącza odbieranie pakietów ICMP (ping). Skanowanie będzie kontynuowane, nawet jeśli nie uzyska odpowiedzi na ping.                                            |
| -sC                 | Uruchania skrypty, które pozwalają dokładniej określić usługe                                                                                                  |
| --max-retries=1     | Ustala maksymalną liczbę prób ponownego wysłania pakietu do jednej skanowanej jednostki (np. hosta lub portu) na 1.                                            |
| -p1-65355           | Skanuje porty od 1 do 65355 (czyli wszystkie dostępne porty).                                                                                                  |
| -A                  | Włącza skanowanie "wszystkich funkcji" (wykrywanie systemu operacyjnego, skanowanie portów, skanowanie serwisów, skanowanie wersji, odkrywanie skryptów, ... ) |
| -sV                 | Wykrywa wersje serwisów na otwartych portach.                                                                                                                  |
