import random
import os
import time

class Naipe:
    def __init__(self, nome, simbolo):
        self.nome    = nome
        self.simbolo = simbolo


class Carta:
    def __init__(self, numero, naipe, peso):
        self.numero = numero
        self.naipe  = naipe
        self.peso   = peso

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
            opcao           = i
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
        self.mao  = mao

    def __str__(self):
        return f"{self.nome}: " + self.mao.__str__() + "\n"


class Dupla:
    def __init__(self, jogadores, pontos, rodadas):
        self.jogadores   = jogadores
        self.pontos      = pontos
        self.rodadas     = rodadas
        self.nomeDaDupla = f"{jogadores[0].nome} e {jogadores[1].nome}" 

    def __str__(self):
        duplaString  = "dupla: "   + self.nomeDaDupla  + "\n"
        duplaString += "pontos: "  + str(self.pontos)  + "\n"
        duplaString += "rodadas: " + str(self.rodadas) + "\n"
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

duplas = [
    Dupla([jogadores[0], jogadores[2]], 0, 0),
    Dupla([jogadores[1], jogadores[3]], 0, 0)
]

filaDeJogadores = []
filaDeJogadores.append(duplas[0].jogadores[0])
filaDeJogadores.append(duplas[1].jogadores[0])
filaDeJogadores.append(duplas[0].jogadores[1])
filaDeJogadores.append(duplas[1].jogadores[1])


# loop para cada partida, roda pela ordem dos jogadores
# uma mão só acaba quando todos os jogadores jogarem todas as suas cartas
# uma rodada acaba quando chegamos ao fim da fila de jogadores
# cada mão possui 3 rodadas
i              = 0
cartasDaMao    = [] 
cartasDaRodada = [] 
numeroDaMao    = 1
duplaVencedora = 0

while not duplaVencedora: # loop de mãos
    # loop de rodadas
    numeroDaRodada = 1
    while numeroDaRodada <= 3: 
        os.system("clear")
        print(duplas[0])
        print(duplas[1])
        valorDaRodada = 2 # valor padrão
        jogadorDaVez  = filaDeJogadores[i]

        print(f"mao {numeroDaMao}")
        print(f"rodada {numeroDaRodada}\n")

        if len(cartasDaRodada) > 0:
            for carta in cartasDaRodada:
                print(f"{carta["jogador"].nome}: {carta["carta"].__str__()}")

        print("\n" + jogadorDaVez.nome)
        
        opcaoErrada = True # só pra entrar no while. é gambiarra... eu sei
        while opcaoErrada:
            opcaoErrada = False
            opcoes      = jogadorDaVez.mao.printaCartasEOpcoes()
            escolha     = input("qual carta vai jogar? ").strip()
            if escolha == "": 
                escolha = 0
            else:
                escolha = int(escolha)

            # verifica se a resposta é válida
            if escolha not in opcoes:
                opcaoErrada = True
                print(f"\nops... você tem as seguintes opções: ")
                continue

            if escolha == 4: # truco ladrao
                # regra do truco aqui
                a = 1 # só pq o python reclama se o if estiver vazio
            else: 
                cartaJogada = jogadorDaVez.mao.removeDaMao(escolha-1)
                cartasDaRodada.append({
                    "jogador": jogadorDaVez,
                    "carta":   cartaJogada
                })

        i += 1
        if i == len(filaDeJogadores): # todos já jogaram, rodada acabou
            os.system("clear")
            # cálculos pra definir a dupla vencedora

            # iniciamos com a primeira e vamos comparar com as outras
            cartaMaisForte = cartasDaRodada[0]
            for cadaCarta in cartasDaRodada:
                if cadaCarta["carta"].peso >= cartaMaisForte["carta"].peso:
                    cartaMaisForte = cadaCarta

            vencedorRodada = cartaMaisForte["jogador"]

            # procuro a dupla do jogador vencedor
            for dupla in duplas:
                for jogador in dupla.jogadores:
                    if jogador.nome == vencedorRodada.nome:
                        # incrementando as vitorias na mão
                        dupla.rodadas += 1

            print("\n\ne quem levou a rodada foi...")
            print(cartaMaisForte["jogador"].nome)
            print(cartaMaisForte["carta"])
            time.sleep(1)

            # resetando os contadores
            for cartaJogada in cartasDaRodada:
                cartasDaMao.append(cartaJogada)
            cartasDaRodada  = []
            numeroDaRodada += 1
            i = 0

    # a mão acabou
    os.system("clear")
    numeroDaMao += 1

    # procurando a dupla vencedora
    duplaVencedoraMao = duplas[0] # só pra iniciar
    for dupla in duplas: 
        if dupla.rodadas > duplaVencedoraMao.rodadas:
            duplaVencedoraMao = dupla

    duplaVencedoraMao.pontos += valorDaRodada
    print("dupla vencedora:")
    print(duplaVencedoraMao)

    # resetando contador de rodadas
    for dupla in duplas: 
        dupla.rodadas = 0

    # verificando se alguma dupla já completou 12 pontos e ganhou
    for dupla in duplas:
        if dupla.pontos >= 12:
            duplaVencedora = dupla
    
    if not duplaVencedora:
        # embaralhando e distribuindo as cartas 
        print("\n\nembaralhando e distribuindo as cartas...")
        baralho.criaBaralho()
        for jogador in filaDeJogadores:
            jogador.mao = baralho.sorteaUmaMao()
        time.sleep(3)

os.system("clear")
print("e a dupla vencedora foi...")
time.sleep(1)
print(duplaVencedora.nomeDaDupla)
print(f"com {duplaVencedora.pontos} pontos!")

time.sleep(10)