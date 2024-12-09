# Az Amoba osztály egy tetszőleges méretű amőba pályát hoz létre tetszőleges hosszúságú győzelmi egyenessel és tetszőleges jelekkel a játékosok számára.
# A négyzetrácsos pálya egyik üres négyzetének koordinátáival léphet a játékos addig, amíg az egyik játékosnak össze nem gyűlt elég egymás melletti jelölése a győzelemhez vagy el nem fogytak az üres négyzetek.
class Amoba:
    def __init__(self, x:int=3, y:int=3, win:int=3, p1:str="X", p2:str="O"):
        if isinstance(x, int) and 0 < x and isinstance(y, int) and 0 < y and isinstance(win, int) and (0 < win <= x or 0 < win <= y) and isinstance(p1, str) and len(p1) == 1 and isinstance(p2, str) and len(p2) == 1 and p1 != p2: # bemeneti paraméterek ellenőrzése
            self.x = x # pálya szélesség
            self.y = y # pálya magasság
            self.p1 = p1 # 1. játékos jelölőkaraktere
            self.p2 = p2 # 2. játékos jelölőkaraktere
            self.win = win # győzelemhez szükséges egymás melletti jelölőkarakterek száma
            self.p = 1 # jelenleg soron lévő játékos a lépéshez
            self.status = (0, "A játék folyamatban van.") # jelenlegi játék státusz (0: folyamatban lévő játék, 1: az első játékos nyert, 2: a második játékos nyert, 3: döntetlen)
            self.moves = 0 # eddigi összes lépés
            self.maxMoves = x*y # maximális lépések száma
            
            self.mapTop = self.PalyaPlafon() # pálya teteje
            self.mapBetween = self.PalyaSorkoz() # pálya sorköze
            self.mapBottom = self.PalyaPadlo() # pálya alja
            
            self.map = [] # amőba játéktábla generálása magasság és szélesség alapján
            for y in range(self.y):
                self.map.append([])
                for x in range(self.x):
                    self.map[-1].append(" ")
        else:
            raise ValueError(f"Helytelen értékeket kapott az Amoba osztály inicializáláskor! (x: {x}, y: {y}, win: {win}, p1: {p1}, p2: {p2})")
    
    def __str__(self): # Vizuális pályamegjelenítés generálása 4 pályakomponens kombinálásával
        visualMap = self.mapTop
        for y in range(self.y):
            visualMap += "\n" + self.PalyaSor(y) + "\n" + self.mapBetween
        visualMap = visualMap[0:(((4*self.x)+1)*-1)] + self.mapBottom
        
        return visualMap

    def PalyaPlafon(self): # A pálya tetejének generálása szélesség alapján
        plafon = "┌"
        for _ in range(self.x):
            plafon += "───┬"
        plafon = plafon[0:-1] + "┐"
        return plafon
    
    def PalyaSor(self, y:int): # A pálya egyik sorának generálása a sorszám megadásával bemenetként a pálya mentett adatai alapján
        if isinstance(y, int) and 0 <= y < len(self.map):
            sor = "│"
            for x in self.map[y]:
                sor += " " + x + " │"

            return sor
        else:
            raise ValueError(f"Helytelen értékeket kapott az Amoba osztály PalyaSor függvénye! (x: {x}, y: {y})")
    
    def PalyaSorkoz(self): # A pálya sorai közötti elválasztó sor generálása szélesség alapján
        sor = "├"
        for _ in range(self.x):
            sor += "───┼"
        sor = sor[0:-1] + "┤"
        
        return sor

    def PalyaPadlo(self): # A pálya aljának generálása szélesség alapján
        padlo = "└"
        for _ in range(self.x):
            padlo += "───┴"
        padlo = padlo[0:-1] + "┘"
        return padlo
        
    def Lepes(self, x:int, y:int): # Lépés tétele a soron következő játékossal a megadott koordinátájú mezőre
        if isinstance(x, int) and isinstance(y, int):
            if self.map[y][x] == " ":
                if self.status[0] == 0:
                    if self.p == 1:
                        self.map[y][x] = self.p1
                        self.p = 2

                    else:
                        self.map[y][x] = self.p2
                        self.p = 1
                    
                    self.moves += 1
                    self.StatuszCsekk(x, y)
                else:
                    raise GameOverError(f"A játék vége után már nem lehet lépni! ({self.status[1]})")
            else:
                raise CircumcisionError(f"Ez a pozíció már foglalt! (x: {x}, y: {y})")
        else:
            raise ValueError(f"Helytelen értékeket kapott az Amoba osztály Lepes eljárása! (x: {x}, y: {y})")
    
    def StatuszCsekk(self, x, y): # A játék státuszának ellenőrzése és frissítése a megadott koordináta alapján a vízszintes, függőleges és átós irányokat vizsgálva
        if isinstance(x, int) and isinstance(y, int) and self.map[y][x]:
            symbol = self.map[y][x]
            if self.Fuggoleges(x, y, symbol) or self.Vizszintes(x, y, symbol) or self.Atlos(x, y, symbol):
                if self.p == 1:
                    self.status = (2, f"A játékot a második játékos nyerte meg. ({self.p2})")
                else:
                    self.status = (1, f"A játékot az első játékos nyerte meg. ({self.p1})")
            elif self.maxMoves <= self.moves:
                self.status = (3, "A játék döntetlennel zárult.")
        else:
            raise ValueError(f"Helytelen értékeket kapott az 'Amoba' osztály 'StatuszFrissit' eljárása! (x: {x}, y: {y})")

    def Fuggoleges(self, x: int, y: int, symbol: str): # Függőleges vizsgálat a megadott koordinátákon
        if isinstance(x, int) and isinstance(y, int) and isinstance(symbol, str):
            vertical = 0
            yPos = y+(self.win*-1)+1
            end = y+self.win-1
            while vertical < self.win and yPos <= end:
                if 0 <= yPos < self.y:
                    if self.map[yPos][x] == symbol:
                        vertical += 1
                    else:
                        vertical = 0
                yPos += 1
            
            if self.win <= vertical:
                return True
            else:
                return False    
        else:
            raise ValueError(f"Helytelen értékeket kapott az 'Amoba' osztály 'StatuszFrissit' eljárása! (x: {x}, y: {y}, symbol: {symbol})")
    
    def Vizszintes(self, x: int, y: int, symbol: str): # Vízszintes vizsgálat a megadott koordinátákon
        if isinstance(x, int) and isinstance(y, int) and isinstance(symbol, str):
            horizontal = 0
            xPos = x+(self.win*-1)+1
            end = x+self.win-1
            while horizontal < self.win and xPos <= end:
                if 0 <= xPos < self.x:
                    if self.map[y][xPos] == symbol:
                        horizontal += 1
                    else:
                        horizontal = 0
                xPos += 1
            
            if self.win <= horizontal:
                return True
            else:
                return False    
        else:
            raise ValueError(f"Helytelen értékeket kapott az 'Amoba' osztály 'StatuszFrissit' eljárása! (x: {x}, y: {y}, symbol: {symbol})")
    
    def Atlos(self, x: int, y: int, symbol: str): # Átlós vizsgálat a megadott koordinátákon
        if isinstance(x, int) and isinstance(y, int) and isinstance(symbol, str):
            diagonal = 0
            xPos = x+(self.win*-1)+1
            yPos = y+(self.win*-1)+1
            end = x+self.win-1
            while diagonal < self.win and xPos <= end:
                if 0 <= xPos < self.x and 0 <= yPos < self.y:
                    if self.map[yPos][xPos] == symbol:
                        diagonal += 1
                    else:
                        diagonal = 0
                xPos += 1
                yPos += 1
            
            if self.win <= diagonal:
                return True
            else:
                diagonal = 0
                xPos = x+self.win-1
                yPos = y+(self.win*-1)+1
                end = y+self.win-1
                while diagonal < self.win and yPos <= end:
                    if 0 <= xPos < self.x and 0 <= yPos < self.y:
                        if self.map[yPos][xPos] == symbol:
                            diagonal += 1
                        else:
                            diagonal = 0
                    xPos += -1
                    yPos += 1
                
                if self.win <= diagonal:
                    return True
                else:
                    return False
        else:
            raise ValueError(f"Helytelen értékeket kapott az 'Amoba' osztály 'StatuszFrissit' eljárása! (x: {x}, y: {y}, symbol: {symbol})")
    
    def Statusz(self): # Játék státuszának visszaadása
        return self.status

    def Jatekos(self): # A jelenlegi játékos visszaadása
        if self.p == 1:
            return f"1 ({self.p1})"
        else:
            return f"2 ({self.p2})"


# A játék vége utáni helytelen hívásokra visszaadott hiba
class GameOverError(Exception): 
    pass

# A már foglalt négyzetre helytelenül hívott lépésekkor visszaadott hiba
class CircumcisionError(Exception):
    pass