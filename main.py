# Función para imprimir el tablero
def imprimir_tablero(tablero):
    for i in range(3):
        print(" | ".join(tablero[i]))
        if i < 4:
            print("---------")


# Función para comprobar si hay un ganador
def comprobar_ganador(tablero, jugador):
    # Comprobar filas, columnas y diagonales
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] == jugador:  # Filas
            return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] == jugador:  # Columnas
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador:  # Diagonal principal
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:  # Diagonal secundaria
        return True
    return False


# Función para comprobar si el tablero está lleno
def tablero_lleno(tablero):
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == " ":
                return False
    return True


# Función principal que controla el flujo del juego
def jugar():
    # Inicializar el tablero vacío
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    jugador_actual = "X"  # El primer jugador es X
    while True:
        imprimir_tablero(tablero)

        # Pedir al jugador su movimiento
        print(f"Turno de {jugador_actual}. Ingrese fila y columna (0-2), separados por un espacio: ", end="")
        fila, columna = map(int, input().split())

        # Comprobar si la casilla está vacía
        if tablero[fila][columna] == " ":
            tablero[fila][columna] = jugador_actual
        else:
            print("¡Casilla ocupada! Intenta de nuevo.")
            continue

        # Comprobar si hay un ganador
        if comprobar_ganador(tablero, jugador_actual):
            imprimir_tablero(tablero)
            print(f"¡{jugador_actual} ha ganado!")
            break

        # Comprobar si el tablero está lleno (empate)
        if tablero_lleno(tablero):
            imprimir_tablero(tablero)
            print("¡Es un empate!")
            break

        # Cambiar de jugador
        jugador_actual = "O" if jugador_actual == "X" else "X"


# Ejecutar el juego
if __name__ == "__main__":
    jugar()
