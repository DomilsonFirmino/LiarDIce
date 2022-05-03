import os
import random
from datetime import datetime
import discord #importar discor.py

random.seed(datetime.now())

#Variaveis
#dictionaires
playersIdToName = {}
playersNamesDices = {}
playersRemainDices = {}
playerPlayOrder = {}
qttOfDices =	{"1": 0,"2": 0,"3": 0,"4": 0,"5": 0,"6": 0 }
#dictionaires
#normalVariables
rodadaAtual = 0 #conta as rodadas atuais
apostaAtual = "" #qual a aposta atual
apostaTotal = 0 #valor total da aposta
jogadorAtual = "" #Qual jogador foi ultimo a jogar
contaVez = 1 #De quem é a vez de jogar
gameStarted = 0 #Se o jogo foi iniciado
#normalVariables
#Variaveis

#function
def verificarFormatoAposta(aposta):
  if(len(aposta)<15):
    return 0
  primeiro = aposta[8:11].replace(" ", "")
  ultimo = aposta[-1]
  if (primeiro.isdigit() and int(primeiro)>0 and ultimo.isdigit() and int(ultimo)<7):
    return 1
  return 0

def resetDices(dicesDict):
  for x in dicesDict:
    dicesDict[x] = 0

def ContPlayersDices(playersNamesDices):
  for x in playersNamesDices:
    contDices(playersNamesDices[x])
    
def contDices(diceString):
  dices = diceString.replace(" ","")
  for x in dices:
    qttOfDices[x] += 1
  
def verificarValorAposta(aposta):
  primeiro = aposta[8:11].replace(" ", "")
  ultimo = aposta[-1]
  return int(int(primeiro)*int(ultimo))

def userName(message):
  return str(message.id)

def randomDices(DiceAmoung):
  dices = ""
  numberAmoung=int(DiceAmoung)
  for x in range(numberAmoung):
    diceValue = random.randrange(1,7)
    dices = dices+" "+str(diceValue);
  return dices
  
def playersDicesDistribution(playersDice,DiceAmoung):
  for x in playersDice:
    playersDice[x] = 0
    playersDice[x] = randomDices(DiceAmoung[x])
    
def rodada(playersDice,DiceAmoung):
  global rodadaAtual
  rodadaAtual+=1
  playersDicesDistribution(playersDice,DiceAmoung)
  return rodadaAtual
  
#function

#COMNADOS
#!desafiar
#!aceitar
#!iniciar
#!apostar
#!mentiroso
#!help
#!Como jogar

#iniciar conexao com o discord

client = discord.Client() #Library discord.py


@client.event
async def on_ready(): #Se o bot estiver pronto a ser usado
  print("we have logged in as {0.user}" .format (client))

@client.event
async def on_message(message):
  global playersIdToName
  global rodadaAtual
  global apostaAtual
  global jogadorAtual
  global contaVez
  global gameStarted
  global apostaTotal

  if message.author == client.user: #ignorar bot messages
    return

  if (message.content.startswith("$desafiar")) and gameStarted == 0:
    idPlayer = userName(message.author)
    playersNamesDices[idPlayer] = ""
    playersRemainDices[idPlayer] = 5
    playerPlayOrder[len(playersNamesDices)] = idPlayer
    playersIdToName[idPlayer] = message.author.name
    await message.channel.send("EU TE DESAFIO PARA UM DUELO")

  if (message.content.startswith("$aceitar")) and gameStarted == 0:
    idPlayer = userName(message.author)
    playersNamesDices[idPlayer] = ""
    playersRemainDices[idPlayer] = 5
    playerPlayOrder[len(playersNamesDices)] = idPlayer
    playersIdToName[idPlayer] = message.author.name
    await message.channel.send("EU ACEITO O DUELO")

  if (message.content.startswith("$iniciar")) and gameStarted == 0 and len(playersNamesDices)> 1:
    gameStarted = 1
    etapa = rodada(playersNamesDices,playersRemainDices)
    await message.channel.send("A ORDEM É")
    for x in playerPlayOrder:
      await message.channel.send(f"O {int(x)} - "+f"<@{playerPlayOrder[x]}>")
    for x in playersNamesDices:
      user = await client.fetch_user(x)
      await user.send(f"Os teus dados {playersNamesDices[x]}")
    await message.channel.send(f"RODADA {etapa}")
    
  if (message.content.startswith("$apostar")) and gameStarted == 1:
    if(playerPlayOrder[contaVez] != userName(message.author)):
      await message.channel.send("Não é a tua vez")
      await message.channel.send(f"É a vez do <@{playerPlayOrder[contaVez]}>")
      return 

    if verificarFormatoAposta(message.content) == 0:
      await message.channel.send("Formato da Aposta está errado")
      return

    novaAposta = verificarValorAposta(message.content)
    if  novaAposta <= apostaTotal :
      await message.channel.send("O Valor da Aposta precisa se maior que a aposta anterior")
      return
    
    apostaAtual = message.content
    jogadorAtual = userName(message.author)
    apostaTotal = novaAposta
    
    if (contaVez == len(playersNamesDices)):
      contaVez = 1
    else:
      contaVez += 1
    await message.channel.send(f"<@{message.author.id}>")
    await message.channel.send("Apostou "+f"**{apostaAtual[9:]}**")
    await message.channel.send("Agora é a vez do "+f"<@{playerPlayOrder[contaVez]}>")

  if (message.content.startswith("$mentiroso")) and gameStarted == 1:
    
    if(playerPlayOrder[contaVez] != userName(message.author)):
      await message.channel.send("Não é a tua vez")
      await message.channel.send(f"É a vez do <@{playerPlayOrder[contaVez]}>")
      return 
    
    for x in playersNamesDices:
      await message.channel.send(playersNamesDices[x])
  
    ContPlayersDices(playersNamesDices)
    primeiro = apostaAtual[8:11].replace(" ", "")
    ultimo = apostaAtual[-1]
    if(qttOfDices[(ultimo)] >= int(primeiro)):
      await message.channel.send(f"<@{jogadorAtual}> Não Mentiu")
      currentPlayer = userName(message.author)
      playersRemainDices[currentPlayer] = playersRemainDices[currentPlayer] - 1
      if (playersRemainDices[currentPlayer] == 0):
        playersRemainDices.pop(currentPlayer)
    else:
      await message.channel.send(f"<@{jogadorAtual}> É um Mentiroso")
      playersRemainDices[jogadorAtual] = playersRemainDices[jogadorAtual] - 1
      if (playersRemainDices[jogadorAtual] == 0):
        playersRemainDices.pop(jogadorAtual)

    if(len(playersRemainDices) == 1):
      for x in playersRemainDices:
        await message.channel.send(f"O vencedor é<@{x}>")
      gameStarted = 0
      return
    
    apostaAtual = ""
    apostaTotal = 0 
    resetDices(qttOfDices)
    etapa = rodada(playersNamesDices,playersRemainDices)
    for x in playersNamesDices:
      user = await client.fetch_user(x)
      await user.send(f"Os teus dados {playersNamesDices[x]}")
    await message.channel.send(f"RODADA {etapa}")
  if (message.content.startswith("$help")):
    await message.channel.send("$desafiar")
    await message.channel.send("$aceitar")
    await message.channel.send("$iniciar")
    await message.channel.send("$apostar 3 de 5")
    await message.channel.send("$mentiroso")
    await message.channel.send("$placar")

  if (message.content.startswith("$placar")) :
    for x in playersRemainDices:
      await message.channel.send(f" O @<{x}> tem "+f"{playersRemainDices[x]}")
my_secret = os.environ['chave']
client.run(my_secret)
