import socket
import json

HOST = '127.0.0.1'
PORT = 65432

def enviar_tarea(id_tarea, descripcion):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            payload = json.dumps({"id": id_tarea, "descripcion": descripcion})
            
            print(f"[CLIENTE] Enviando: {descripcion}")
            s.sendall(payload.encode('utf-8'))
            
            respuesta_raw = s.recv(1024)
            respuesta = json.loads(respuesta_raw.decode('utf-8'))
            print(f"[CLIENTE] Respuesta del servidor: {respuesta}\n")
            
        except ConnectionRefusedError:
            print("[ERROR] Conexión rechazada. Asegúrate de encender el servidor primero.")

if __name__ == "__main__":
    print("--- Iniciando simulación de envío de tareas ---")
    enviar_tarea(1, "Procesar pago de usuario mediante pasarela")
    enviar_tarea(2, "Subir imagen de perfil a S3")
    enviar_tarea(3, "Actualizar registro de logs en PostgreSQL")