import socket
import threading
import cv2
from imagem import Imagem
from protocolo import enviar_mensagem, receber_mensagem

HOST = 'localhost'
PORT = 5000


def processar_imagem(img):
    """Detecta faces na imagem e desenha retângulos verdes. Não acessa sockets."""
    classificador = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    cinza = cv2.cvtColor(img.pixels, cv2.COLOR_BGR2GRAY)
    faces = classificador.detectMultiScale(
        cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )
    resultado = Imagem(pixels=img.pixels.copy())
    for (x, y, w, h) in faces:
        cv2.rectangle(resultado.pixels, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return resultado


def atender_cliente(conn, addr):
    """Função executada em uma thread separada para cada cliente."""
    print(f"Iniciou {addr}")
    # time.sleep(5)  # descomente apenas para o teste de dois clientes
    try:
        dados = receber_mensagem(conn)
        if dados is None:
            print(f"Falha ao receber imagem de {addr}")
            return
        img = Imagem.decodificar(dados)
        resultado = processar_imagem(img)
        enviar_mensagem(conn, resultado.codificar())
    except Exception as e:
        print(f"Erro ao atender {addr}: {e}")
    finally:
        conn.close()
    print(f"Terminou {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor aguardando conexoes em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True)
            t.start()


if __name__ == '__main__':
    main()
