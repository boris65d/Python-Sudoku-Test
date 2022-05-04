

import random as rnd
import sys
import datetime
from timeit import default_timer as timer
import pygame as pg
import pygamebg

# pyinstaller --onefile sudoku.py ****** this is how to make sudoku.exe ********** ovako se pravi sudoku.exe
pg.init()  # ********** initijalize modul pygame ********************
#  ****** button ******  dugme  ************************** treba napraviti efitor za postavlanje dugmadi na ekran ***********
#  ****** button ******  dugme  ************************** to do: make editor for seting buttons on screen ***********
dugmad = [[0, 0, 0, " ", 0, False, 0, 0, ""],
          [1, 590, 100, "  Nova igra  ", 18, False, 1, 1, "nova_igra()"],
          [2, 590, 160, " - ", 22, False, 1, 1, "set_tezina(-1)"],
          [3, 696, 160, " + ", 22, False, 1, 1, "set_tezina(1)"],
          [4, 667, 500, " Kraj ", 18, False, 1, 1, "pg.quit()"],  # *** quit() needs repair, have error .
          [15, 590, 460, "   Rešenje   ", 18, False, 1, 1, "resi(70,70)"],
          [16, 590, 430, "  Iz početka ", 18, False, 1, 1, "iz_pocetka(70,70)"],
          [14, 590, 400, "   Brisanje  ", 18, False, 1, 1, "brisanje()"],
          [17, 590, 500, " Save ", 18, False, 1, 1, "saveslika()"],
          [18, 590, 540, " Retro XP  ", 18, False, 1, 1, "retro()"],
          [5, 590, 220, " 1 ", 24, False, 1, 1, "set_broj(1)"],
          [6, 640, 220, " 2 ", 24, False, 1, 1, "set_broj(2)"],
          [7, 690, 220, " 3 ", 24, False, 1, 1, "set_broj(3)"],
          [8, 590, 255, " 4 ", 24, False, 1, 1, "set_broj(4)"],
          [9, 640, 255, " 5 ", 24, False, 1, 1, "set_broj(5)"],
          [10, 690, 255, " 6 ", 24, False, 1, 1, "set_broj(6)"],
          [11, 590, 290, " 7 ", 24, False, 1, 1, "set_broj(7)"],
          [12, 640, 290, " 8 ", 24, False, 1, 1, "set_broj(8)"],
          [13, 690, 290, " 9 ", 24, False, 1, 1, "set_broj(9)"]]

prozor = 0
(sirina, visina) = (800, 600)  # ***** Dimnzije prozora
# treba napraviti da se prilagođava raznim rezolucijama ekrana *****************************
rub = 10
sik = 50
k = 0
t_kol = 0
t_red = 0
tezina = 6
x = y = 0
start_i = end_i = 0
# ****** paleta boja ****************
BOJA_PODLOGE = [150, 150, 180]
SVETLA_IVICA = [255, 255, 255]
TAMNA_IVICA = [0, 0, 0]
BOJA_ZADATOG = [245, 220, 220]
BOJA_ISPONOVO = [200, 255, 200]
BOJA_RESI = [200, 200, 255]
BOJA_BROJA = [220, 130, 185]
BOJA_REDKOL = [255, 190, 205]
BOJA_BRIS = [255, 55, 255]
# zašto su boje vidljive i bez deklaracije global iako su to zapravo varijable velikim slovima ?
retro_stil = True
prozor = pygamebg.open_window(sirina, visina, "Sudoku Python SudoPyr")
# bojimo pozadinu prozora u svetlo sivo, világos szúrke
prozor.fill(pg.Color(BOJA_PODLOGE))

# ********* niz (array) nizova koji sadrži brojčanu matricu sudokua ***************
sudo = [[0 for i in range(9)] for j in range(9)]
sud_x = [[0 for i in range(9)] for j in range(9)]
# ********* niz (array) nizova koji sadrži tekstualnu (string) matricu sudokua ***************
sudos = [[" " for i in range(9)] for j in range(9)]

# *************** ovo je prazna funkcija za dugme **************
def uradi():
    pass

# *************** ovde se matrica puni brojevima 1-9 svaki red, kolona i polje 3x3 sadrži sve cifre 1-9
def osnovna():  # ***** ovde se genriše rešen sudoku, jako jednostavan, uvek isti, samo jedan *********
    global sudo  # ****** Od ovoga je sve počelo ********************
    # print("osnovna")               # ***** mogao sam ga napisati i napamet
    for i in range(9):               # 123 456 789
        for j in range(9):           # 456 789 123
            if i < 3:                # 789 123 456
                k = i * 3 + j        # 912 345 678
            if 3 <= i < 6:           # 345 678 912
                k = i * 3 + j + 8    # 678 972 345
            if i >= 6:               # 567 891 234
                k = i * 3 + j + 4    # 891 234 567
            k = k % 9                # 234 567 891
            sud_x[i][j] = sudo[i][j] = k + 1  # **** ali ga ne znam rešiti
        # print(sudo[i])

"""
def osnovnaxx():   # **************** ovo je bilo samo za probu
    global sudo
    print("osnovna")
    for i in range(9):
        for j in range(9):
            sudo[i][j] = j+1
        print(sudo[i])
"""

# ********** funkcija koja menja mesta svih pojava dva broja u matrici sudo *******************
def zamena(a, b):  # mislim da bi ovo moglo bez posrednika ali ne znam još   *****************
    global sudo  # mešaju se brojevi da bi sudoku izgledao drugačije svaki put **********
    # print("zameni ", a, "za", b)
    for i in range(9):
        for n, k in enumerate(sudo[i]):
            if k == a:
                sudo[i][n] = 0
        for n, k in enumerate(sudo[i]):
            if k == b:
                sudo[i][n] = a
        for n, k in enumerate(sudo[i]):
            if k == 0:
                sudo[i][n] = b


# ovde se matrica transponuje (redovi postaju kolone a kolone redovi da bi sudoku izgledao drugačije ****************
def transpon():
    global sudo, sud_x
    # print("transponovana")
    if rnd.randint(0, 9) > 5:  # ali ne svaki put.
        for i in range(9):
            for j in range(9):
                sudo[i][j] = sud_x[j][i]

def prevrni():  # *********************** ovde prvi red postaje poslednji, drugi - predposlednji...
    global sudo, sud_x  # isto da bi izgledao drugačije  ****************
    if rnd.randint(0, 9) > 5:  # ali ne svaki put.
        for i in range(5):
            sudo[i], sudo[8 - i] = sudo[8 - i], sudo[i]

# ********* ovde s izbacuju brojevi iz matrice da bi se imalo šta rešavati ***********
# ******************** i brojevi se pretvaraju u tekst da bi se mogli lepo odštampati
def izbaci(a):
    global sudo, sud_x, sudos
    for i in range(9):
        # print("+++++", sudo[i])
        for j in range(9):
            b = rnd.randint(1, 9)
            if b <= a:
                sudos[i][j] = " "
                sud_x[i][j] = 0
            else:
                sudos[i][j] = str(sudo[i][j])
                sud_x[i][j] = sudo[i][j]

def prikaz():  # za potrebe tekstualnog prikaza sudokua, sada se ne poziva u program, ali je zanimljivo
    # kako python radi sa stringovima  ** ovde se stringovi spajaju pomoću for petlje ************************
    global sudos
    print("  ┌───┬───┬───╦───┬───┬───╦───┬───┬───┐")
    for i in range(9):
        reds = "  │ "
        for j in range(9):
            if j == 2 or j == 5:
                reds += sudos[j][i] + " ║ "
            else:
                reds += sudos[j][i] + " │ "
        # reds += "│"
        print(reds)
        if i == 2 or i == 5:
            print("  ├═══╪═══╪═══╫═══╪═══╪═══╫═══╪═══╪═══╡")
        else:
            if i < 8:
                print("  ├───┼───┼───╫───┼───┼───╫───┼───┼───┤")
            else:
                print("  └───┴───┴───╩───┴───┴───╩───┴───┴───┘")

def xprikaz():  # za potrebe tekstualnog prikaza sudokua, sada se ne poziva u program, ali je zanimljivo
    # kako python radi sa stringovima  ** ovde se stringovi spajaju pomoću .join metode *********
    global sudos
    print("  ┌───┬───┬───╦───┬───┬───╦───┬───┬───┐")
    for i in range(9):
        print("  │", " │ ".join(sudos[i][:3:]), "║", " │ ".join(sudos[i][3:6:]), "║", " │ ".join(sudos[i][6:9:]), "│")
        if i == 2 or i == 5:
            print("  ├═══╪═══╪═══╫═══╪═══╪═══╫═══╪═══╪═══╡")
        else:
            if i < 8:
                print("  ├───┼───┼───╫───┼───┼───╫───┼───┼───┤")
            else:
                print("  └───┴───┴───╩───┴───┴───╩───┴───┴───┘")

# *************upisuje sudoku u fajl "sudopyr.txt"***********************************************************
def upisi():  # isto se zasada ne poziva
    global sudo, sudos
    original_stdout = sys.stdout  # Save a reference to the original standard output
    with open("sudopyr.txt", 'a') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        print('Sudoku Python SudoPyr')
        prikaz()
        sys.stdout = original_stdout  # Reset the standard output to its original value
    f.close()

# ************** dali se broj vec nalazu u datom redu ili koloni ili kvadratu ***************************
def ima_vec(sta, kol, red):
    global sudos
    for i in range(9):  # ******** ovde se proverava red i kolona ****************
        if sudos[kol][i] == sta or sudos[i][red] == sta:
            return True
    s1 = kol // 3  # ********* ovde se proverava da li ima u kvadratu *************
    s2 = red // 3
    for i in range(3):
        for j in range(3):
            if sudos[s1 * 3 + i][s2 * 3 + j] == sta:
                return True
    return False

# ***************** ovde se polje popunjava brojevima ************************************************************
def ubaci(x, y):
    global sudo, sud_x, sudos, t_kol, t_red, sik
    for i in range(9):
        for j in range(9):
            if sud_x[i][j] == 0:
                boja = BOJA_PODLOGE
            else:
                boja = BOJA_ZADATOG
            pg.draw.rect(prozor, pg.Color(boja),
                         (x + i * sik + 3, y + j * sik + 3, sik - 4, sik - 4))
            tekst_centar(i * sik + x + (sik / 2), j * sik + y + (sik / 2), sudos[i][j], 24)

# **************************************** ovde se ide iz početka ****************************************
def iz_pocetka(x, y):  # ******* ako zabrljaš jako, možeš iz početka  **************
    global sudo, sud_x, sudos, t_kol, t_red, sik
    # sudos = [[" " for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            if sud_x[i][j] == 0:
                sudos[i][j] = " "
                pg.draw.rect(prozor, pg.Color(BOJA_ISPONOVO),
                             (x + i * sik + 3, y + j * sik + 3, sik - 4, sik - 4))
                tekst_centar(i * sik + x + (sik / 2), j * sik + y + (sik / 2), sudos[i][j], 24)

# **************************************** ovde se prikazuje rešenje ****************************************
def resi(x, y):
    global sudo, sud_x, sudos, t_kol, t_red, sik
    # sudos = [[" " for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            if sud_x[i][j] == 0:
                sudos[i][j] = str(sudo[i][j])
                pg.draw.rect(prozor, pg.Color(BOJA_RESI),
                             (x + i * sik + 3, y + j * sik + 3, sik - 4, sik - 4))
                tekst_centar(i * sik + x + (sik / 2), j * sik + y + (sik / 2), sudos[i][j], 24)

    if jeli_gotovo():
        tekst_box(50, 550, ' ************* Evo rešenja! **************** ', 18, True)
        pg.display.update()
        pg.time.wait(3000)

# ************************ ovde se crta polje za igru sudoku 9x9 **********************************************
def polje(x, y):
    ram(rub, rub, sirina - rub * 2, visina - rub * 2, False, True, BOJA_PODLOGE)
    ram(rub * 2, rub * 2, sirina - rub * 4, visina - rub * 4, True, False, BOJA_PODLOGE)
    # ram(x-5,y-5,x+sik*7+10,y+sik*7+10, False, False,[120, 120, 255])
    ram(x - 18, y - 18, x + sik * 8 + 18, y + sik * 8 + 18, False, False, BOJA_PODLOGE)

    tekst_box(590, 60, " 00:00 ", 20, True)
    tekst_box(50, 550, "                                             ", 18, True)
    tekst_box(590, 130, "   Težina    ", 18, False)
    tekst_box(645, 160, " " + str(tezina) + " ", 20, False)
    tekst_box(640, 345, " " + str(k) + " ", 24, False)
    tekst_box(100, 24, " Sudoku v1.2 by B&D Soft On The Pump ", 16, False)
    for i in range(10):  # ******** ovde se crta mrežica za sudoku sa podebljanim linijama za kvadrate *****
        if i == 3 or i == 6:
            deb = 4
        else:
            deb = 2
        pg.draw.line(prozor, pg.Color("black"), (x, i * sik + y), (x + sik * 9, i * sik + y), deb)
        pg.draw.line(prozor, pg.Color("black"), (i * sik + x, y), (i * sik + x, y + 9 * sik), deb)

# **************** ova funkcija se izvršava stalno u petlji kada nema događaja ***********************
def novi_frejm():  # karakteristika modula pygame *** meni crta sat ***************************
    global t_red, t_kol, sudos, sik, rub, k, tezina, start_i, end_i, x0, y0, x, y
    sat = str(datetime.datetime.now())  # prikazuje sat ...   *************
    tekst_box(650, 25, sat[10:19] + " ", 20, True)

# ****** ovde se menja globalna varijabla tezina koja određuje koliko če se brojeva izbaciti
# ******* treba napraviti ravnomernu raspodelu po kvadratima .... *************************************************
def set_tezina(a):
    global tezina
    tezina = tezina + a
    if tezina < 1:
        tezina = 1
    if tezina > 9:
        tezina = 9
    tekst_box(645, 160, " " + str(tezina) + " ", 20, False)
    izbaci(tezina)

# ************************** ovde program reaguje na komande miša (i tastature, u budućnosti, za sada samo miš ) **********************
def obradi_dogadjaj(dogadjaj):
    global t_red, t_kol, sudos, sik, rub, k, tezina, start_i

    if dogadjaj.type == pg.MOUSEBUTTONDOWN:
        (xm, ym) = dogadjaj.pos
        tekst_levo(500, 25, "x" + str(xm) + "  y" + str(ym), 18)
        t_kol = int((xm + 30) / sik) - 1  # ***** ubačena korekcija da se pogodi polje (30)
        t_red = int((ym + 30) / sik) - 1  # ***** ubačena korekcija da se pogodi polje (30)
        tekst_levo(25, 25, "C" + str(t_kol) + " R" + str(t_red),
                   18)  # **** korekcija treba da je vezana za poziciju polja
        a = test_dugme(xm, ym, True)  # ***** koje je dugme pritisnuto ?  *************
        tajmer(True)
        ubaci(70, 70)  # ********** ispisuje polje za igru sa brojevima, osvežava prikaz   ***********
        polje_igre(70, 70)

# ***** koji broj želiš ubaciti u polje ? *********
def set_broj(a):
    global k
    k = a
    tekst_box(640, 345, " " + str(a) + " ", 24, False)
    proveri(a, 70, 70)  # ****** ovde obeleži sve pojave broja k u sudokuu ************

# **************************************** brisanje *****************************
def brisanje():
    global t_red, t_kol, sudos, sik, rub, k
    k = 0
    tekst_box(640, 345, "   ", 24, False)


# *************** polje za igru *************************************************
def polje_igrex():  # ova procedura ima bag, prikazuje X preko broja u poslednjoj pojavi broja u matrici *******
    global t_red, t_kol, sudos, sik, rub, k, BOJA_PODLOGE  # ne poziva se više ali mi je žao obrisati
    # da li su kordinate miša u granicama polja i dali je u polje dozvoljeno brisati i pisati
    if 0 < t_kol < 10 and 0 < t_red < 10 and sud_x[t_kol - 1][t_red - 1] == 0:
        if ima_vec(str(k), t_kol - 1, t_red - 1) and k != 0:  # *******  ne može !  ******
            tekst_centar((t_kol + 1.5) * sik, (t_red + 1.5) * sik, "X", 24)
        else:
            if k != 0:  # ******** upis u polje ************************************
                tekst_centar((t_kol + 1.5) * sik, (t_red + 1.5) * sik, str(k), 24)
                sudos[t_kol - 1][t_red - 1] = str(k)
            else:  # ******** ovo je zapravo brisanje ***************************
                pg.draw.rect(prozor, pg.Color([255, 55, 255]),
                             ((t_kol + 1) * sik + 3, (t_red + 1) * sik + 3, sik - 4, sik - 4))
                pg.display.update()
                sudos[t_kol - 1][t_red - 1] = " "
                pg.time.wait(200)
                pg.draw.rect(prozor, pg.Color(BOJA_PODLOGE),
                             ((t_kol + 1) * sik + 3, (t_red + 1) * sik + 3, sik - 4, sik - 4))

# *************** polje za igru ******* ispravljena greška *********************************************************************
def polje_igre(x, y):  # ***** verovatno bi se noglo skratiti a da bude bez greške *******
    global t_red, t_kol, sudos, sud_x, sik, k, BOJA_PODLOGE
    # i dali je u polje dozvoljeno brisati i pisati
    if 0 < t_kol < 10 and 0 < t_red < 10:  # da li su kordinate miša u granicama polja
        if k != 0:  # upisati broj
            if sudos[t_kol - 1][t_red - 1] == " ":  # # ako je polje prazno
                if ima_vec(str(k), t_kol - 1, t_red - 1):  # *** ako nije ****  ne može !  ******
                    tekst_centar((t_kol - 1) * sik + x + (sik / 2), (t_red - 1) * sik + y + (sik / 2), "X", 24)
                else:  # ******** upis u polje ************************************
                    tekst_centar((t_kol - 1) * sik + x + (sik / 2), (t_red - 1) * sik + y + (sik / 2), str(k), 24)
                    sudos[t_kol - 1][t_red - 1] = str(k)
                    # *********** ako upišeš broj u matricu možda je poslednji pa proveri jeli gotovo ************
                    if jeli_gotovo():  # ******* ovo je provera da li je sudoku ispravno popunjen ******************
                        tekst_box(50, 550, " ********* Gotovo je! Uspeo si !!! ********* ", 18, True)
                        tajmer(True)
                        pg.display.update()
        else:  # ******** ovo je zapravo brisanje ***************************
            if sud_x[t_kol - 1][t_red - 1] == 0:
                pg.draw.rect(prozor, pg.Color([255, 55, 255]),
                             (x + (t_kol - 1) * sik + 3, y + (t_red - 1) * sik + 3, sik - 4, sik - 4))
                pg.display.update()
                sudos[t_kol - 1][t_red - 1] = " "
                pg.time.wait(200)
                pg.draw.rect(prozor, pg.Color(BOJA_PODLOGE),
                             (x + (t_kol - 1) * sik + 3, y + (t_red - 1) * sik + 3, sik - 4, sik - 4))

# ************************** ovde se markiraju sve pojave nekog broja u polju *******************************
def proveri(sta, x, y):
    global sik, sudo, sud_x, sudos, t_kol, t_red, end_i, start_i
    for i in range(9):
        for j in range(9):
            if str(sta) == sudos[i][j]:
                (t_kol, t_red) = (i + 1, j + 1)
                pg.draw.rect(prozor, pg.Color(BOJA_BROJA),
                             (x + (t_kol - 1) * sik + 3, y + (t_red - 1) * sik + 3, sik - 4, sik - 4))
                tekst_centar((t_kol - 1) * sik + x + (sik / 2), (t_red - 1) * sik + y + (sik / 2),
                             sudos[t_kol - 1][t_red - 1], 24)
                (p_red, p_kol) = (t_red, t_kol)
                for l in range(9):
                    t_kol = l + 1
                    if t_kol == p_kol:
                        continue
                    pg.draw.rect(prozor, pg.Color(BOJA_REDKOL),
                                 (x + (t_kol - 1) * sik + 3, y + (t_red - 1) * sik + 3, sik - 4, sik - 4))
                    tekst_centar((t_kol - 1) * sik + x + (sik / 2), (t_red - 1) * sik + y + (sik / 2),
                                 sudos[t_kol - 1][t_red - 1], 24)
                pg.display.update()
                (t_red, t_kol) = (p_red, p_kol)
                for l in range(9):
                    t_red = l + 1
                    if t_red == p_red:
                        continue
                    pg.draw.rect(prozor, pg.Color(BOJA_REDKOL),
                                 (x + (t_kol - 1) * sik + 3, y + (t_red - 1) * sik + 3, sik - 4, sik - 4))
                    tekst_centar((t_kol - 1) * sik + x + (sik / 2), (t_red - 1) * sik + y + (sik / 2),
                                 sudos[t_kol - 1][t_red - 1], 24)
                (t_red, t_kol) = (p_red, p_kol)
                pg.display.update()
    pg.time.wait(1500)

# ************* tajmer *****************************************************************
def tajmer(sta):
    global start_i, end_i
    if sta:
        end_i = timer()
        vreme = int(end_i - start_i)
        v_sec = ("00" + str(vreme % 60))[-2:]
        v_min = ("00" + str((vreme // 60) % 60))[-2:]
        vremes = v_min + ":" + v_sec
        tekst_box(590, 60, " " + vremes + " ", 20, True)
    else:
        start_i = timer()

# ********* gotovo je ** ne poziva se, stoji tu za primer skraćenja *****************************************
def xjeli_gotovo():  # ********** sudoku je gotov ako :
    global t_red, t_kol, sudos
    for i in range(9):  # nema praznih polja i ...
        for j in range(9):
            if sudos[i][j] == " ":
                return False
    for i in range(9):  # **** zbir svakog reda i kolone je 45
        a = 0
        for j in range(9):
            a = a + int(sudos[i][j])  # **** zbir svake kolone
        if a != 45:
            return False
    for i in range(9):
        a = 0
        for j in range(9):
            a = a + int(sudos[j][i])  # **** zbir svakog reda
        if a != 45:
            return False
    return True  # ******* očigledno je da se može napisati kraće !!!
# ********* gotovo je ** ne poziva se, stoji tu za primer skraćenja *****************************************
def yjeli_gotovo():  # ********** sudoku je gotov ako :
    global t_red, t_kol, sudos
    for i in range(9):  # nema praznih polja i ...
        for j in range(9):
            if sudos[i][j] == " ":
                return False
    for i in range(9):  # **** zbir svakog reda i kolone je 45
        a = b = 0
        for j in range(9):
            a = a + int(sudos[i][j])  # **** zbir svake kolone
            b = b + int(sudos[j][i])  # **** zbir svakod reda
        if a != 45 or b != 45:
            return False
    return True  # *******  skraćena verzija !!! a može još kraće!!!!!!!

def jeli_gotovo():  # ********** sudoku je gotov ako :
    global t_red, t_kol, sudos
    for i in range(9):  # nema praznih polja i ...
        a = b = 0
        for j in range(9):
            if sudos[i][j] == " " or sudos[j][i] == " ":
                return False
            a = a + int(sudos[i][j])  # **** zbir svake kolone
            b = b + int(sudos[j][i])  # **** zbir svakod reda
        if a != 45 or b != 45:  # **** zbir svakog reda i kolone je 45
            return False
    return True  # *******  skraćena verzija 2!!!



# ********************************************************************************************
# *************** crta ram sa svetlim i tamnim ivicama da bi izgledao 3D
# **************** sada je uklopljena sa drugim retro stilom  *** ne poziva se više *******
def yram(x, y, s, v, utis, p, boja):  # pozicija gornjeg levog ugla, širina, visina, dali je utisnut ili ne,
    # dali farba pozadinu i kojom bojom  **************
    if p:
        pg.draw.rect(prozor, pg.Color(boja), (x, y, s, v), 0, 10)
    if not utis:
        (boja1, boja2) = (SVETLA_IVICA, TAMNA_IVICA)
    else:
        (boja2, boja1) = (SVETLA_IVICA, TAMNA_IVICA)

    pg.draw.rect(prozor, pg.Color(boja2), (x + 1, y + 1, s, v), 1, 10)
    pg.draw.rect(prozor, pg.Color(boja1), (x - 1, y - 1, s, v), 1, 10)
    pg.draw.rect(prozor, pg.Color(boja), (x, y, s, v), 2, 10)

    pg.display.update()

# ********************************************************************************************
def retro():  # ******* treba napraviti da igra ostane ista kada se menja stil ------***********
    global retro_stil
    retro_stil = not retro_stil
    if retro_stil:
        dugmad[9][3] = " Retro XP "
    else:
        dugmad[9][3] = " Retro    "
    # set_dugme() # ******* treba napraviti da se može postaviti dugme po broju: set_dugme(x)
    nova_igra()

# *************** crta ram sa svetlim i tamnim ivicama da bi izgledao 3D
def ram(x, y, s, v, utis, p, boja):  # pozicija gornjeg levog ugla, širina, visina, dali je utisnut ili ne,
    global retro_stil
    if retro_stil:  # koji retro stil?
        if p:  # dali farba pozadinu i kojom bojom  **************
            pg.draw.rect(prozor, pg.Color(boja), (x, y, s, v))
        if not utis:
            (boja1, boja2) = (SVETLA_IVICA, TAMNA_IVICA)  # kako su ove nazovi konstante
        else:  # a to su zapravo obične varijable
            (boja2, boja1) = (SVETLA_IVICA, TAMNA_IVICA)  # vidljive i bez deklaracije global ???
        pg.draw.line(prozor, pg.Color(boja1), (x - 2, y - 2), (x + 1 + s, y - 2), 2)  # gornja horizontalna
        pg.draw.line(prozor, pg.Color(boja1), (x - 2, y - 2), (x - 2, y + 1 + v), 2)  # leva vertikalna
        pg.draw.line(prozor, pg.Color(boja2), (x + 2 + s, y + 2 + v), (x + 2, y + v + 2), 2)  # donja horizontalna
        pg.draw.line(prozor, pg.Color(boja2), (x + 2 + s, y + 2), (x + 2 + s, y + 2 + v), 2)  # desna vertikalna
        pg.display.update()
    else:
        if p:  # dali farba pozadinu i kojom bojom  **************
            pg.draw.rect(prozor, pg.Color(boja), (x, y, s, v), 0, 12)
        if not utis:
            (boja1, boja2) = (SVETLA_IVICA, TAMNA_IVICA)
        else:
            (boja2, boja1) = (SVETLA_IVICA, TAMNA_IVICA)
        pg.draw.rect(prozor, pg.Color(boja2), (x + 1, y + 1, s, v), 1, 12)
        pg.draw.rect(prozor, pg.Color(boja2), (x + 2, y + 2, s, v), 1, 12)
        pg.draw.rect(prozor, pg.Color(boja1), (x - 1, y - 1, s, v), 1, 12)
        pg.draw.rect(prozor, pg.Color(boja1), (x - 2, y - 2, s, v), 1, 12)
        pg.draw.rect(prozor, pg.Color(boja), (x, y, s, v), 4, 12)
        pg.display.update()

# ********** ove dve funkcije su iz "Petlja...rs" malo prepravljene **********************
def tekst_centar(x, y, tekst, velicina):
    font = pg.font.SysFont("Courier", velicina)
    tekst = font.render(tekst, True, pg.Color("black"))
    (sirina_teksta, visina_teksta) = (tekst.get_width(), tekst.get_height())
    (x, y) = (x - sirina_teksta / 2, y - visina_teksta / 2)
    prozor.blit(tekst, (x, y + 1))
    pg.display.update()

def tekst_levo(x, y, tekst, velicina):
    global BOJA_PODLOGE
    font = pg.font.SysFont("Courier", velicina)  # font kojim će biti prikazan broj poena
    tekst = font.render(tekst, True, pg.Color("black"))
    (sirina_teksta, visina_teksta) = (tekst.get_width(), tekst.get_height())
    pg.draw.rect(prozor, pg.Color(BOJA_PODLOGE), (x - 1, y - 1, sirina_teksta + 9, visina_teksta))
    prozor.blit(tekst, (x, y))
    pg.display.update()

# *************** snima sadržaj prozora igre u sudoku.png ************************************************
def saveslika():  # ***** sada se koristi za eksperimente sa bojama i "KONSTANTAMA"
    global BOJA_PODLOGE # ***** treba napraviti color whell da svako može podešavato boje po želji ******
    # ime_slike = "sudoku.png"
    # pg.image.save(prozor, ime_slike)
    BOJA_PODLOGE = [180, 180, 180]


# ********* uokviren tekst osnova za dugme, poziva ram() **************************************************
def tekst_box(x, y, tekst, velicina, utis):
    global BOJA_PODLOGE
    # pg.draw.rect(prozor, pg.Color([186, 222, 186]), (x - 1, y - 1, len(tekst) * 8 + 1, velicina + 1))
    font = pg.font.SysFont("Courier", velicina)  # font kojim će biti prikazan broj poena
    tekst = font.render(tekst, True, pg.Color("black"))
    (sirina_teksta, visina_teksta) = (tekst.get_width(), tekst.get_height())
    (s, v) = (sirina_teksta, visina_teksta)
    ram(x, y, s, v, False, True, BOJA_PODLOGE)
    prozor.blit(tekst, (x, y))
    pg.display.update()

#  ****************************  Postavlja dugmad na ekran **********************************
def set_dugme():
    global dugmad, BOJA_PODLOGE
    for i in range(1, len(dugmad)):
        brd = dugmad[i][0]
        x = dugmad[i][1]
        y = dugmad[i][2]
        velicina = dugmad[i][4]
        utis = dugmad[i][5]
        font = pg.font.SysFont("Courier", velicina)  # font kojim će biti prikazan broj poena
        natpis = font.render(dugmad[i][3], True, pg.Color("black"))
        (sirina_teksta, visina_teksta) = (natpis.get_width(), natpis.get_height())
        (s, v) = (sirina_teksta, visina_teksta)
        (dugmad[i][6], dugmad[i][7]) = (sirina_teksta, visina_teksta)
        ram(x, y, s, v, utis, True, BOJA_PODLOGE)
        prozor.blit(natpis, (x, y))
        pg.display.update()

#  ***** proverava koje dugmeje pritisnuto i vraća njegov broj, utisne ga, izvrši funkciju i otpusti**********************
def test_dugme(mx, my, mk):
    global dugmad, BOJA_PODLOGE
    for i in range(1, len(dugmad)):
        brd = dugmad[i][0]
        x = dugmad[i][1]
        y = dugmad[i][2]
        velicina = dugmad[i][4]
        utis = mk
        s = dugmad[i][6]
        v = dugmad[i][7]
        if mx > x and mx < x + s and my > y and my < y + v:
            ram(x, y, s, v, utis, False, BOJA_PODLOGE)
            eval(dugmad[i][8])
            pg.time.wait(300)
            ram(x, y, s, v, not utis, False, BOJA_PODLOGE)
            return brd
    return 0

# *************** ovde je spakovano redom sve što treba za igru **********************************
def nova_igra():
    global sudo, sud_x, sudos, t_kol, t_red, dugmad, tezina
    # ********* niz (array) nizova koji sadrži brojčanu matricu sudokua ***************
    sudo = [[0 for i in range(9)] for j in range(9)]
    sud_x = [[0 for i in range(9)] for j in range(9)]
    # ********* niz (array) nizova koji sadrži tekstualnu (string) matricu sudokua ***************
    sudos = [[" " for i in range(9)] for j in range(9)]
    a = b = 0
    #  ***********************************************************************************************************
    osnovna()  # *********************** ovde se generiše rešeni sudoku *** samo jedan uvek isti *********
    transpon()  # *************ovde mu se zamene redovi i kolone ******************************************
    prevrni()  # *********************** ovde prvi red postaje poslednji, drugi - predposlednji...
    for i in range(4):
        a = rnd.randint(i + 1, 9)
        if i != a:
            zamena(i,
                   a)  # ****************ovde mu se 4 puta zamene dva broja da bi izgledao komplikovaniji ***************

    izbaci(tezina)  # ****************** ovde mu se izbace neki brojevi da bi se imalo šta rešavati ***********

    prikaz()  # *********************** ovde se sudoku prikazuje u obliku teksta ************************
    polje(70, 70)  # ****************** ovde se crta polje za sudoku uz pomoć grafike ************************
    ubaci(70, 70)  # ****************ovde se ubaccuju brojevi u polje za igru ********************************
    set_dugme()  # ***************** postavlja dugmad na ekran *********************************************
    tajmer(False)  # *** reset tajmera *******
    set_broj(0)  # *** u startu je u modu brisanje


nova_igra()
# ************** ovo dole je glavna petlja programa * karakteristična za pygame modul *******************************
pygamebg.frame_loop(20, novi_frejm, obradi_dogadjaj)

# pg.time.wait(30)
# pygamebg.wait_loop()
# pg.quit()
# *********************************************************************** kraj *******************************
# ** ovo dole su razne probe i napušteni delovi koda *************************************************************************************
"""
# *********************************
def volvox(a,b,c):
    global x0, y0
    x=y=1
    while (True):
        red = rnd.randint(1, 255)
        grn = rnd.randint(1, 255)
        blu = rnd.randint(1, 255)
        for i in range(1, 900):
            xx = y - math.copysign(1, x) * math.sqrt(abs(b * x + c))
            yy = a - x
            x = xx
            y = yy
            pg.gfxdraw.pixel(prozor, int(x + x0), int(y + y0),[red,grn,blu] )

    # **************************************************************************


       # print(a)
            if a == 1:
            pass
            # nova_igra()   # **** počinje nova igra ******
        elif a == 2 and tezina > 1:
            pass
            # tezina = tezina - 1
            # tekst_box(705, 160, " " + str(tezina) + " ", 20, False)
            # nova_igra()
            #izbaci(tezina)
        elif a == 3 and tezina < 9:
            pass
            # tezina = tezina + 1
            # tekst_box(705, 160, " " + str(tezina) + " ", 20, False)
            # nova_igra()
            # izbaci(tezina)
        elif a == 4:
            pass
            # pg.quit()
        elif a >= 5 and a <= 13:
            k = a - 4
            tekst_box(700, 345, " " + str(k) + " ", 24, False)
            proveri(k, 100, 100)  # ****** ovde obeleži sve pojave broja k u sudokuu ************
        elif a == 14:
            pass
            # brisanje()
        elif a == 15:
            pass
            # resi(100,100)
        elif a == 16:
            pass
            # iz_pocetka(100,100)

"""
"""
# print(" │x".join(sudos[i][:3:])," │/", " │ ".join(sudos[i][3:6:])," │ ", "*│+".join(sudos[i][6:9:]), "-│+")
thin = "─│┌┐└┘├┤┬┴┼"
thin_thick = "─│┌┐└┘├┤┬┴┼┝━┿┥"
thin_double = "─│┌┐└┘├┤┬┴┼╞═╪╡"
rounded = "─│╭╮╰╯├┤┬┴┼"
rounded_thick = "─│╭╮╰╯├┤┬┴┼┝━┥"
rounded_double = "─│╭╮╰╯├┤┬┴┼╞═╪╡"
thick = "━┃┏┓┗┛┣┫┳┻╋"
thick_thin = "─│┌┐└┘├┤┬┴┼┠─╂┨"
double = "═║╔╗╚╝╠╣╦╩╬"
double_thin = "═║╔╗╚╝╠╣╦╩╬╟─╫╢"
booktabs = "─       ─── ━━ "

ascii_thin = "-|+++++++++"
ascii_thin_double = "-|++++++++++=++"
ascii_double = "=H+++++++++"
ascii_double_thin = "=H++++++++++-++"
ascii_booktabs = "-       --- == "

markdown = " |         |-||"
"""

# *********************************************************************************************
