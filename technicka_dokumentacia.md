# Triedy
Program obsahuje triedy Button, Pin, Board, Game. Jednotlivé triedy zodpovedajú za objekty v hre, ktoré pomenúvajú, pričom trieda Game zabezpečuje celý chod hry.

## Game
Zabezpečuje chod hry. Volá funkcie , ktoré umožňujú, aby sa vykonali a vyhodnotili akcie hráča. Jednotlivé funkcie sú viazané na hráčov vstup cez stisknutie entru alebo kliknutie myše.

## Board
Graficky vykresľuje plochou kam sa ukladajú kolíky a priestor, kde sa kolíky ukladajú. Vytvára dátove štruktúry, kam sa ukladajú informácie o jednotlivých akciách hráča v priebehu hry.
Zodpovedná za tvorbu priestorov na ukladanie kolíkov, ich voľbu, kontrolu rozloženia  a porovnanie s hádanou postupnosťou. Zabezpečuje chod hry cez funkcie volané v triede Game.

## Pin
Trieda reprezentujúca kolík. Má atribút polohy,farby a či bol odhalený (týka sa kolíkov na vrcholu obrazovky, čo sa odhalia na konci hry). Pracuje sa s nimi hlavne vrámci funkcií triedy Board. Okrem toho nie sú viazané priamo naňho,žiadne funkcie.

## Button /Hint systém
Tlačidlo, ktoré spúšta mechaniku hintu. Vrámci hintu sú implentované 2 rôzne heuristiky. Táto hra patrí do triedy NP=ťažkých problémov, čiže prísť s rýchlym a zároveň algoritmom je náročné. V mechanike hintu je implemontovaná "rýchly" náhodný algoritmus, určený v situáciaách s dlhými postupnosťami a doposialľ ešte veľa validnými možnosťami. Tento algoritmus len overí, či daná postupnosť môže byť riešením na základe zatiaľ vykonaných tipov a vyberie z nich jeden náhodný. 

Druhý "pomalý" ale efektívnejší, čo sa počtu pokusov týka, je implementácia Knuthovho minimax-algoritmu, kde okrem vykonania overenia či je daná postupnosť vôbec ešte riešenie tak sa vyskúša koľko možností vyradí v najhoršom prípade, následne sa zo všetkých možných vyhovujúcich postupností vezme tá, ktorá má túto hodnotu najväčšiu.

## Zvyšok
Okrem týchto tried sa volajú úvodné funkcie na zadanie hodnôt čísel do konzoly alebo funkcie určené na porovnávanie postupností alebo vykonanie funkcie hintu.
