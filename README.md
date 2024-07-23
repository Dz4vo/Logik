# Logik
Implementácia známej logickej hry, kde je cieľom zistiť postupnosť na základe indícii.
Program je napísaný v jazyku Python prostredníctvom knižnice pygame, na jeho spustenie je potrebné mať tieto komponenty nainštalované. Spúšťa sa priamo spustením kódu v Pythone.

## Manuál na použitie
Po spustením programu je potrebné do konzole zadať dĺžku postupnosti a počet farieb z daného rozsahu. Po úspešnom zadaní sa zobrazí hracia plocha. Na jej spodku sú umiestnené farebné sú farebné kolíky. Kliknutím na ne si zvolíte danú farbu 
,ktorú môžete umiestniť do voľného miesta v rade, okolo ktorého je zelený rámček. Farbu umiestňovaných kolíkov viete si zmeniť kliknutím na farebný kolík inej farby. Farbu zapichnutého kolíka viete pred vyplnením celého radu zmeniť opätovným kliknutím s inou zvolenou farbou.

Ak ste vyplnili celý rad tak stlačením klávesy **ENTER** ho submitnete a konzole sa vám objavia dve čísla. Prvé hovorí koľko kolíkov ste umiestnili na správnu pozíciu a druhé hovorí koľko kolíkov správnej farby sa nachádza na nesprávnej pozícii.

Ak si neviete rady tak môžete stlačiť tlačidlo **HINT**, ktoré do konzoly vypíše postupnosť farieb, ktorá môže byť potenciálnym riešením na základe predošlých ťahov a výsledkov. Niekedy určenie hintu môže trvať zopár sekúnd.

V prípade, že sa Vám podarilo postupnosť v danom počte krokov uhádnuť, v konzole sa vypíše **Vyhrali ste** v opačnom prípade po minutí všetkých pokusov sa tam vypíše **Koniec hry**. Okno hry zavriete klikntím na  **X**  v pravom hornom rohu.





