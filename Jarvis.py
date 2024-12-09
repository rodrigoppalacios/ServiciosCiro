import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyttsx3
import random
import speech_recognition as sr
import threading

# Configuración de la voz de Jarvis
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Configura la voz masculina (puedes ajustar la voz si es necesario)

# Función para hablar como Jarvis
def hablar_como_jarvis(texto):
    engine.say(texto)
    engine.runAndWait()

# Clase para la simulación 3D de neuronas
class SimulacionNeuronas3D:
    def __init__(self, num_neuronas=1000, radio_limite=200):
        self.num_neuronas = num_neuronas
        self.radio_limite = radio_limite
        self.neuronas = np.random.rand(num_neuronas, 3) * 2 * radio_limite - radio_limite
        self.velocidad = np.random.rand(num_neuronas, 3) - 0.5  # Movimiento aleatorio en x, y, z
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-radio_limite, radio_limite)
        self.ax.set_ylim(-radio_limite, radio_limite)
        self.ax.set_zlim(-radio_limite, radio_limite)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Simulación de Neuronas 3D')
        self.rotando = False  # Variable para saber si la simulación debe rotar
        self.terminar = False  # Control para detener la simulación

    def actualizar(self):
        # Actualiza la posición de las neuronas
        self.neuronas += self.velocidad

        # Mantén las neuronas dentro de la esfera, rebotan al chocar con el borde
        distancias = np.linalg.norm(self.neuronas, axis=1)
        fuera_limite = distancias > self.radio_limite

        # Invertir la dirección de las neuronas fuera de la esfera
        self.velocidad[fuera_limite] = -self.velocidad[fuera_limite]

        # Limpiar la gráfica y dibujar de nuevo
        self.ax.cla()
        self.ax.set_xlim(-self.radio_limite, self.radio_limite)
        self.ax.set_ylim(-self.radio_limite, self.radio_limite)
        self.ax.set_zlim(-self.radio_limite, self.radio_limite)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Simulación de Neuronas 3D')

        # Graficar las neuronas
        self.ax.scatter(self.neuronas[:, 0], self.neuronas[:, 1], self.neuronas[:, 2], color='red', s=10)

    def obtener_figura(self):
        return self.fig

    def rotar(self):
        # Método para hacer que la visualización gire lentamente
        while self.rotando:
            for angle in range(0, 360, 1):
                self.ax.view_init(elev=20., azim=angle)
                plt.draw()
                plt.pause(0.01)

    def iniciar_simulacion(self):
        hablar_como_jarvis("Iniciando la simulación de neuronas en 3D.")
        self.terminar = False
        while not self.terminar:
            self.actualizar()
            plt.draw()
            plt.pause(0.01)

    def detener_simulacion(self):
        self.terminar = True
        hablar_como_jarvis("Simulación detenida.")

# Función para reconocer comandos de voz
def reconocer_comando():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Escuchando comando...")
            audio = recognizer.listen(source)

        try:
            comando = recognizer.recognize_google(audio).lower()
            print(f"Comando recibido: {comando}")
            procesar_comando(comando)
        except sr.UnknownValueError:
            print("No entendí el comando, por favor repite.")
        except sr.RequestError as e:
            print(f"Error de solicitud: {e}")

# Función para procesar comandos de voz
def procesar_comando(comando):
    if "iniciar" in comando:
        iniciar_simulacion_thread()
    elif "detener" in comando:
        detener_simulacion()
    elif "rotar" in comando:
        rotar_simulacion()
    elif "salir" in comando:
        hablar_como_jarvis("Cerrando el programa. Hasta pronto.")
        exit()

# Funciones para controlar la simulación desde los comandos de voz
def iniciar_simulacion_thread():
    global simulacion
    hablar_como_jarvis("Iniciando la simulación.")
    simulacion_thread = threading.Thread(target=simulacion.iniciar_simulacion)
    simulacion_thread.start()

def detener_simulacion():
    global simulacion
    simulacion.detener_simulacion()

def rotar_simulacion():
    global simulacion
    simulacion.rotando = not simulacion.rotando
    if simulacion.rotando:
        hablar_como_jarvis("Rotando la simulación.")
        rotar_thread = threading.Thread(target=simulacion.rotar)
        rotar_thread.start()
    else:
        hablar_como_jarvis("Deteniendo rotación.")

# Crear la simulación y la ventana 3D
if __name__ == "__main__":
    simulacion = SimulacionNeuronas3D()
    hablar_como_jarvis("Bienvenido a la simulación 3D de neuronas.")
    
    # Ejecutar el reconocimiento de comandos en un hilo independiente
    reconocimiento_thread = threading.Thread(target=reconocer_comando)
    reconocimiento_thread.start()
    
    plt.show()
