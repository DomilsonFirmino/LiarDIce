import os
import discord
import random

class Node:
  def __init__(self,data,next=None):
    self.data = data
    self.next = next


class Players:
  def __init__(self,id):
    self.id = id
    self.dicesArray = []
    self.dicesQuant = 5

class LinkedList:
  def __init__(self):
    self.head = None
    self.tail = None

  def addNode(self,data):
    newNode = Node(data)
    if (self.head == None):
      self.head = newNode
      self.head.next = self.head
      self.tail = self.head
      return
    if (self.tail.next == self.head):
      self.tail.next = newNode
      self.tail = newNode
      self.tail.next = self.head
      return
#concluido Sem methodo eliminar e listar so para nós

class Game:

  instances = []
  playersID = {}
  gameStarted = 0
  def __init__(self,lastPlayer = None):
    self.List = LinkedList()
    self.lastPlayer = lastPlayer
    self.bet = "0 de 1"
    self.betValue = 0
    self.gameRound = 0
    self.playerCount = 0
    Game.instances.append(self) 
  def checkLiar(self):
    end = game.List.tail
    current = game.List.head
    numberofFaces = 0
    while(True):
      for y in current.data.dicesArray:
        if y == self.bet2:
          numberofFaces += 1
      if (current.data.id == end.data.id):
        break   
      current = current.next
    if numberofFaces >= self.bet1:
      return 1 #Ele não mentiu
    return 0 #Ele Mentiu

  def checkBet(self,bet):
    if len(bet) < 11:
      return 1
    betArray = bet.split(" ")
    if betArray[1].isdigit()==False or betArray[3].isdigit()==False:
      return 1 # bet format error
    if int(betArray[3]) > 6 or int(betArray[3]) < 0:
      return 2 # invalid dice number
    self.bet1 = int(betArray[1])
    self.bet2 = int(betArray[3])
    total = self.bet1 * self.bet2
    if total <= self.betValue:
      return 3 #bet value lower than preview
    self.bet = bet[5:]
    self.betValue = total
    return self.bet
    
  def addPlayer(self,id):
    Game.playersID[id]=1
    player = Players(id)
    self.List.addNode(player)
    self.playerCount += 1 

  def resetValues(self):
    self.lastPlayer = None
    self.bet = "0 de 1"
    self.betValue = 0
  def playerDices(self):
    #melhor codificar para não repetir na hora de enviar por Player
    end = self.List.tail
    current = self.List.head
    if(self.List.head == None and self.List.tail == None):
      print("lista esta Vazia")
      return
    while(True):
      current.data.dicesArray = []
      for y in range(current.data.dicesQuant):
        current.data.dicesArray.append(random.randrange(1,7))
      if (current.data.id == end.data.id):
        break   
      current = current.next 
  def newRound(self):
    self.gameRound = self.gameRound + 1
    self.playerDices()
    return self.gameRound
  def updatePlayer(self):
    self.lastPlayer = self.currentPlayer
    self.currentPlayer = self.currentPlayer.next
  def StartGame(self):
    self.currentPlayer = self.List.head
    Game.gameStarted = 1
    return self.newRound()
  def ContinueGame(self):
    return self.newRound()
  def deletePlayer(self,id):
    delete = self.List.head
    #se a lista for esvaziada
    if(self.List.head.data.id == self.List.tail.data.id):
      self.List.head = None
      self.List.tail = None
      return
      
    #Se o elemento a ser eliminado for o primeiro  
    if(self.List.head.data.id == id):
      self.List.head = delete.next
      self.List.tail.next = self.List.head
      delete = None
      self.playerCount -= 1
      return

    prev = delete
    end = self.List.tail
    while(True):
      if(delete.data.id == id):
        break
      prev = delete
      delete = delete.next
      if (delete.data.id == end.next.data.id):
        return
    if (delete.data.id == end.data.id):
      prev.next = self.List.tail.next
      end = None
      self.List.tail = prev
      self.playerCount -= 1
      return

    prev.next = delete.next
    delete = None   
    self.playerCount -= 1
    return
 
  def printList(self):
    end = self.List.tail
    current = self.List.head
    if(self.List.head == None and self.List.tail == None):
      print("lista esta Vazia")
      return
    while(True):
      print(f"O Atual é {current.data.id}")
      print(f"o Proximo valor {current.next.data.id}")
      print()
      print()
      if (current.data.id == end.data.id):
        return
      current = current.next

  def printPlayerDicesArray(self):
    end = self.List.tail
    current = self.List.head
    if(self.List.head == None and self.List.tail == None):
      print("lista esta Vazia")
      return
    while(True):
      print(f"O Jogador {current.data.id}")
      print(f"Tem os dados {current.data.dicesArray}")
      print()
      print()
      if (current.data.id == end.data.id):
        return 
      current = current.next

    



client = discord.Client()
@client.event
async def on_ready():
  print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  
  if message.author == client.user:
    return 

  if message.content.startswith("$challenge") or message.content.startswith("$desafiar") and len(Game.instances) == 0:
    if(not message.author.id in Game.playersID):
      global game
      game = Game()
      game.addPlayer(message.author.id)
      await message.channel.send(f"<@{message.author.id}> As challenged You")
      return
    else:
      await message.channel.send(f"<@{message.author.id}> You are in game already")
      return
  
  if message.content.startswith("$accept") or message.content.startswith("$aceitar") and game.gameStarted == 0 and len(Game.instances) > 0:
    if(not message.author.id in Game.playersID):
      game.addPlayer(message.author.id)
      await message.channel.send(f"<@{message.author.id}> As accepted Yours challenge")
      return
    else:
      await message.channel.send(f"<@{message.author.id}> You are in game already")
      return
  
  if message.content.startswith("$start") or message.content.startswith("$começar") and Game.gameStarted == 0 and game.playerCount > 1 and len(Game.instances) > 0:
    await message.channel.send(f"Round {game.StartGame()}")
    #Send dices no player in a private message
    end = game.List.tail
    current = game.List.head
    while(True):
      current.data.dicesArray = []
      for y in range(current.data.dicesQuant):
        current.data.dicesArray.append(random.randrange(1,7))
      user = await client.fetch_user(current.data.id)
      await user.send(f"Your dices are {current.data.dicesArray}")
      if (current.data.id == end.data.id):
        break   
      current = current.next 
    return
  if message.content.startswith("$bet") and Game.gameStarted==1:
    if message.author.id != game.currentPlayer.data.id:
      await message.channel.send(f"Its not your turn <@{message.author.id}>")
      await message.channel.send(f"Its <@{game.currentPlayer.data.id}>Turn")
      return
    gameBet = game.checkBet(message.content)
    if gameBet == 1:
      await message.channel.send(f"Bet Format Error, try something like {game.bet} ")
      return
    if gameBet == 2:
      await message.channel.send(f"Dice Face Value is invalid try between 1 and 6")
      return
    if gameBet == 3:
      await message.channel.send(f"Bet Value must be Higher than {game.bet} ")
      return
    await message.channel.send(f"<@{game.currentPlayer.data.id}> Betted {game.bet}")
    await message.channel.send(f"You turn to bet<@{game.currentPlayer.next.data.id}>")
    game.updatePlayer()
    return

  if message.content.startswith("$liar") and Game.gameStarted==1 and game.lastPlayer != None:
    end = game.List.tail
    current = game.List.head
    while(True):
      await message.channel.send(f"The player <@{current.data.id}> have this dices{current.data.dicesArray}")
      if (current.data.id == end.data.id):
        break   
      current = current.next
    liar = game.checkLiar()
    if(liar == 1):
      await message.channel.send(f"<@{game.lastPlayer.data.id}> **You are a saint**")
      game.currentPlayer.data.dicesQuant -= 1
      #Check if the dice reduction reached 0
      if (game.currentPlayer.data.dicesQuant==0):
        Game.playersID.pop(game.currentPlayer.data.id)
        game.deletePlayer(game.currentPlayer.data.id)
        #If current player = 0 then last player win
        if (len(Game.playersID)==1):
          await message.channel.send(f"YOU WIN <@{game.lastPlayer.data.id}>")
    else:
      await message.channel.send(f"<@{game.lastPlayer.data.id}> You **LIAR**")  
      game.lastPlayer.data.dicesQuant -= 1
      #Check if the dice reduction reached 0
      if (game.lastPlayer.data.dicesQuant==0):
        Game.playersID.pop(game.currentPlayer.data.id)
        game.deletePlayer(game.lastPlayer.data.id)
        #If Last player = 0 then last player win
        if (len(Game.playersID)==1):
          await message.channel.send(f"YOU WIN <@{game.currentPlayer.data.id}>")
          Game.instances = None
          return
    #reset Values
    game.resetValues()
    #start New Round
    await message.channel.send(f"Round {game.ContinueGame()}")
    #Send dices no player in a private message
    end = game.List.tail
    current = game.List.head
    while(True):
      current.data.dicesArray = []
      for y in range(current.data.dicesQuant):
        current.data.dicesArray.append(random.randrange(1,7))
      user = await client.fetch_user(current.data.id)
      await user.send(f"Your dices are {current.data.dicesArray}")
      if (current.data.id == end.data.id):
        break   
      current = current.next 
    return
  if message.content.startswith("$help") or message.content.startswith("$ajuda"):
    await message.channel.send("$ challenge/desafiar")
    await message.channel.send("$ accept/aceitar")
    await message.channel.send("$ start/começar")
    await message.channel.send("$bet")
    await message.channel.send("$liar")
    await message.channel.send("$ how to play/como jogar")
    return
  if message.content.startswith("$score") or message.content.startswith("$placar"):
    end = game.List.tail
    current = game.List.head
    while(True):

      await message.channel.send(f"<@{current.data.id}> have {current.data.dicesQuant}")
      if (current.data.id == end.data.id):
        break   
      current = current.next 
    return
  if message.content.startswith("$how to play") or message.content.startswith("$como jogar"):
    user = await client.fetch_user(message.author.id)
    await user.send(
    """
    **Liar's Dice - how the game work**
      
Liar's Dice is a betting game, consistis in 2 or more player betting the quantity of repetition of a dices face. you can heiter bet or call the preview player as a Liar, reveling how dices to now if it is telling the truth.
You win the round if you call a person liar ou you where called liar but told the truth
If you lied you loose a dice, its keep going until you loose all you dices and only one players remain

**How to use the bot**
      
$challenge for starting the game and wait for more people tu $accept the challenge
$accept is for you to participat in the game, can only be used after $challenge command
$start starts the game with the first Round inicialization

After the start the first player start the game by betting
    
$bet is for you to bet  => $bet 3 de 5 mean 3 dices of face 5

Then the next player must choose: $bet a new value or call the preview player a $liar
If you do a new $bet the next player have the same choice as you $bet/$liar until someone choose $liar
If you choose $liar, the dices of all players are revealed if amoung the dices are more of igual number of dices of the face the preview player said that existed you loose otherwise you win.

The player who lost looses one dices, when they loose all 5 dices it is removed from the game

After this a new round start, from who saided $liar, you play until only one player remain""")
    return                       

my_secret = os.environ['chave']
client.run(my_secret)
