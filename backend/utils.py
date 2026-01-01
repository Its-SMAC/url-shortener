import secrets
import string

NUM_CHAR = 6

def gerar_codigo_curto():
    letras_numeros = string.ascii_letters + string.digits
    code: list = []
    for _ in range(NUM_CHAR):
        code.append(secrets.choice(letras_numeros))
    return ''.join(code)

if __name__ == '__main__':
    print(gerar_codigo_curto())
    print(gerar_codigo_curto())
    print(gerar_codigo_curto())