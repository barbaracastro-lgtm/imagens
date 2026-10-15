import cv2
import numpy as np


class Imagem:
    def __init__(self, pixels=None):
        self.pixels = pixels  # numpy array com os dados da imagem

    @classmethod
    def ler(cls, caminho):
        """Lê uma imagem de um arquivo e retorna um objeto Imagem."""
        pixels = cv2.imread(caminho)
        if pixels is None:
            raise FileNotFoundError(f"Imagem não encontrada: {caminho}")
        return cls(pixels=pixels)

    def codificar(self):
        """Codifica a imagem em JPEG e retorna bytes."""
        sucesso, buffer = cv2.imencode('.jpg', self.pixels)
        if not sucesso:
            raise RuntimeError("Falha ao codificar imagem em JPEG")
        return buffer.tobytes()

    @classmethod
    def decodificar(cls, dados):
        """Decodifica bytes JPEG e retorna um objeto Imagem."""
        arr = np.frombuffer(dados, dtype=np.uint8)
        pixels = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if pixels is None:
            raise RuntimeError("Falha ao decodificar bytes JPEG")
        return cls(pixels=pixels)
