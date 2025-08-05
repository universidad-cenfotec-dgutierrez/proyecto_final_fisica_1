# === Etapa C–D: Rebote después del impacto ===
import json
import math
import numpy as np
import matplotlib.pyplot as plt

# Gravedad
g = 9.81

# Cargar datos de A–B y B–C
with open("salida_AB.json", "r") as f:
    datos_AB = json.load(f)

with open("salida_BC.json", "r") as f:
    datos_BC = json.load(f)

# Verificar si hubo impacto
if not datos_BC.get("impacto", False):
    print("No hay impacto. Etapa C–D no se ejecuta.")
    exit()

# === DATOS DE PARTIDA ===
v_B = datos_AB["v_B"]
theta_rad = datos_AB["theta_rad"]

x_C = datos_BC["x_C"]
y_C = datos_BC["y_C"]
t_C = datos_BC["t_C"]
vx = datos_BC["v_x"]
vy = datos_BC["v_y"]

# Solicitar coeficiente de restitución co2n validación
try:
    e = float(input("Ingrese el coeficiente de restitución (e, entre 0 y 1): "))
    if not (0 <= e <= 1):
        raise ValueError("El coeficiente de restitución debe estar entre 0 y 1.")
except ValueError as error:
    print(f"Error: {error}")
    exit()

# Ángulo de la pared (45°)
theta_pared_rad = math.radians(45)

# Transformar velocidad al sistema tangencial/normal
v_t = vx * math.cos(theta_pared_rad) + vy * math.sin(theta_pared_rad)
v_n = -vx * math.sin(theta_pared_rad) + vy * math.cos(theta_pared_rad)

# Aplicar rebote
v_t_post = v_t
v_n_post = -e * v_n

# Volver a sistema original
v_x_post = v_t_post * math.cos(theta_pared_rad) - v_n_post * math.sin(theta_pared_rad)
v_y_post = v_t_post * math.sin(theta_pared_rad) + v_n_post * math.cos(theta_pared_rad)

# Calcular magnitud y ángulo
v_rebote = math.sqrt(v_x_post**2 + v_y_post**2)
beta_deg = math.degrees(math.atan2(v_y_post, v_x_post))

# Mostrar resultados
print("\n--- RESULTADOS DEL REBOTE ---")
print(f"Velocidad después del rebote: {v_rebote:.2f} m/s")
print(f"Ángulo después del rebote: {beta_deg:.2f}°")
print(f"v'_x = {v_x_post:.2f} m/s")
print(f"v'_y = {v_y_post:.2f} m/s")

# === GUARDAR RESULTADOS EN JSON ===
resultados_CD = {
    "v_rebote": v_rebote,
    "v_x_post": v_x_post,
    "v_y_post": v_y_post
}
with open("salida_CD.json", "w") as f:
    json.dump(resultados_CD, f, indent=4)

# === SIMULACIÓN COMPLETA: B–C + C–D ===

# Etapa B–C
v0x = v_B * math.cos(theta_rad)
v0y = v_B * math.sin(theta_rad)
t_vals_BC = np.linspace(0, t_C, 100)
x_BC = v0x * t_vals_BC
y_BC = v0y * t_vals_BC - 0.5 * g * t_vals_BC**2

# Etapa C–D
t_vals_CD = np.linspace(0, 1.5, 100)
x_CD = x_C + v_x_post * t_vals_CD
y_CD = y_C + v_y_post * t_vals_CD - 0.5 * g * t_vals_CD**2

# Pared inclinada 45°
pared_x = np.linspace(x_C - 2, x_C + 2, 2)
pared_y = y_C - (x_C - pared_x)

# === GRAFICAR ===
plt.figure(figsize=(10, 5))
plt.plot(x_BC, y_BC, label="Trayectoria antes del choque (B–C)", color="blue")
plt.plot(x_CD, y_CD, label="Trayectoria después del choque (C–D)", color="orange")
plt.plot(pared_x, pared_y, 'r--', label="Pared inclinada 45°")
plt.plot(x_C, y_C, 'ko', label="Punto de colisión")

plt.title("Trayectoria completa con rebote (B–C + C–D)")
plt.xlabel("Posición horizontal x (m)")
plt.ylabel("Altura vertical y (m)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()