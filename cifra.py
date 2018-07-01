# coding: utf-8
import operator

alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

caracteres_especiais = ['?', ',', ':', ' ', '.']

# chave = "WONDERWOMAN"
chave = "MAXIMOFF"

LIMITE_SUPERIOR = 126
LIMITE_INFERIOR = 32

def is_posicao_de_uma_letra(pos):
    return (pos >= 65 and pos <= 90) or (pos >= 97 and pos <= 122)

class Cifra():
    def definir_lista_circular(self, lista):
        while True:
            for nodo in lista:
                yield nodo

    def criptografar_conteudo(self, conteudo):
        chave_circular = self.definir_lista_circular(chave)
        texto = ""
        for caractere in conteudo:
            letra_chave = next(chave_circular)
            ascii = ord(caractere)

            if caractere not in caracteres_especiais and is_posicao_de_uma_letra(ascii):
                pos = ascii + alfabeto.index(letra_chave)
                if pos > LIMITE_SUPERIOR:
                    pos -= LIMITE_SUPERIOR
                if pos < LIMITE_INFERIOR:
                    pos += LIMITE_INFERIOR
                nova_letra = chr(pos)
            else:
                nova_letra = caractere

            texto += nova_letra
        return texto

    def descriptografar_conteudo(self, conteudo):
        chave_circular = self.definir_lista_circular(chave)
        texto = ""
        for caractere in conteudo:
            letra_chave = next(chave_circular)
            ascii = ord(caractere)

            if caractere not in caracteres_especiais:
                pos = ascii - alfabeto.index(letra_chave)
                if pos < LIMITE_INFERIOR:
                    pos = ascii + LIMITE_SUPERIOR - alfabeto.index(letra_chave) - LIMITE_INFERIOR
                nova_letra = chr(pos)
            else:
                nova_letra = caractere
            texto += nova_letra
        return texto

    # TODO: remover esse método se não for utilizado pra generalizar
    def resolve_criptografia(self, conteudo, decrypt=False):
        chave_circular = self.definir_lista_circular(chave)
        texto = ""
        operador = operator.sub if decrypt else operator.add
        for caractere in conteudo:
            print(caractere)
            letra_chave = next(chave_circular)
            print(letra_chave)
            ascii = ord(caractere)
            print(ascii)

            if (decrypt and ascii != LIMITE_INFERIOR) or (not decrypt and ascii != LIMITE_INFERIOR and is_posicao_de_uma_letra(ascii)):
                pos = operador(ascii, alfabeto.index(letra_chave))
                tentativas = 0
                while validar_posicao(pos) and tentativas < 3:
                    pos = posicao_interna
                    tentativas += 1

                print(pos)
                nova_letra = chr(pos)
            else:
                nova_letra = caractere

            print(nova_letra)
            print("----------------")
            texto += nova_letra
        return texto
