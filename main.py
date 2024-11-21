from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import base64

# Função para cifrar a mensagem
def encrypt(message, key):
    iv = os.urandom(16)  # Gera um vetor de inicialização (IV) aleatório
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Padding para alinhar ao tamanho do bloco
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode('utf-8')  # Retorna IV + texto cifrado em Base64

# Função para decifrar a mensagem
def decrypt(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)  # Decodifica Base64
    iv = ciphertext[:16]  # Extrai o vetor de inicialização (IV)
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Decifra os dados
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove o padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()

def main():
    print("=== Cifração Simétrica com AES ===")
    
    # Gera uma chave de 256 bits (32 bytes) automaticamente
    key = os.urandom(32)
    print("Chave de criptografia gerada automaticamente (Base64):", base64.b64encode(key).decode('utf-8'))

    # Solicita a mensagem ao usuário
    message = input("Digite a mensagem que deseja cifrar: ")

    # Cifra a mensagem
    encrypted = encrypt(message, key)
    print("\nTexto cifrado (Base64):", encrypted)

    # Decifra a mensagem
    decrypted = decrypt(encrypted, key)
    print("Texto decifrado:", decrypted)

if __name__ == "__main__":
    main()
