# Projekt Betterize


### vue3-circle-progress custom component

Ten komponent implementowany jest w repozytorium: [AddCubeDev/vue3-circle-progress.git](https://github.com/AddCubeDev/vue3-circle-progress.git).

Aby poniższe skrypty zadziałały musisz mieć zainstalowany program [Nushell](https://www.nushell.sh).

Jeżeli jeszcze nie sklonowałeś tego repozytorium, to możesz to zrobić w następujący sposób:
```
npm run clone-circle-progress
```
Projekt zostanie sklonowany w katalogu: ../vue3-circle-progress
```
./betterize             <- katalog tego projektu
./vue3-circle-progress  
```

Jeżeli chcesz mieć pewność, że katalog ../vue3-circle-progress zawiera
najnowszą wersję, to uruchom następującą komendę:
```
npm run pull-circle-progress
```

Reinstalacja pakietów (np. musiałeś skasować katalog node_modules, bo coś się nie kompilowało):
```
npm run reinstall
```

### vanilla-tilt

W obecnej implementacji pakiet 'vanilla-tilt' jest używany tylko na desktop-ach
i jest ładowany warunkowo (patrz: index.astro), dlatego pakiet został usunięty z 
pliku package.json (npm uninstall vanilla-tilt; bieżąca wersja to: 1.8 )
i jego wersja .min została umieszczona w katalogu /public/scripts/vanilla-tilt.min.js.
