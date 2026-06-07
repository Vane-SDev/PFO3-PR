import socket
import json
import time
from concurrent.futures import ThreadPoolExecutor

HOST = '127.0.0.1'
PORT = 65432
MAX_WORKERS = 5 

def procesar_tarea(conn, addr):
    with conn:
        print(f"[WORKER] Conexión aceptada de {addr}")
        try:
            datos = conn.recv(1024)
            if datos:
                tarea = json.loads(datos.decode('utf-8'))
                print(f"[WORKER] Ejecutando tarea: {tarea['descripcion']}")
                
                # Simular una tarea I/O bound 
                time.sleep(2)
                
                respuesta = {
                    "status": "completado",
                    "id_tarea": tarea["id"],
                    "mensaje": "Procesado por el pool de hilos del worker"
                }
                conn.sendall(json.dumps(respuesta).encode('utf-8'))
                print(f"[WORKER] Tarea {tarea['id']} finalizada y enviada al cliente.")
        except Exception as e:
            print(f"[ERROR] Problema con la conexión {addr}: {e}")

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVIDOR] Escuchando peticiones en {HOST}:{PORT}")
        
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            while True:
                conn, addr = s.accept()
                pool.submit(procesar_tarea, conn, addr)

if __name__ == "__main__":
    iniciar_servidor()