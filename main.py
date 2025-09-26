import random
import os
import time

class Naipe:
    def __init__(self, nome, simbolo):
        self.nome = nome
        self.simbolo = simbolo


class Carta:
    def __init__(self, numero, naipe, peso):
        self.numero = numero
        self.naipe = naipe
        self.peso = peso

    def __str__(self):
        return f"[{self.numero}{self.naipe.simbolo}]"


class Baralho:
    cartas = []

    def __init__(self, naipes):
        self.naipes = naipes

    def criaBaralho(self):
        # criando o baralho
        for naipe in self.naipes:

            if naipe.nome == "paus": # zap
                self.cartas.append(Carta("4", naipe, 14))
            else:
                self.cartas.append(Carta("4", naipe, 1))

            self.cartas.append(Carta("5", naipe, 2))
            self.cartas.append(Carta("6", naipe, 3))

            if naipe.nome == "copas": # setão
                self.cartas.append(Carta("7", naipe, 13))
            elif naipe.nome == "ouros": # mole
                self.cartas.append(Carta("7", naipe, 11))
            else:
                self.cartas.append(Carta("7", naipe, 4))

            self.cartas.append(Carta("Q", naipe, 5))
            self.cartas.append(Carta("J", naipe, 6))
            self.cartas.append(Carta("K", naipe, 7))

            if naipe.nome == "espadas": # espadilha
                self.cartas.append(Carta("A", naipe, 12))
            else:
                self.cartas.append(Carta("A", naipe, 8))

                self.cartas.append(Carta("2", naipe, 9))
                self.cartas.append(Carta("3", naipe, 10))

    def sorteaCartaTiraDoBaralho(self):
        cartaSorteada = random.choice(self.cartas)
        self.cartas.remove(cartaSorteada)
        return cartaSorteada

    def sorteaUmaMao(self):
        cartas = []
        for i in range (0,3):
            cartas.append(self.sorteaCartaTiraDoBaralho())
        return Mao(cartas)


class Mao:
    def __init__(self, cartas):
        self.cartas = cartas

    def __str__(self):
        cartasString = ""
        for carta in self.cartas:
            cartasString += carta.__str__() + " "
        return cartasString
    
    def printaCartasEOpcoes(self):
        print(self.__str__() + "[truco]")
        mensagemOpcoes = ""
        opcoes = []
        for i in range (1, len(self.cartas)+1):
            opcao = i
            mensagemOpcoes += f" {opcao}   "
            opcoes.append(opcao)
        opcao = 4
        mensagemOpcoes += f"   {opcao}"
        opcoes.append(opcao)
        print(mensagemOpcoes)
        return opcoes

    def removeDaMao(self, posicaoCarta):
        return self.cartas.pop(posicaoCarta)


class Jogador:
    def __init__(self, nome, mao):
        self.nome = nome
        self.mao = mao

    def __str__(self):
        return f"{self.nome}: " + self.mao.__str__() + "\n"


class Dupla:
    def __init__(self, jogadores, pontos):
        self.jogadores = jogadores
        self.pontos = pontos

    def __str__(self):
        duplaString = ""
        for jogador in self.jogadores:
            duplaString += jogador.__str__()
            duplaString += "pontos: " + str(self.pontos) + "\n"
        return duplaString




### Inicia programa
naipes = []
naipes.append(Naipe("copas",   "\U00002665"))
naipes.append(Naipe("ouros",   "\U00002666"))
naipes.append(Naipe("espadas", "\U00002660"))
naipes.append(Naipe("paus",    "\U00002663"))

baralho = Baralho(naipes)
baralho.criaBaralho()

jogadores = [
    Jogador("gore", baralho.sorteaUmaMao()),
    Jogador("luan", baralho.sorteaUmaMao()),
    Jogador("joao", baralho.sorteaUmaMao()),
    Jogador("bern", baralho.sorteaUmaMao()),
]

dupla1 = Dupla([jogadores[0], jogadores[2]], 0)
dupla2 = Dupla([jogadores[1], jogadores[3]], 0)

filaDeJogadores = []
filaDeJogadores.append(dupla1.jogadores[0])
filaDeJogadores.append(dupla2.jogadores[0])
filaDeJogadores.append(dupla1.jogadores[1])
filaDeJogadores.append(dupla2.jogadores[1])


# loop para cada partida, roda pela ordem dos jogadores
i = 0
rodadas = 1
cartasDaRodada = []
while True:
    jogadorDaVez = filaDeJogadores[i]

    # os.system("clear")
    print(f"rodada {rodadas}\n")

    if len(cartasDaRodada) > 0:
        for carta in cartasDaRodada:
            print(f"{carta["jogador"].nome}: {carta["carta"].__str__()}")

    print("\n" + jogadorDaVez.nome)
    
    opcaoErrada = True # só pra entrar no while. é gambiarra... eu sei
    while opcaoErrada:
        opcaoErrada = False
        opcoes = jogadorDaVez.mao.printaCartasEOpcoes()
        escolha = input("qual carta vai jogar? ").strip()
        if escolha == "": 
            escolha = 0
        else:
            escolha = int(escolha)

        # vericia se a resposta e válida
        if escolha not in opcoes:
            opcaoErrada = True
            print(f"\nops... você tem as seguintes opções: ")
            continue

        if escolha == 4: # truco ladrao
            # regra do truco aqui
            a = 1 # só pq o python reclama se o if estiver vazio
        else: 
            cartaJogada = jogadorDaVez.mao.removeDaMao(escolha-1)
            print(cartaJogada)
            cartasDaRodada.append({
                "jogador": jogadorDaVez,
                "carta": cartaJogada
            })

    i += 1
    if i == 4: # todos já jogaram, rodada acabou
        os.system("clear")
        # cálculos pra definir a dupla vencedora

        # iniciamos com a primeira e vamos comparar com as outras
        cartaMaisForte = cartasDaRodada[0]
        for cadaCarta in cartasDaRodada:
            if cadaCarta["carta"].peso >= cartaMaisForte["carta"].peso:
                cartaMaisForte = cadaCarta

        print("\n\ne quem levou a rodada foi...")
        print(cartaMaisForte["jogador"].nome)
        print(cartaMaisForte["carta"])
        time.sleep(2)

        # resetando os contadores
        cartasDaRodada = []
        rodadas += 1
        i = 0

        # embaralhando e distribuindo as cartas 
        # os.system("clear")
        # print("\n\nembaralhando e distribuindo as cartas...")
        # baralho.criaBaralho()
        # for jogador in filaDeJogadores:
        #     jogador.mao = baralho.sorteaUmaMao()
        # time.sleep(3)
