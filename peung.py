#!/usr/bin/env python

import random, copy
from pynput.mouse import Button, Listener
from time import sleep
from playsound import playsound


MAX_SOUND_FILE = 30 # maximum score for which a recording exists
QLUMB_MODE = False # toggle qlumbers
SPECIAL_PLAYERS = ["heddood", "yusuf", "yussra", "mama", "baba"]
OUTCOME_MAPPING = {Button.left:0, Button.right:1, Button.middle:-1}

class Game:

  def __init__(self,player0,player1):
    self.score=[0,0]
    self.server = random.choice([0,1])
    self.serve_counter=0
    self.deuce = False
    self.player = [player0,player1]

  def report(self):
    for i in range(2):
      print self.player[i]+": "+str(self.score[i])
    print self.player[self.server]+"'s serve."

    if max(self.score) <= MAX_SOUND_FILE:
      num_prefix = "num" if not QLUMB_MODE else "qlum"
      playsound(num_prefix+"_"+str(self.score[0])+".mp3")
      sleep(0.35)
      playsound(num_prefix+"_"+str(self.score[1])+".mp3")
    sleep(0.65)
    if self.player[self.server] in SPECIAL_PLAYERS:
      playsound("serve_"+str(self.player[self.server])+".mp3")
    else:
      playsound("serve_"+str(self.server)+".mp3")

  def next(self):
    set_outcome()
    if outcome == -1:
      self.undo()
    else:
      self.previous = copy.deepcopy(self)
      self.score[outcome]+=1
      if self.score[0]==10 and self.score[1]==10:
        self.deuce = True
        playsound("deuce.mp3")
      if self.serve_counter == 1 or self.deuce:
        self.server = 1 if self.server == 0 else 0
        self.serve_counter = 0
      else:
        self.serve_counter+=1
  
  def undo(self):
    if "previous" not in self.__dict__.keys():
      playsound("you_peuped.mp3")
    else:
      playsound("you_peuped.mp3")
      playsound("peuped.mp3")
      self.__dict__ = self.previous.__dict__

    
def on_click(x,y,button,pressed):
  if button in [Button.left, Button.right, Button.middle]:
    global quit_sig, outcome
    outcome = OUTCOME_MAPPING[button]
    quit_sig = True

def set_outcome():
  global quit_sig
  quit_sig = False
  listener = Listener(on_click=on_click)
  listener.start()
  while not quit_sig:
    sleep(0.1)
  listener.stop()


print "Enter a player name."
player0 = raw_input()
print "Enter a player name."
player1 = raw_input()

game = Game(player0,player1)


while abs(game.score[0]-game.score[1])<2 or max([game.score[0],game.score[1]]) < 11:
  game.report()
  print "Left click if "+game.player[0]+" scores and right click if "+game.player[1]+" scores. Middle click to undo."
  print ""
  game.next()


game.report()


winner = 0 if game.score[0] > game.score[1] else 1
if game.player[winner] in SPECIAL_PLAYERS:
  playsound("win_"+str(player[winner])+".mp3")
else:
  playsound("win_"+str(winner)+".mp3")
playsound("factorio.mp3")
