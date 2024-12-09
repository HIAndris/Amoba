from Modules import amobasito
import os

def Kozepre(sr:str, sorsz:int, oszlopsz:int):
    sorok = sr.split("\n")
    kozepsor = ""
    for _ in range((sorsz - len(sorok)) // 2):
        kozepsor += "\n"
    for sor in sorok:
        kozepsor += sor.center(oszlopsz) + "\n"
    for _ in range((sorsz - len(sorok)) - ((sorsz - len(sorok)) // 2)):
        kozepsor += "\n"
    
    return kozepsor

terminal_size = os.get_terminal_size()

amoba = amobasito.Amoba(10, 10, 5)
print(Kozepre(str(amoba), terminal_size.lines, terminal_size.columns))
while amoba.Statusz()[0] == 0:
    try:
        terminal_size = os.get_terminal_size()
        x, y = input(f"Adja meg játékos {amoba.Jatekos()} lépését!(x, y): ").split()
        x = int(x)
        y = int(y)
        amoba.Lepes(x, y)
        print(Kozepre(str(amoba), terminal_size.lines, terminal_size.columns))
    except ValueError as ve:
        print(f"Rossz értéket adott meg! ({ve})")
    except amobasito.CircumcisionError:
        print("Ez a hely foglalt!")
    except amobasito.GameOverError:
        print("A játék véget ért!")
print("A játék véget ért!")
print(amoba.Statusz()[1])