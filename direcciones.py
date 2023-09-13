from scapy.all import ARP, Ether, srp

# Definir la IP de la red que quieres escanear en formato CIDR (por ejemplo, 192.168.1.0/24)
ip_range = "192.168.15.0/24"

# Crear un paquete ARP
arp = ARP(pdst=ip_range)

# Crear un paquete Ethernet
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# Combinar el paquete Ethernet y el paquete ARP
packet = ether/arp

# Enviar el paquete y recibir respuestas
result = srp(packet, timeout=3, verbose=0)[0]

# Mostrar las direcciones IP y MAC encontradas
for sent, received in result:
    print(f"IP: {received.psrc}   MAC: {received.hwsrc}")
