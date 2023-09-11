from socket import *
import random
import math
from decimal import *

serverName = "192.168.0.39"  # IPv4 // ::1 IPv6
serverPort = 12500
clientSocket = socket(AF_INET, SOCK_DGRAM)  # AF_INET6

p = 0
q = 0

n = 0 #publica
e = 0 #publica
d = 0 #privada
m = 0

dserver = 0
nserver = 0

def getKeys(clientSocket, numero):
    global dserver, nserver
    response, serverAddress = clientSocket.recvfrom(4096)
    decoded_response = response.decode("utf-8")
    print("Received response from server:", decoded_response)

    text = decoded_response
    if (len(text) != 0):
        if (numero == 1):
            dserver = text
            decoded_response = dserver
        elif (numero == 2):
            nserver = text
            decoded_response = nserver


print("UDP Client\n")

def genereate():
    global p,q,n,e,d,m
    bitlen = 4096  # Tamanho desejado para os números primos
    random_seed = 100  # Semente para geração de números aleatórios
    random_generator = random.Random(random_seed)

# Gerar números primos p e q
    p = random.getrandbits(bitlen // 2)
    q = random.getrandbits(bitlen // 2)

    n = p * q

    m = (p - 1) * (q - 1)

    # Inicialize "e" com o valor 3
    e = 3

    # Verifique se "e" e m.gcd(e) são primos entre si
    while math.gcd(e, m) > 1:
        e += 2 
    
    d = mod_inverse(e, m)

def cifrar(msg):
    global n,d,e,dserver,nserver
    msg_numeric = int.from_bytes(msg.encode('utf-8'), byteorder='big')
    # Calcule a mensagem cifrada
    msg_cifrada = pow(msg_numeric, e, int(nserver))
    # Converta a mensagem cifrada em uma string
    msg_cifrada_str = str(msg_cifrada)
    print("Mensagem cifrada:", msg_cifrada_str)
    return msg_cifrada_str

def decifrar(msg):
    global n,d,e
    msgcifrada = int(msg)
    # Calcule a mensagem decifrada
    msg_decifrada_numeric = pow(msgcifrada, d, n) 
    # Converta a mensagem decifrada em uma string
    msg_decifrada_bytes = msg_decifrada_numeric.to_bytes((msg_decifrada_numeric.bit_length() + 7) // 8, byteorder='big')
    msg_decifrada_str = msg_decifrada_bytes.decode('utf-8')
    return msg_decifrada_str

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


genereate()

while 1:

    message = e
    if isinstance(message, str):
        clientSocket.sendto(bytes(message, "utf-8"), (serverName, serverPort))
    else:
        message = str(message)
        clientSocket.sendto(bytes(message, "utf-8"), (serverName, serverPort))
    getKeys(clientSocket, 1)

    message = n
    if isinstance(message, str):
        clientSocket.sendto(bytes(message, "utf-8"), (serverName, serverPort))
    else:
        message = str(message)
        clientSocket.sendto(bytes(message, "utf-8"), (serverName, serverPort))
    getKeys(clientSocket, 2)

    message = input("Digite sua mensagem: ")
    if message == "exit":
        break
    
    message = cifrar(message)
    if isinstance(message, str):
        clientSocket.sendto(bytes(message, "utf-8"), (serverName, serverPort))
    else:
        message = str(message)
        clientSocket.sendto(bytes(message, "utf-8"), (serverName, serverPort))

clientSocket.close()
