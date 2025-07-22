#!/usr/bin/env python3
"""
Explorador de Red Doméstica - Descubrimiento Pasivo
Identifica dispositivos en tu red local de manera respetuosa y no intrusiva
"""

import socket
import subprocess
import time
import json
import os
from datetime import datetime
import threading
import queue

class NetworkExplorer:
    def __init__(self, output_file="dispositivos_red.txt"):
        self.output_file = output_file
        self.dispositivos_encontrados = {}
        self.mi_ip = self.obtener_mi_ip()
        self.red_base = ".".join(self.mi_ip.split(".")[:-1]) + "."

    def obtener_mi_ip(self):
        """Obtiene la IP local de este dispositivo"""
        try:
            # Conectar a un servidor externo para obtener la IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            return ip_local
        except:
            return "192.168.1.100"  # fallback común

    def ping_suave(self, ip):
        """Realiza un ping muy suave a una IP"""
        try:
            # En Windows usa -n, en Linux/Mac usa -c
            param = "-n" if os.name == "nt" else "-c"
            # Solo 1 ping con timeout de 2 segundos
            resultado = subprocess.run(
                ["ping", param, "1", "-W", "2000" if os.name == "nt" else "-W", "2", ip],
                capture_output=True,
                text=True,
                timeout=5
            )
            return resultado.returncode == 0
        except:
            return False

    def obtener_nombre_dispositivo(self, ip):
        """Intenta obtener el nombre del dispositivo de manera pasiva"""
        try:
            # Resolución DNS inversa
            nombre = socket.gethostbyaddr(ip)[0]
            return nombre
        except:
            try:
                # Intento alternativo con getfqdn
                nombre = socket.getfqdn(ip)
                if nombre != ip:
                    return nombre
            except:
                pass
        return "Dispositivo desconocido"

    def detectar_tipo_dispositivo(self, ip, nombre):
        """Detecta el posible tipo de dispositivo basándose en patrones del nombre"""
        nombre_lower = nombre.lower()

        if any(palabra in nombre_lower for palabra in ['router', 'gateway', 'modem']):
            return "Router/Gateway"
        elif any(palabra in nombre_lower for palabra in ['iphone', 'android', 'mobile']):
            return "Teléfono móvil"
        elif any(palabra in nombre_lower for palabra in ['laptop', 'pc', 'desktop', 'computer']):
            return "Computadora"
        elif any(palabra in nombre_lower for palabra in ['smart', 'tv', 'roku', 'chromecast']):
            return "Smart TV/Streaming"
        elif any(palabra in nombre_lower for palabra in ['printer', 'hp', 'canon', 'epson']):
            return "Impresora"
        elif any(palabra in nombre_lower for palabra in ['alexa', 'google', 'echo']):
            return "Asistente inteligente"
        else:
            return "Dispositivo de red"

    def explorar_ip(self, ip, resultados_queue):
        """Explora una IP específica de manera no intrusiva"""
        if self.ping_suave(ip):
            nombre = self.obtener_nombre_dispositivo(ip)
            tipo = self.detectar_tipo_dispositivo(ip, nombre)

            dispositivo = {
                'ip': ip,
                'nombre': nombre,
                'tipo': tipo,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'activo': True
            }

            resultados_queue.put(dispositivo)
            print(f"✓ Encontrado: {ip} - {nombre} ({tipo})")

    def escaneo_pasivo(self):
        """Realiza un escaneo muy suave de la red"""
        print(f"Iniciando exploración pasiva de la red...")
        print(f"Tu IP: {self.mi_ip}")
        print(f"Explorando red: {self.red_base}x")
        print("Esto puede tomar varios minutos para ser respetuoso con la red...\n")

        resultados_queue = queue.Queue()
        threads = []

        # Explorar solo las IPs más comunes primero (1-50, 100-150)
        ips_comunes = list(range(1, 51)) + list(range(100, 151))

        for i in ips_comunes:
            ip = self.red_base + str(i)

            # Crear thread para cada IP
            thread = threading.Thread(target=self.explorar_ip, args=(ip, resultados_queue))
            threads.append(thread)
            thread.start()

            # Pausa entre intentos para ser muy respetuoso
            time.sleep(0.5)

            # Limitar threads concurrentes
            if len(threads) >= 5:
                for t in threads:
                    t.join()
                threads = []

        # Esperar a que terminen todos los threads
        for thread in threads:
            thread.join()

        # Recoger resultados
        while not resultados_queue.empty():
            dispositivo = resultados_queue.get()
            self.dispositivos_encontrados[dispositivo['ip']] = dispositivo

    def guardar_resultados(self):
        """Guarda los resultados en un archivo de texto legible"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("EXPLORACIÓN DE RED DOMÉSTICA\n")
            f.write("=" * 60 + "\n")
            f.write(f"Fecha de exploración: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Tu IP: {self.mi_ip}\n")
            f.write(f"Red explorada: {self.red_base}x\n")
            f.write(f"Dispositivos encontrados: {len(self.dispositivos_encontrados)}\n\n")

            if self.dispositivos_encontrados:
                for ip, dispositivo in sorted(self.dispositivos_encontrados.items()):
                    f.write("-" * 40 + "\n")
                    f.write(f"IP: {dispositivo['ip']}\n")
                    f.write(f"Nombre: {dispositivo['nombre']}\n")
                    f.write(f"Tipo estimado: {dispositivo['tipo']}\n")
                    f.write(f"Detectado: {dispositivo['timestamp']}\n")
                    f.write(f"Estado: {'Activo' if dispositivo['activo'] else 'Inactivo'}\n")
                    f.write("\n")
            else:
                f.write("No se encontraron dispositivos adicionales.\n")

            f.write("=" * 60 + "\n")
            f.write("NOTAS:\n")
            f.write("- Esta exploración fue realizada de manera pasiva y respetuosa\n")
            f.write("- Solo se usaron técnicas de ping suave y resolución DNS\n")
            f.write("- Algunos dispositivos pueden no aparecer si tienen firewall activo\n")
            f.write("- Los nombres y tipos son estimaciones basadas en respuestas de red\n")

    def mostrar_resumen(self):
        """Muestra un resumen en pantalla"""
        print("\n" + "=" * 50)
        print("RESUMEN DE EXPLORACIÓN")
        print("=" * 50)
        print(f"Dispositivos encontrados: {len(self.dispositivos_encontrados)}")

        if self.dispositivos_encontrados:
            print("\nDispositivos activos:")
            for ip, dispositivo in sorted(self.dispositivos_encontrados.items()):
                print(f"  • {ip} - {dispositivo['nombre']} ({dispositivo['tipo']})")

        print(f"\nResultados guardados en: {self.output_file}")
        print("Exploración completada de manera respetuosa.")

    def ejecutar(self):
        """Ejecuta la exploración completa"""
        start_time = time.time()

        try:
            self.escaneo_pasivo()
            self.guardar_resultados()
            self.mostrar_resumen()

            elapsed_time = time.time() - start_time
            print(f"\nTiempo total: {elapsed_time:.1f} segundos")

        except KeyboardInterrupt:
            print("\n\nExploración interrumpida por el usuario.")
            if self.dispositivos_encontrados:
                self.guardar_resultados()
                print(f"Resultados parciales guardados en: {self.output_file}")
        except Exception as e:
            print(f"\nError durante la exploración: {e}")

def main():
    print("Explorador de Red Doméstica")
    print("Descubrimiento pasivo y respetuoso de dispositivos\n")

    # Permitir al usuario cambiar el archivo de salida
    archivo_salida = input("Archivo de salida (Enter para 'dispositivos_red.txt'): ").strip()
    if not archivo_salida:
        archivo_salida = "dispositivos_red.txt"

    explorer = NetworkExplorer(archivo_salida)
    explorer.ejecutar()

if __name__ == "__main__":
    main()