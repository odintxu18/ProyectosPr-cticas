from juego import Juego

class Main:
    def __init__(self):
        self.juego = Juego()

    def ejecutar(self):
        self.juego.jugar()

if __name__ == "__main__":
    main = Main()
    main.ejecutar()