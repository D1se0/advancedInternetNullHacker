# Herramientas de Monitoreo y Seguridad en Red

Este proyecto contiene dos herramientas diseñadas para monitorear y proteger tu `red local`. Una herramienta está basada en el monitoreo de direcciones **IP** y la otra en el monitoreo de **MACs**. Ambas herramientas funcionan con una lista de elementos permitidos que se definen en archivos de texto (`.txt`) específicos.

## Requisitos Previos

Antes de ejecutar estas herramientas, asegúrate de cumplir con los siguientes requisitos:

- **Linux** (preferiblemente basado en `Debian`, como `Kali Linux`).

- Herramientas instaladas:
  - `arp-scan`
  - `arpspoof`
  - `Python 3`

Puedes instalar `arp-scan` y `arpspoof` con el siguiente comando:

```bash
sudo apt-get install arp-scan dsniff
```

## Herramientas Incluidas

### 1. Herramienta Basada en IP

### Descripción

Esta herramienta monitorea las direcciones `IP` activas en tu `red local`. Detecta cualquier dirección `IP` desconocida (que no esté incluida en la lista permitida) y realiza un `ARP Spoofing` para desconectarla de la red.

## Configuración

Crea un archivo llamado `permitted_ip.txt` en el mismo directorio del script.
Agrega las direcciones `IP` permitidas, una por línea.

### Ejecución

Ejecuta el script de la herramienta basada en `IP` con el siguiente comando:

```bash
python3 advanceInternetNullHacker_IP.py
```

Durante la ejecución, deberás ingresar la interfaz de red (por ejemplo, `wlan0` o `eth0`).

### 2. Herramienta Basada en MAC

### Descripción

Esta herramienta monitorea las direcciones `MAC` activas en tu red local. Detecta cualquier dirección `MAC` desconocida (que no esté incluida en la lista permitida) y realiza un `ARP Spoofing` contra la `IP` asociada.

## Configuración

Crea un archivo llamado `permitted_mac.txt` en el mismo directorio del script.
Agrega las direcciones `MAC` permitidas, una por línea.

### Ejecución

Ejecuta el script de la herramienta basada en `MAC` con el siguiente comando:

```bash
python3 advanceInternetNullHacker_MAC.py
```

Durante la ejecución, deberás ingresar la interfaz de red (por ejemplo, `wlan0` o `eth0`).

Identificación de Dispositivos Activos: `knowIP.sh`

El script `knowIP.sh` te permite identificar los dispositivos actualmente conectados a tu red local. Utiliza `arp-scan` para obtener una lista de las direcciones `IP` y `MAC` activas.

## Uso

Ejecuta el script con el siguiente comando:

```bash
bash knowIP.sh
```

Durante la ejecución, deberás ingresar la interfaz de red (por ejemplo, `wlan0` o `eth0`). Este script generará una lista de dispositivos conectados en formato:

```
192.168.1.1     c0:3c:04:3f:63:60       Nombre del Fabricante
192.168.1.2     00:11:22:33:44:55       Nombre del Fabricante
```

Utiliza esta información para actualizar los archivos `permitted_ip.txt` y `permitted_mac.txt`.

### Archivos de Configuración

`permitted_ip.txt`: Lista de direcciones `IP` permitidas. Cada dirección debe ir en una línea separada.
`permitted_mac.txt`: Lista de direcciones `MAC` permitidas. Cada dirección debe ir en una línea separada.

Asegúrate de mantener estas listas actualizadas con las direcciones de tus dispositivos conocidos.

## Notas Importantes

Ambas herramientas ejecutan `ARP Spoofing` para desconectar dispositivos desconocidos. Esto podría ser detectado por sistemas de seguridad en redes más avanzadas.
Usa estas herramientas de manera responsable y únicamente en `redes que administras`.
Ejecuta los scripts con permisos de administrador (`sudo`) si encuentras problemas de permisos.

### Ejemplo de Flujo de Trabajo

Ejecuta knowIP.sh para identificar los dispositivos actuales en tu red.
Añade las direcciones IP o MAC detectadas en sus respectivos archivos (`permitted_ip.txt` o `permitted_mac.txt`).
Ejecuta la herramienta correspondiente (por `IP` o por `MAC`).
Monitorea el estado de los dispositivos conectados y desconecta aquellos desconocidos automáticamente.

## Contacto

Si tienes alguna duda o mejora para estas herramientas, no dudes en compartirla. ¡Disfruta de una red más segura!

Creador: d1se0

Contacto: ciberseguridad12345@gmail.com
