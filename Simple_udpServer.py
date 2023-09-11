from socket import *
import random
import math
from decimal import *
serverPort = 12500
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

p = 0
q = 0

n = 0 #publica
e = 0 #publica
d = 0 #privada
m = 0

dclient = 0
nclient = 0

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
    global n,d,e
    msg_numeric = int.from_bytes(msg.encode('utf-8'), byteorder='big')
    # Calcule a mensagem cifrada
    msg_cifrada = pow(float(msg_numeric), e, n)
    # Converta a mensagem cifrada em uma string
    msg_cifrada_str = str(msg_cifrada)
    print("Mensagem cifrada:", msg_cifrada_str)

def decifrar(msg):
    global n,d,e
    # digits_str = ''.join(filter(str.isdigit, msg))
    # msgcifrada_int = int(digits_str)


    # digits_client = ''.join(filter(str.isdigit, dclient))
    # dclient_int = int(digits_client)
    
    # msg_decifrada_numeric = pow(msgcifrada_int, d, dclient_int)

    # # Converta a mensagem decifrada em uma string
    # msg_decifrada_bytes = msg_decifrada_numeric.to_bytes((msg_decifrada_numeric.bit_length() + 7) // 8, byteorder='big')
    # msg_decifrada_str = msg_decifrada_bytes.decode('utf-8')

    # # Converte a mensagem cifrada em uma lista de inteiros
    # encrypted_message = [int(char) for char in msg.split()]

    # # Descriptografa cada número
    # decrypted_message = ''.join([chr(pow(char, d, int(n))) for char in encrypted_message])

    global n,d,e
    msgcifrada = int(msg)
    # Calcule a mensagem decifrada
    msg_decifrada_numeric = pow(msgcifrada, d, n)
    # Converta a mensagem decifrada em uma string
    msg_decifrada_bytes = msg_decifrada_numeric.to_bytes(msg_decifrada_numeric.bit_length(), byteorder='big')
    print(msg_decifrada_bytes)
    msg_decifrada_str = msg_decifrada_bytes.decode('utf-8')
    return msg_decifrada_str

    return decrypted_message

    return msg_decifrada_str

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


genereate()

print("UDP server\n")
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    text = str(message, 'utf-8')  # cp1252 #utf-8
    sendMessage = False
    if (nclient == 0):
        nclient = text
        text = ''
        response_message = e
        serverSocket.sendto(
            str(response_message).encode("utf-8"), clientAddress)
    elif (dclient == 0):
        dclient = text
        text = ''
        response_message = n
        serverSocket.sendto(
            str(response_message).encode("utf-8"), clientAddress)
    elif(text != '' and text != nclient and text != dclient):
        text = decifrar(text)
        print("Received from Client: ", text)
        sendMessage = False
