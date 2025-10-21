from tablero import Tablero

class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.jugador_actual = "X"

    def cambiar_jugador(self):
        self.jugador_actual = "O" if self.jugador_actual == "X" else "X"

    def jugar(self):
        while True:
            self.tablero.imprimir()

            try:
                fila, col = map(int, input(f"Turno de {self.jugador_actual}. Ingresa fila y columna (0-2), separados por espacio: ").split())
            except ValueError:
                print("Entrada inválida, ingresa dos números separados por espacio.")
                continue

            if not (0 <= fila <= 2 and 0 <= col <= 2):
                print("Índices fuera del rango permitido (0-2). Intenta de nuevo.")
                continue

            if not self.tablero.colocar(fila, col, self.jugador_actual):
                print("Casilla ocupada, intenta otra.")
                continue

            if self.tablero.comprobar_ganador(self.jugador_actual):
                self.tablero.imprimir()
                print(f"¡Felicidades! El jugador {self.jugador_actual} ha ganado.")
                break

            if self.tablero.esta_lleno():
                self.tablero.imprimir()
                print("¡Empate!")
                break

            self.cambiar_jugador()