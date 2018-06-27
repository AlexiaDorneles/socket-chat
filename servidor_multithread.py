#-*- coding: UTF-8 -*-
from socket import *
from threading import Thread
import re

porta = 12001
ip = 'localhost'	#localhost.

nick_con = {}

def receber_mensagem_cliente(con):
	return con.recv(1024).decode("utf-8")

def get_usuarios_conectados(prefixo):
	if len (nick_con) > 1:
		return prefixo.format("\n - " + "\n - ".join(list(nick_con.keys())) + "\n")
	else:
		return prefixo.format("".join(list(nick_con.keys()))  + "\n")

def enviar_para_cliente(con, conteudo):
	con.send(bytearray(conteudo, "utf-8"))

def inicia_servidor(servidorSoc):
	servidorSoc.bind((ip, porta))
	servidorSoc.listen(60)

	print("Servidor ativo!\nAguardando conexões.")

	while True:
		conexao, end_remoto = servidorSoc.accept()
		enviar_para_cliente(conexao, get_usuarios_conectados("Usuários conectados: {}"))
		t = Thread(target=trata_nova_conexao, args=(conexao, end_remoto))
		t.setDaemon(True)
		t.start()

def trata_nova_conexao(con, end_remoto):
	nick = receber_mensagem_cliente(con).strip()

	if nick in list(nick_con.keys()):
		resposta = nick + " ja esta em uso." + get_usuarios_conectados("Nicks em uso: {}")
		enviar_para_cliente(con, resposta)
		trata_nova_conexao(con, end_remoto)
	else:
		nick_con[nick] = con
		enviar_para_cliente(con, nick + " conectado com sucesso.\n")

		while True:
			msg_remota = receber_mensagem_cliente(con)
			if msg_remota == '' or msg_remota == 'SAIR':
				print("A conexao com ", nick, " foi fechada.\n")
				con.close()
				del nick_con[nick]
				break

			elif msg_remota.split()[0] == 'SEND':
				usuarioAlvo = msg_remota.split("TO")[1].strip()
				if usuarioAlvo not in list(nick_con.keys()):
					enviar_para_cliente(con, "O usuário %s não está conectado" % (usuarioAlvo))
				else:
					try:
						conUsuarioAlvo = nick_con[usuarioAlvo]
						conteudoMensagem = re.match(r"SEND(.*)TO", msg_remota).group(1)
						mensagem = "Mensagem de %s: %s" % (nick, conteudoMensagem)
						enviar_para_cliente(conUsuarioAlvo, mensagem)
					except error:
						enviar_para_cliente(con, "O usuário %s não está online no momento" % (usuarioAlvo))

			elif msg_remota.split()[0] == 'LIST':
				enviar_para_cliente(con, get_usuarios_conectados("Usuários conectados: {}"))

#Função principal.
if __name__ == '__main__':
	try:
		servidorSoc = socket(AF_INET, SOCK_STREAM)	#Socket TCP
		t2 = Thread(target=inicia_servidor, args=(servidorSoc,))
		t2.setDaemon(True)
		t2.start()

		while True:
			aux = input('')
			if aux == 'FIM':
				print("Tchau!\n")
				servidorSoc.close()  #nunca!
				exit(1)

	except timeout:
  		print("Tempo exedido!")
	except error:
  		print("Erro no Servidor:", host)
  		exit(1)
