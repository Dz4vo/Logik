# Triedy
Program obsahuje triedy Button, Pin, Board, Game. Jednotlivé triedy zodpovedajú za objekty v hre, ktoré pomenúvajú, pričom trieda Game zabezpečuje celý chod hry.

## Game
Zabezpečuje chod hry. Volá funkcie, ktoré umožňujú, aby sa vykonali a vyhodnotili akcie hráča.
## Board
Graficky vykresľuje plochou kam sa ukladajú kolíky a priestor, kde sa kolíky ukladajú. 
Zodpovedná za tvorbu priestorov na ukladanie kolíkov, ich voľbu, kontrolu rozloženia  a porovnanie s hádanou postupnosťou. Zabezpečuje chod hry cez funkcie volané v triede Game

## Pin
Trieda reprezentujúca kolík. Má atribút polhy,farby a či bol odhalený. Pracuje sa s nimi hlavne vrámci funkcií triedy Board. 

## Button
Tlačidlo, ktoré spúšta mechaniku hintu.

## Zvyšok
Okrem týchto tried sa volajú úvodné funkcie na zadanie hodnôt čísel do konzoly alebo funkcie určené na porovnávanie postupností.
