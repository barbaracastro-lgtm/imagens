import socket
import cv2
from imagem import Imagem
from protocolo import enviar_mensagem, receber_mensagem

HOST = 'localhost'
PORT = 5000
CAMINHO_IMAGEM = 'imagem_teste.jpeg'  # altere para o caminho da sua imagem


def main():
    # Lê a imagem do disco e codifica em JPEG
    img = Imagem.ler(CAMINHO_IMAGEM)
    dados = img.codificar()

    # Conecta ao servidor, envia a imagem e aguarda o resultado
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado ao servidor {HOST}:{PORT}")
        enviar_mensagem(s, dados)
        resposta = receber_mensagem(s)

    if resposta is None:
        print("Erro: servidor encerrou a conexão sem resposta.")
        return

    # Decodifica e exibe o resultado
    resultado = Imagem.decodificar(resposta)
    cv2.imshow('Resultado - Deteccao de Faces', resultado.pixels)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
