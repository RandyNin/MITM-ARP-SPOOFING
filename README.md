# MITM-ARP-SPOOFING

> **Autor:** Randy Nin **Laboratorio de Seguridad de Redes | GNS3**

Script de Python que realiza un ataque Man-in-the-Middle posicionando al atacante entre la víctima y el gateway mediante envenenamiento ARP. Envía ARP replies falsificados en ambas direcciones de forma continua, asociando las IPs legítimas de ambos extremos con la MAC del atacante e interceptando todo el tráfico que fluye entre ellos.

---

## Contenido del repositorio

```
MITM-ARP-SPOOFING/
├── arp-spoofing.py
├── Documentación Tecnica Profesional MITM-ARP SPOOFING(Randy Nin -- 2025-0660).pdf
└── README.md
```

---

## Documentación técnica

La documentación técnica completa de este laboratorio está disponible en:

**[Documentación Tecnica Profesional MITM-ARP SPOOFING(Randy Nin -- 2025-0660).pdf](Documentación%20Tecnica%20Profesional%20MITM-ARP%20SPOOFING(Randy%20Nin%20--%202025-0660).pdf)**

Incluye contexto técnico del protocolo ARP y su vulnerabilidad, topología y configuración del entorno, análisis completo del script, evidencia del ataque con capturas de pantalla, demostración de intercepción con Wireshark y contramedidas con Dynamic ARP Inspection.

---

## Requisitos

**Sistema:** ParrotSec OS, Kali Linux o cualquier distribución Linux con soporte para envío de paquetes raw.

**Python:** 3.x con permisos de superusuario (`sudo`).

**Dependencias externas:**

|Librería|Instalación|
|:--|:--|
|`scapy`|`pip install scapy`|
|`pwntools`|`pip install pwntools`|

**Instalación rápida:**

```bash
pip install scapy pwntools
```

---

## Uso

```bash
sudo python3 arp-spoofing.py -i <interfaz> -t <IP_víctima> -g <IP_gateway>
```

**Parámetros:**

|Flag|Descripción|
|:--|:--|
|`-i` / `--interface`|Interfaz de red del atacante|
|`-t` / `--target`|IP de la víctima|
|`-g` / `--gateway`|IP del gateway|

**Ejemplo usado en el laboratorio:**

```bash
sudo python3 arp-spoofing.py -i ens4 -t 20.25.6.61 -g 20.25.6.60
```

Presionar `Ctrl+C` para detener el ataque de forma limpia.

---

## Cómo funciona

El script resuelve primero las MACs de la víctima y el gateway mediante ARP requests legítimos. Con ambas MACs conocidas, entra en el loop de envenenamiento bidireccional:

|Dirección|ARP reply falsificado|
|:--|:--|
|Hacia víctima (20.25.6.61)|"La IP del gateway 20.25.6.60 está en mi MAC"|
|Hacia gateway (20.25.6.60)|"La IP de la víctima 20.25.6.61 está en mi MAC"|

Con IP forwarding activo en el sistema atacante, el tráfico es reenviado de forma transparente entre ambos extremos, manteniendo la conectividad de la víctima mientras todo su tráfico es interceptado.

**Activar IP forwarding:**

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

## Entorno de laboratorio

|Dispositivo|Rol|IP|MAC|
|:--|:--|:--|:--|
|R-1|Gateway / DHCP / NAT|20.25.6.60/24|0c:16:94:84:00:00|
|PC1|Víctima|20.25.6.61/24|00:50:79:66:68:00|
|Parrot-1|Atacante|20.25.6.62/24|0c:db:b8:ad:00:00|
|Sw-1|Switch capa 2|N/A|N/A|

> Red de laboratorio: 20.25.6.0/24

---

## Impacto observado

- Tabla ARP de PC1 envenenada: el gateway (20.25.6.60) queda asociado a la MAC del atacante
- Tabla ARP del router envenenada: la IP de PC1 (20.25.6.61) queda asociada a la MAC del atacante
- Todo el tráfico entre PC1 e internet transita por Parrot-1 de forma transparente
- Consultas DNS, credenciales en texto claro y tráfico no cifrado quedan expuestos al atacante

---

## Mitigación

Dynamic ARP Inspection (DAI) en el switch con ACL estática:

```
Switch(config)# arp access-list ARP_DAI
Switch(config-arp-nacl)# permit ip host 20.25.6.60 mac host 0c16.9484.0000
Switch(config-arp-nacl)# permit ip host 20.25.6.61 mac host 0050.7966.6800
Switch(config-arp-nacl)# permit ip host 20.25.6.62 mac host 0cdb.b8ad.0000
Switch(config-arp-nacl)# exit
Switch(config)# ip arp inspection filter ARP_DAI vlan 1
Switch(config)# ip arp inspection vlan 1
Switch(config)# interface GigabitEthernet1/0
Switch(config-if)# ip arp inspection trust
```

Para entornos con DHCP dinámico, la documentación técnica incluye la configuración combinada de DAI con DHCP Snooping, que elimina la necesidad de mantener ACLs estáticas.

---

## Video demostrativo

**Enlace:** [https://youtu.be/DNBmjy7cqAo](https://youtu.be/DNBmjy7cqAo)

---

## Disclaimer

Este script fue desarrollado con fines exclusivamente académicos y educativos. Su uso está permitido únicamente en entornos propios o autorizados como GNS3, EVE-NG o laboratorios internos de prueba. El uso en redes de terceros sin autorización expresa constituye una violación legal.

---

_Randy Nin / Matrícula 2025-0660_

---
