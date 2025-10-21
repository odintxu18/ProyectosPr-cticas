from juego import Juego

def pedir_jugada(jugador):
    while True:
        try:
            entrada = input(f"Turno de {jugador}. Ingresa fila y columna (0-2): ")
            fila, col = map(int, entrada.strip().split())
            return fila, col
        except ValueError:
            print("Entrada inválida. Escribe dos números separados por un espacio.")

def main():
    juego = Juego()

    print("¡Bienvenido a Tres en Raya!\n")
    while not juego.ha_terminado():
        juego.mostrar_tablero()
        fila, col = pedir_jugada(juego.obtener_jugador_actual())
        juego.realizar_turno(fila, col)

    juego.mostrar_tablero()
    if juego.hay_ganador():
        print(f"\n ¡El jugador {juego.obtener_ganador()} ha ganado!")
    else:
        print("\n ¡Empate!")

if __name__ == "__main__":
    main()
