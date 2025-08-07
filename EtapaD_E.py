# Ejemplo de calculo #4 – Etapa D–E
# Simulacion de la trayectoria final del proyectil despues del rebote hasta tocar el suelo.

import json
import math
import numpy as np
import matplotlib.pyplot as plt

# Gravedad
g = 9.81

try:
    # Cargar datos de A–B, B–C y C-D
    with open("salida_AB.json", "r") as f:
        datos_AB = json.load(f)

    with open("salida_BC.json", "r") as f:
        datos_BC = json.load(f)

    with open("salida_CD.json", "r") as f:
        datos_CD = json.load(f)

except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar el archivo {e.filename}.")
    print("Asegúrese de que los archivos 'salida_AB.json', 'salida_BC.json' y 'salida_CD.json' existen.")
    print("Por favor, ejecute las etapas anteriores primero.")
    exit()

# Verificar si hubo impacto para proceder
if not datos_BC.get("impacto", False):
    print("No hay impacto. Etapa D–E no se ejecuta.")
    exit()

# Parámetros de partida para la etapa D-E (desde el punto de colisión)
x0_DE = datos_BC["x_C"]
y0_DE = datos_BC["y_C"]

# Velocidades iniciales para la etapa D-E (las velocidades post-rebote)
v_x_post = datos_CD["v_x_post"]
v_y_post = datos_CD["v_y_post"]

print("--- Etapa D–E: Vuelo Final Post-Rebote ---")
print(f"Punto inicial (post-rebote): (x_D={x0_DE:.2f} m, y_D={y0_DE:.2f} m)")
print(f"Velocidad inicial (post-rebote): (v'_x={v_x_post:.2f} m/s, v'_y={v_y_post:.2f} m/s)")

# Calcular el tiempo de caída hasta el suelo (y=0)
# Se resuelve la ecuación cuadrática: 0 = y0_DE + v_y_post*t - 0.5*g*t^2
a = -0.5 * g
b = v_y_post
c = y0_DE
discriminante = b**2 - 4 * a * c

if discriminante < 0:
    print("Error: No se puede calcular el tiempo de caída (discriminante negativo).")
    exit()

# Se elije la solución de tiempo positiva
t_caida = (-b - math.sqrt(discriminante)) / (2 * a)

# Calcular la distancia horizontal recorrida en esta etapa
x_recorrido_DE = v_x_post * t_caida
x_final = x0_DE + x_recorrido_DE

# --- Guardar Resultados de D-E en JSON ---
resultados_DE = {
    "t_caida": t_caida,
    "x_recorrido_DE": x_recorrido_DE,
    "x_final_total": x_final,
    "v_x_post": v_x_post,
    "v_y_post": v_y_post
}
with open("salida_DE.json", "w") as f:
    json.dump(resultados_DE, f, indent=4)

print("\nResultados de la etapa D-E guardados en 'salida_DE.json'.")


# --- Generación de la Gráfica Completa (B -> C -> D -> E) ---

# 1. Generar puntos para la trayectoria B-C (vuelo inicial)
v_B = datos_AB["v_B"]
theta_rad = datos_AB["theta_rad"]
v0x_BC = v_B * math.cos(theta_rad)
v0y_BC = v_B * math.sin(theta_rad)
t_BC = datos_BC["t_C"]
t_vals_BC = np.linspace(0, t_BC, 100)
x_BC = v0x_BC * t_vals_BC
y_BC = v0y_BC * t_vals_BC - 0.5 * g * t_vals_BC**2

# 2. Generar puntos para la trayectoria D-E (vuelo post-rebote)
t_vals_DE = np.linspace(0, t_caida, 100)
x_DE = x0_DE + v_x_post * t_vals_DE
y_DE = y0_DE + v_y_post * t_vals_DE - 0.5 * g * t_vals_DE**2

# 3. Definir la pared del obstáculo
pared_x = np.linspace(x0_DE - 1, x0_DE + 1, 2)
pared_y = y0_DE - (x0_DE - pared_x) # Pared a 45 grados que pasa por (x0_DE, y0_DE)

# 4. Graficar todos los elementos
plt.figure(figsize=(12, 7))
# Trayectorias
plt.plot(x_BC, y_BC, label="Etapa B-C (Vuelo inicial)", color="blue")
plt.plot(x_DE, y_DE, label="Etapa D-E (Vuelo post-rebote)", color="green")
# Elementos estáticos
plt.plot(pared_x, pared_y, 'r--', label="Obstáculo (pared a 45°)")
plt.axhline(y=0, color='brown', linestyle='-', linewidth=2, label="Suelo")
# Puntos clave
plt.plot(x0_DE, y0_DE, 'ko', markersize=8, label=f"Punto de Colisión C ({x0_DE:.2f}, {y0_DE:.2f})")
plt.plot(x_final, 0, 'kx', markersize=10, mew=2, label=f"Impacto Final E ({x_final:.2f}, 0)")

plt.title("Trayectoria Completa del Proyectil (B-C + D-E)")
plt.xlabel("Posición Horizontal x (m)")
plt.ylabel("Posición Vertical y (m)")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.ylim(bottom=-0.5) # Ajustar límite para mejor visibilidad del impacto
plt.tight_layout()
plt.show()