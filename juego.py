from tablero import Tablero

class Juego:
#se establecen los selfs para poder dar el juego
    def __init__(self):
        self.tablero = Tablero()
        self.jugador_actual = "X"
        self.ganador = None
        self.terminado = False
#Saltan las excepciones del juego o si la persona ha ganado
    def realizar_turno(self, fila, col):
        if not (0 <= fila <= 2 and 0 <= col <= 2):
            print("Posición fuera de rango. Intenta con valores entre 0 y 2.")
            return False

        if not self.tablero.colocar(fila, col, self.jugador_actual):
            print("Casilla ocupada. Elige otra.")
            return False

        if self.tablero.comprobar_ganador(self.jugador_actual):
            self.ganador = self.jugador_actual
            self.terminado = True
            return True

        if self.tablero.esta_lleno():
            self.terminado = True
            return True

        self.cambiar_jugador()
        return True

    def mostrar_tablero(self):
        self.tablero.imprimir()

    def ha_terminado(self):
        return self.terminado

    def hay_ganador(self):
        return self.ganador is not None

    def obtener_ganador(self):
        return self.ganador

    def cambiar_jugador(self):
        self.jugador_actual = "O" if self.jugador_actual == "X" else "X"

    def obtener_jugador_actual(self):
        return self.jugador_actual
