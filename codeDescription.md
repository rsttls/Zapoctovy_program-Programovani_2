# Popis kódu
## Main
Pro pole buňek používáme `defaultdict`. Výpočetně je to náročnejší než `array`, ale umožňuje to "nekonečné" pole, ulehčuje dynamickou alokaci a nemusíme používat jiné datové struktury na uložení živých buňek.

Hlavní pole (`fieldCurrent`) v průběhu simulace obsahuje jen živé buňky a tedy můžeme pole projít pomocí klíčů. Následně podle pravidel hry ukládáme do nového pole (`fieldNew`) jen živé buňky (odtud se odvijí, že hlavní pole má jen žívé buňky). Pro zobrazení nového pole jen prohodíme reference na objekty.

Pro aplikaci pravidel simulace procházíme jen živé buňky a díváme se na ně a jejich sousedy. Všechny zbylé buňky jsou mrtvé a mají 0 sousedů.


Hlavní funkce je rozdělena do 3 sekcí: event, update a draw. 
### `event`
 zpracovává různé události (vypnutí hry, změna velikosti okna, vstup). Vstup je rozdělen to dvou částí. První část je pro jednorázový vstup a druhá část je pro spojitý vstup.
### `update`
je zodpovědný za simulaci hry a je spouštěn v zavisloti na `cyclePeriod`, kde `cyclePeriod` udává v milisekundách minimální čas než se update může zavolat.
### `draw`
je zodpovědný za vykreslování do okna v intevalu `frametime`. Výchozí nastavení `frametime` je 16.666 milisekund, což je přbližně 60fps.

## Třídy
### `cellSingleton`
Zjednodušuje načítání a kreslení buňek.

### `gridSingleton`
Zjednodušuje načítání a kreslení mřížky.

### `textSingleton`
Zjednodušuje kreslení textu.

## Funkce
### `visibleCell`
Funkce vrací dva intevaly viditelných buňek.
### `numberOfNeighbors`
Funkce vrací počet živých buňek kolem buňky[x][y]
### `applyLogic`
Funkce aplikuje pravidla simulace na buňku[x][y]
