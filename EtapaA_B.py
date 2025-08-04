# Autor: gjimenez
# Ejemplo de calculo #1 – Etapa A–B
# Simulación del trayecto de un proyectil deslizandose por una rampa
# usando dos metodos: conservacion de la energia y analisis con fuerzas (MRUA)

import math
import numpy as np
import matplotlib.pyplot as plt

# --- Datos del usuaro ---
print("Ingrese los datos del sistema:")
h = float(input("Altura desde la que se suelta el proyectil (m): "))
L = float(input("Longitud de la rampa (m): "))
g = 9.81  # gravedad (m/s²)

# --- Metodo 1: Conservacion de la energia ---
# v = sqrt(2gh)
v_energy = math.sqrt(2 * g * h)

print("\n Método 1: Conservación de la energía")
print(f"Velocidad al final de la rampa (v_B): {v_energy:.2f} m/s")

# --- Metodo 2: Analisis con fuerzas ---
# Angulo de inclinacion
sin_theta = h / L
theta_rad = math.asin(sin_theta)
theta_deg = math.degrees(theta_rad)

# Aceleracion sobre la rampa
a_mrua = g * sin_theta

# Velocidad al final con MRUA
v_mrua = math.sqrt(2 * a_mrua * L)

print("\n Método 2: Análisis con fuerzas y MRUA")
print(f"Ángulo de inclinación de la rampa: {theta_deg:.2f}°")
print(f"Aceleración a lo largo de la rampa: {a_mrua:.3f} m/s²")
print(f"Velocidad al final de la rampa (v_B): {v_mrua:.2f} m/s")

# --- Comparacion ---
print("\n Comparación de métodos:")
if abs(v_energy - v_mrua) < 1e-6:
    print("Ambos métodos coinciden en el resultado final.")
else:
    print("Existe una diferencia entre los métodos.")

# --- Calculo del tiempo total para recorrer la rampa ---
# x = 1/2 * a * t² → t = sqrt(2x / a)
t_total = math.sqrt(2 * L / a_mrua)

# --- Generar datos para graficar ---
t_values = np.linspace(0, t_total, 100)
v_values = a_mrua * t_values             # v(t) = a * t
x_values = 0.5 * a_mrua * t_values**2    # x(t) = 1/2 * a * t²

# --- Grafica: Velocidad vs Tiempo ---
plt.figure(figsize=(10, 4))
plt.plot(t_values, v_values, label='Velocidad (m/s)', linewidth=2)
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')
plt.title('Velocidad vs Tiempo sobre la rampa')
plt.grid(True)
plt.legend()
plt.show()

# --- Grafica: Posicion vs Tiempo ---
plt.figure(figsize=(10, 4))
plt.plot(t_values, x_values, label='Posición (m)', color='orange', linewidth=2)
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición sobre la rampa (m)')
plt.title('Posición vs Tiempo sobre la rampa')
plt.grid(True)
plt.legend()
plt.show()
