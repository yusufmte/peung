import random, copy, pygame
from pynput import mouse
from time import sleep
from pathlib import Path
from platformdirs import user_data_dir
from gtts import gTTS

QLUMB_MODE = False # toggle qlumbers
GAME_LENGTH = 11 # number of rallies in a game

OUTCOME_MAPPING = {
  mouse.Button.left:0,
  mouse.Button.right:1,
  mouse.Button.middle:-1,
}

sound_assets_dir = Path(user_data_dir("peung")) / "assets"

def play_sound(phrase,skip_if_missing=False):
  filepath = sound_assets_dir/to_filename(phrase)
  if not filepath.exists():
    if skip_if_missing:
      return
    else:
      tts = gTTS(phrase)
      tts.save(str(sound_assets_dir)+"/"+to_filename(phrase))
  pygame.mixer.music.load(filepath)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

def say_num(num):
  num_prefix = "" if not QLUMB_MODE else "q"
  play_sound(num_prefix+str(num))

def to_filename(phrase):
  return phrase.replace(" ", "_")+".mp3"

class Game:

  def __init__(self,player):
    self.score=[0,0]
    self.server = random.choice([0,1])
    self.serve_counter=0
    self.deuce = False
    self.player = player

  def report(self):
    for i in range(2):
      print(self.player[i]+": "+str(self.score[i]))
    print(self.player[self.server]+" serve")

    if sum(self.score)==0:
      play_sound("game score")

    say_num(self.score[0])
    #sleep(0.2)
    say_num(self.score[1])
    #sleep(0.65)
    play_sound(str(self.player[self.server])+" serve")

  def next(self):
    set_outcome()
    if outcome == -1:
      self.undo()
    else:
      self.previous = copy.deepcopy(self)
      self.score[outcome]+=1
      if self.score[0]==GAME_LENGTH-1 and self.score[1]==GAME_LENGTH-1:
        self.deuce = True
        play_sound("deuce")
      if self.serve_counter == 1 or self.deuce:
        self.server = 1 if self.server == 0 else 0
        self.serve_counter = 0
      else:
        self.serve_counter+=1
  
  def undo(self):
    if "previous" not in self.__dict__.keys():
      play_sound("undo")
    else:
      play_sound("undo")
      play_sound("undo chime",True)
      self.__dict__ = self.previous.__dict__

  def play(self):
    while abs(self.score[0]-self.score[1])<2 or max([self.score[0],self.score[1]]) < GAME_LENGTH:
      print("Left click if "+self.player[0]+" scores and right click if "+self.player[1]+" scores. Middle click to undo.\n")
      self.report()
      self.next()
    
    winner = 0 if self.score[0] > self.score[1] else 1
    play_sound(str(self.player[winner])+" win")
    play_sound("victory chime",True)
    return winner

    
def on_click(x,y,button,pressed):
  if button in [mouse.Button.left, mouse.Button.right, mouse.Button.middle]:
    if pressed:
      global outcome
      outcome = OUTCOME_MAPPING[button]
    else:
      return False # stops the listener thread

def set_outcome():
  with mouse.Listener(on_click=on_click) as listener:
    listener.join()

def main():
  pygame.init()
  pygame.mixer.init()

  if not sound_assets_dir.is_dir():
    sound_assets_dir.mkdir(parents=True,mode=0o755)

  print(f"Sound asset directory: {sound_assets_dir}")
  print("How many games in this match?")
  num_games = int(input())
  if num_games%2==0: num_games+=1
  player=[]
  print("Enter player 0 name.")
  player.append(input())
  print("Enter player 1 name.")
  player.append(input())

  match_score = [0,0]

  while max(match_score) <= num_games/2:
    game = Game(player)
    play_sound("match score")
    say_num(match_score[0])
    #sleep(0.2)
    say_num(match_score[1])
    #sleep(0.65)
    match_score[game.play()] += 1

  match_winner = 0 if match_score[0] > match_score[1] else 1
  play_sound(str(player[match_winner])+" win")
  #sleep(0.5)
  play_sound("the match that is")
  play_sound("grand victory chime",True)

if __name__=="__main__":
  main()
