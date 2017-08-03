#!/usr/bin/env python

import random, copy
from pynput.mouse import Button, Listener
from time import sleep
from playsound import playsound


MAX_SOUND_FILE = 30 # maximum score for which a recording exists
QLUMB_MODE = False # toggle qlumbers
SPECIAL_PLAYERS = ["heddood", "yusuf", "yussra", "mama", "baba"]
OUTCOME_MAPPING = {Button.left:0, Button.right:1, Button.middle:-1}
GAME_LENGTH = 11 # number of rallies in a game


def say_num(num):
  num_prefix = "num" if not QLUMB_MODE else "qlum"
  playsound(num_prefix+"_"+str(num)+".mp3")


class Game:

  def __init__(self,player):
    self.score=[0,0]
    self.server = random.choice([0,1])
    self.serve_counter=0
    self.deuce = False
    self.player = player

  def report(self):
    for i in range(2):
      print self.player[i]+": "+str(self.score[i])
    print self.player[self.server]+"'s serve."

    if sum(self.score)==0:
      playsound("game_score.mp3")

    if max(self.score) <= MAX_SOUND_FILE:
      num_prefix = "num" if not QLUMB_MODE else "qlum"
      say_num(self.score[0])
      sleep(0.2)
      say_num(self.score[1])
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
      if self.score[0]==GAME_LENGTH-1 and self.score[1]==GAME_LENGTH-1:
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

  def play(self):
    while abs(self.score[0]-self.score[1])<2 or max([self.score[0],self.score[1]]) < GAME_LENGTH:
      self.report()
      print "Left click if "+self.player[0]+" scores and right click if "+self.player[1]+" scores. Middle click to undo."
      print ""
      self.next()
    
    winner = 0 if self.score[0] > self.score[1] else 1
    if self.player[winner] in SPECIAL_PLAYERS:
      playsound("win_"+str(player[winner])+".mp3")
    else:
      playsound("win_"+str(winner)+".mp3")
    playsound("factorio.mp3")
    return winner

    
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

print "How many games in this match?"
num_games = int(raw_input())
if num_games%2==0: num_games+=1
player=[]
print "Enter player 0 name."
player.append(raw_input())
print "Enter player 1 name."
player.append(raw_input())

match_score = [0,0]

while max(match_score) <= num_games/2:
  game = Game(player)
  playsound("match_score.mp3")
  say_num(match_score[0])
  sleep(0.2)
  say_num(match_score[1])
  sleep(0.65)
  match_score[game.play()] += 1

match_winner = 0 if match_score[0] > match_score[1] else 1
if player[match_winner] in SPECIAL_PLAYERS:
  playsound("win_"+str(player[match_winner])+".mp3")
else:
  playsound("win_"+str(match_winner)+".mp3")
sleep(0.5)
playsound("the_match.mp3")
playsound("match_factorio.mp3")
