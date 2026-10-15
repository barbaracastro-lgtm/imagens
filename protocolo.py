import struct


def _ler_bytes(sock, total):
    """Lê exatamente 'total' bytes do socket, acumulando chamadas ao recv."""
    dados = b''
    while len(dados) < total:
        restante = total - len(dados)
        chunk = sock.recv(restante)
        if chunk == b'':
            return None  # conexão encerrada antes de terminar
        dados += chunk
    return dados


def enviar_mensagem(sock, dados):
    """Envia bytes com cabeçalho de 4 bytes indicando o tamanho (big-endian)."""
    tamanho = len(dados)
    cabecalho = struct.pack('>I', tamanho)
    sock.sendall(cabecalho + dados)


def receber_mensagem(sock):
    """Recebe uma mensagem: lê o cabeçalho de 4 bytes e depois os dados."""
    cabecalho = _ler_bytes(sock, 4)
    if cabecalho is None:
        return None
    tamanho = struct.unpack('>I', cabecalho)[0]
    return _ler_bytes(sock, tamanho)
