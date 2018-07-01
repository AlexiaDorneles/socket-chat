#-*- coding: UTF-8 -*-
from socket import *
from threading import Thread
from cifra import Cifra
import hashlib
import codecs
import sys
import re

# Para codificação no terminal do windows
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

porta = 12001
host = 'localhost'

def custom_print(string, sucesso=True):
    if sucesso: print('\x1b[%sm%s\x1b[0m' % ("32", string))
    else: print('\x1b[%sm%s\x1b[0m' % ("31", string))

def receber_resposta_servidor(clienteSoc, breakLoop=False):
	while True:
		msg = clienteSoc.recv(1024).decode("utf-8")
		custom_print(msg)
		if (breakLoop):
			return msg
			break

def converter_e_enviar(clienteSoc, conteudo):
	clienteSoc.send(bytearray(gerar_hash(conteudo), 'utf-8'))

def printar_comandos():
	custom_print("--------------------------------------------------------------------\n")
	custom_print("Lista de comandos: \n-QUIT = sair do chat\n-LIST = lista os usuários conectados\n-SEND mensagem TO usuario = Para enviar uma mensagem, substituindo os campos corretamente.\n-HELP = mostra novamente a lista de comandos")
	custom_print("--------------------------------------------------------------------\n")

def gerar_hash(msg):
    return hashlib.sha224(bytearray(msg, "utf-8")).hexdigest() + "HASH" + msg

if __name__ == '__main__':
	try:
		encripter = Cifra()
		clienteSoc = socket(AF_INET, SOCK_STREAM)
		clienteSoc.connect((host,porta))

		custom_print("---------------------------\n")
		custom_print("Bem vindo ao Terminal Chat!\n")
		custom_print("---------------------------\n")

		receber_resposta_servidor(clienteSoc, True)

		while True:
			nick = input( 'Informe o seu nome de usuario: \n')
			converter_e_enviar(clienteSoc, nick)
			msg = receber_resposta_servidor(clienteSoc, True)
			if "com sucesso" in msg: break

		t = Thread(target=receber_resposta_servidor, args=(clienteSoc,))
		t.setDaemon(True)
		t.start()

		printar_comandos()
		while True:
			stringInput = input('')
			if stringInput is not '':
				comando = stringInput.split()[0]
				if comando == 'QUIT':
					custom_print("Obrigado por utilizar o Terminal Chat!\nVolte Sempre ;)")
					converter_e_enviar(clienteSoc, "SAIR")
					clienteSoc.close()
					exit(1)
					break
				elif comando == 'LIST':
					converter_e_enviar(clienteSoc, stringInput)
				elif comando == 'SEND':
					conteudoMensagem = re.match(r"SEND(.*)TO", stringInput).group(1).strip()
					conteudoCriptografado = encripter.criptografar_conteudo(conteudoMensagem)
					usuarioAlvo = stringInput.split("TO")[1].strip()
					converter_e_enviar(clienteSoc, "SEND %s TO %s" % (conteudoCriptografado, usuarioAlvo))
				elif comando == 'HELP':
					printar_comandos()
				else:
					custom_print('Comando inválido.\nDigite HELP para ver a lista de comandos novamente\n ')

	except timeout:
  		custom_print("Tempo exedido!", False)
	except error:
		custom_print("Erro no Cliente: %s" % (host), False)
