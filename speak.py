####################
#   speak.py
#   Written by Chip Cox & Rene Tode
#
#   Allow your HA and AD installs to talk to you and your family.
#
#   This was heavily influenced by the work done by Rene Tode on his sound application
#
####################
#
#   you will need to install gtts and omxplayer if not already installed
#
###################
#
#   set your appdaemon.cfg file as follows
#
#   [speak]
#   module=speak
#   class=speak
#
###################
#
#   Save this in your appdaemon appdir with your apps.
#
#   to use this simply fire the "SPEAK_EVENT" with text, priority, and language parameters as follows
#   self.fire_event("SPEAK_EVENT",text=speaktext, priority=pri, language=lang)
#
###################

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
import tempfile
#import subprocess
import os
import pygame
from gtts import gTTS

class speaknow(hass.Hass):

  def initialize(self):
    pygame.init()
    if "device" in self.args:
      self.device=self.args["device"]
    else:
      self.device="local"
    self.log("using device {} for my voice".format(self.device))
    self.filelist = {"1":["empty"],"2":["empty"],"3":["empty"],"4":["empty"],"5":["empty"]}
    self.log("listening for SPEAK_EVENT")
    self.listen_event(self.handle_speak_event,"SPEAK_EVENT")              # listen for a SPEAK_EVENT
    self.play("media_player.office","Initializing Speak")
    self.log("initialization complete")

  def handle_speak_event(self, event_name, data, kwargs):
    self.log("handling speak event {} media_player={} message={}".format(event_name,data["media_player"],data["message"]),"INFO")
    self.play(data["media_player"],data["message"])              # Add it to priority list for processing 

  ########################
  #  Send file to omxplayer over local speaker
  ########################
  def play(self,player,mess):
      self.log("About to play {} on {}".format(mess,player))
      self.call_service("media_player/alexa_tts", entity_id=player, message=mess)
#    pygame.mixer.music.load(filename)
#    pygame.mixer.music.play(0)
#    while pygame.mixer.music.get_busy() == True:
#      continue
#    cmd = "thiswontwork/usr/bin/omxplayer --no-osd -o local " + filename 
#    self.log("cmd={}".format(cmd))
#    options="--no-osd -o local"
#    with tempfile.TemporaryFile() as f:
#        result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True, env=dict(os.environ), cwd="/usr/bin")
#        self.log("result={}".format(result))
#        f.seek(0)
#        output = f.read()

  ##### Set unix file permissions
  def setfilemode(self,_in_file,_mode):
    if len(_mode)<9:
      self.log("mode must bein the format of 'rwxrwxrwx'")
    else:
      result=0
      for val in _mode: 
        if val in ("r","w","x"):
          result=(result << 1) | 1
        else:
          result=result << 1
      self.log("Setting file to mode {} binary {}".format(_mode,bin(result)))
      os.chmod(_in_file,result)

