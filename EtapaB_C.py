# === Etapa B–C: Vuelo parabólico ===
# Cargar los resultados de la etapa A–B
import json
import math
import numpy as np
import matplotlib.pyplot as plt
g = 9.81  # gravedad (m/s²)

with open("salida_AB.json", "r") as f:
    datos = json.load(f)

v_B = datos["v_B"]
theta_rad = datos["theta_rad"]
theta_deg = datos["theta_deg"]

print(f"Velocidad de entrada desde A–B: {v_B:.2f} m/s")
print(f"Ángulo de salida desde la rampa: {theta_deg:.2f}°")

# Ingreso de datos adicionales para la etapa B–C
x_C = float(input("Posición horizontal del obstáculo (x_C) en m: "))
y_C = float(input("Altura del obstáculo (y_C) en m: "))

# Componentes de la velocidad inicial (usando v_mrua de etapa A-B y ángulo theta_rad)
v0x = v_B * math.cos(theta_rad)
v0y = v_B * math.sin(theta_rad)

# Calcular el tiempo que tarda en llegar a x_C
t_C = x_C / v0x

# Calcular la posición vertical en ese instante
y_proj = v0y * t_C - 0.5 * g * t_C**2

# Verificar si hay impacto
print(f"Tiempo estimado de llegada a x_C: {t_C:.3f} s")
print(f"Altura del proyectil en x_C: {y_proj:.2f} m")
print(f"Altura del obstáculo: {y_C:.2f} m")

if abs(y_proj - y_C) <= 0.01:
    print("Impacto confirmado: la altura coincide con la del obstáculo.")
    
    # Calcular la velocidad en el momento del impacto
    vx = v0x
    vy = v0y - g * t_C
    v_impacto = math.sqrt(vx**2 + vy**2)

    # Calcular el ángulo de impacto
    alpha_rad = math.atan2(vy, vx)
    alpha_deg = math.degrees(alpha_rad)

    print(f"Velocidad al impactar: {v_impacto:.2f} m/s")
    print(f"Ángulo de impacto: {alpha_deg:.2f}°")
else:
    print("No hay impacto: el proyectil no está a la altura del obstáculo.")

    # Crear arreglo de tiempos desde 0 hasta t_C
t_values = np.linspace(0, t_C, 100)

# Posiciones horizontales y verticales
x_values = v0x * t_values
y_values = v0y * t_values - 0.5 * g * t_values**2

# Gráfica de trayectoria parabólica
plt.figure(figsize=(10, 5))
plt.plot(x_values, y_values, label="Trayectoria del proyectil", color="blue")
plt.axhline(y=y_C, linestyle="--", color="red", label=f"Altura del obstáculo ({y_C} m)")
plt.axvline(x=x_C, linestyle="--", color="green", label=f"Posición del obstáculo ({x_C} m)")

plt.title("Trayectoria del proyectil (Etapa B–C)")
plt.xlabel("Posición horizontal x (m)")
plt.ylabel("Altura vertical y (m)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
