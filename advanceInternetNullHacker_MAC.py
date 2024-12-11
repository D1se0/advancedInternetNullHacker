import subprocess
import time
import sys
from collections import defaultdict

# Archivos
PERMITTED_MACS_FILE = "permitted_mac.txt"

# Colores
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

# Variables globales
detected_unknown_macs = set()
disconnected_macs = set()
unknown_mac_count = defaultdict(int)

def load_permitted_macs():
    """Carga las MACs permitidas desde el archivo."""
    try:
        with open(PERMITTED_MACS_FILE, "r") as file:
            return {line.strip().lower() for line in file if line.strip()}
    except FileNotFoundError:
        print(f"{RED}[!] Archivo {PERMITTED_MACS_FILE} no encontrado.{RESET}")
        return set()

def get_network_hosts(interface):
    """
    Obtiene las MACs e IPs de la red usando arp-scan.
    Devuelve una lista de tuplas (ip, mac).
    """
    try:
        result = subprocess.check_output(
            ["arp-scan", "-I", interface, "--localnet"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        hosts = []
        for line in result.splitlines():
            parts = line.split()
            if len(parts) >= 2 and ":" in parts[1]:
                ip, mac = parts[0], parts[1].lower()
                hosts.append((ip, mac))
        return hosts
    except subprocess.CalledProcessError:
        print(f"{RED}[!] Error al ejecutar arp-scan.{RESET}")
        return []

def spoof_disconnect(interface, target_ip):
    """
    Ejecuta arpspoof para desconectar una IP desconocida.
    """
    gateway = "192.168.1.1"  # Cambiar según tu red
    try:
        subprocess.Popen(
            ["arpspoof", "-i", interface, "-t", target_ip, gateway],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"{RED}[!] Error al ejecutar arpspoof para {target_ip}: {e}{RESET}")

def display_status(detected_count, disconnected_count):
    """Sobrescribe el estado de los contadores en la terminal."""
    # Sobrescribe la línea en lugar de imprimir varias líneas
    sys.stdout.write(f"\r{BLUE}--- Resumen --- "
                     f"{RED}[!] MACs desconocidas detectadas: {detected_count} "
                     f"{GREEN}[+] MACs desconectadas: {disconnected_count}{RESET}")
    sys.stdout.flush()

def main():
    interface = input(f"{YELLOW}[?] Ingresa la interfaz de red (ejemplo: wlan0): {RESET}").strip()
    if not interface:
        print(f"{RED}[-] Debes ingresar una interfaz de red.{RESET}")
        return

    permitted_macs = load_permitted_macs()
    print(f"{GREEN}[+] MACs permitidas cargadas: {len(permitted_macs)}{RESET}\n")
    print(f"{BLUE}[+] Comenzando monitoreo...{RESET}")

    current_macs = set()  # MACs conectadas actualmente

    while True:
        try:
            new_macs = set()
            current_hosts = get_network_hosts(interface)
            for ip, mac in current_hosts:
                new_macs.add(mac)

                if mac not in permitted_macs:
                    if mac not in detected_unknown_macs:
                        detected_unknown_macs.add(mac)
                        print(f"\n{RED}[!] MAC desconocida detectada: {mac} (IP: {ip}){RESET}")
                        spoof_disconnect(interface, ip)
                        unknown_mac_count[mac] += 1

            # Detectar MACs desconectadas
            for mac in current_macs:
                if mac not in new_macs and mac in detected_unknown_macs and mac not in disconnected_macs:
                    disconnected_macs.add(mac)
                    print(f"\n{GREEN}[+] MAC desconectada: {mac}{RESET}")

            current_macs = new_macs

            # Mostrar resumen actualizado
            display_status(len(detected_unknown_macs), len(disconnected_macs))
            time.sleep(2)  # Ajustado para mejor actualización
        except KeyboardInterrupt:
            print(f"\n{RED}[-] Interrupción detectada. Saliendo...{RESET}")
            display_status(len(detected_unknown_macs), len(disconnected_macs))
            break

if __name__ == "__main__":
    main()
