/*1. crearea unui set de date SAS din fișiere externe;*/
data date1;
    infile '/home/u64205077/PROIECT/SET_DE_DATE_WALMART_PS.txt' dlm='09'x dsd firstobs=2;
    input Store Date : ddmmyy10. Weekly_Sales Holiday_Flag Temperature CPI Unemployment;
    format Date ddmmyy10.;
run;

proc print data=date1;
run;

data date2;
    infile '/home/u64205077/PROIECT/SET_DE_DATE_WALMART_PS_2.txt' dlm='09'x dsd firstobs=2;
    input Store Fuel_Price;
run;

/*2. crearea și folosirea de formate definite de utilizator;
4. crearea de subseturi de date;
6. combinarea seturilor de date prin proceduri specifice SAS și SQL;*/

proc print data=date2;
run;

proc format;
    value formatare
        1 = 'E sarbatoare'
        0 = 'Nu e sarbatoare';
run;

data date_format;
    set date1;
    format Holiday_Flag formatare.;
run;

proc print data=date_format;
run;

proc sql;
    create table jonctiune as
    select a.*, b.Fuel_Price
    from date_format a
    inner join date2 b
    on a.Store = b.Store;
quit;

proc print data=jonctiune;
run;

/*3. Procesare iterativă și condițională */
data vanzari;
    set jonctiune;
    length Tip_vanzare $10;
    if Weekly_Sales > 2000000 then Tip_vanzare = "Ridicat";
    else if Weekly_Sales > 1000000 then Tip_vanzare = "Mediu";
    else Tip_vanzare = "Mic";
run;

proc print data=vanzari;
run;

/*7. Utilizarea de masive*/
data masiv;
    set jonctiune;
    array temp[1] Temperature;
    array tempC[1] Temperatura_Celsius;
    do i = 1 to 1;
        tempC[i] = (temp[i] - 32) * 5 / 9;
    end;
    drop i;
run;

proc print data=masiv;
run;

/*5. utilizarea de funcții SAS;
8. utilizarea de proceduri pentru raportare;
9. folosirea de proceduri statistice
10.generarea de grafice.*/

data luna_mai;
    set masiv;
    where month(Date) = 5;
run;

proc UNIVARIATE data=luna_mai;
    var Weekly_Sales;
    histogram Weekly_Sales;
run;

PROC MEANS DATA = jonctiune;    
   BY Store;    
   VAR Fuel_Price;
   TITLE 'Raportul pretului la combustibil per magazin';
RUN;

TITLE "Evolutia in timp a vanzarilor saptamanale";
 PROC GPLOT data=jonctiune;
    by Store;
 	PLOT Weekly_Sales * Date;
RUN;
QUIT;
