class Tablero:
    def __init__(self):
        self.juego = None
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]

    def imprimir(self):
        for i in range(3):
            print(" | ".join(self.tablero[i]))
            if i < 2:
                print("---------")

    def colocar(self, fila, col, jugador):
        if self.tablero[fila][col] == " ":
            self.tablero[fila][col] = jugador
            return True
        return False

    def comprobar_ganador(self, jugador):
        b = self.tablero
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == jugador:
                return True
            if b[0][i] == b[1][i] == b[2][i] == jugador:
                return True
        if b[0][0] == b[1][1] == b[2][2] == jugador:
            return True
        if b[0][2] == b[1][1] == b[2][0] == jugador:
            return True
        return False

    def esta_lleno(self):
        for fila in self.tablero:
            if " " in fila:
                return False
        self.juego.reiniciar()
        return True
