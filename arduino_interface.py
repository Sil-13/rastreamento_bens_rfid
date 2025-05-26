import serial
import mysql.connector
from mysql.connector import Error

# Configurações
ARDUINO_PORT = 'COM3'  # ou '/dev/ttyUSB0' no Linux
BAUD_RATE = 9600
DB_CONFIG = {
    'host': 'localhost',
    'database': 'gestao_bens_escolares',
    'user': 'root',
    'password': 'senha'
}

def process_rfid_tag(tag):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Verifica se é um bem
        cursor.execute("SELECT id FROM bens WHERE rfid_tag = %s", (tag,))
        bem = cursor.fetchone()
        
        if bem:
            print(f"Bem detectado: ID {bem['id']}")
            # Aqui você pode implementar a lógica de movimentação
            # Por exemplo, mover para um ambiente padrão
            cursor.execute("""
                INSERT INTO movimentacoes (bem_id, destino_id, usuario_id)
                VALUES (%s, 1, 1)  # Valores exemplo
            """, (bem['id'],))
            conn.commit()
            print("Movimentação registrada no banco de dados")
        
    except Error as e:
        print("Erro no banco de dados:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def main():
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line.startswith("RFID Tag:"):
                    tag = line.split(":")[1].strip()
                    print(f"Tag lida: {tag}")
                    process_rfid_tag(tag)
    except KeyboardInterrupt:
        print("Programa encerrado")
    finally:
        ser.close()

if __name__ == "__main__":
    main()