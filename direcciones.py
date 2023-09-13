from scapy.all import ARP, Ether, srp

# Dirección IP y máscara de tu red local (en formato CIDR)
# Por ejemplo, si tu red es 192.168.1.0/24, entonces la dirección IP sería "192.168.1.0/24"
network = "192.168.15.255/24"
direcciones_ip  = []
# Crea un paquete ARP para hacer un escaneo de la red local
arp = ARP(pdst=network)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast Ethernet frame

packet = ether / arp

# Realiza el escaneo enviando el paquete ARP
result = srp(packet, timeout=3, verbose=0)[0]

# Lista para almacenar las direcciones IP y las direcciones MAC de los dispositivos encontrados
devices = []

# Recorre los resultados y agrega los dispositivos a la lista
for sent, received in result:
    devices.append({'ip': received.psrc, 'mac': received.hwsrc})

# Imprime la lista de dispositivos encontrados
print("Dispositivos en la red local:")
print("IP\t\t\tMAC Address")
print("-----------------------------------------")
for device in devices:
    direcciones_ip.append({device['ip']})
    #print(f"{device['ip']}\t\t{device['mac']}")
print(type(direcciones_ip[0]))
