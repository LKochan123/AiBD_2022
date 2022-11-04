Oryginalny plik weather.txt zawiera dane pogodowe dla jednej stacji w Meksyku (MX17004).
Poszczególne dane w odpowiednich kolumnach:

-   id stacji, rok i miesiąc pomiaru, oraz informacja czego jest to pomiar [tmax, tmin, prcp] (1 kolumna)
-   wyniki danego pomiaru w kolejnych dniach miesiąca oddzielone separatorem "I"

Problemy istniejące w tabeli:

-   tmax, tmin odpowiednie podzielone przez 10 dadzą wynik w stopniach celcjuszach
-   daną "-9999" zakładamy jako błędny pomiar
-   różne separatory między danymi np. spacja, znak "I" lub znak "S"
-   różna ilość kolumn dla poszczególnych rekordów z powodu różnej ilośći dni w każdym miesiącu
