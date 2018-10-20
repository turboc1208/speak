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
#from gtts import gTTS

class speaknow(hass.Hass):

  def initialize(self):
    self.log("listening for SPEAK_EVENT")
    self.listen_event(self.handle_speak_event,"SPEAK_EVENT")              # listen for a SPEAK_EVENT
    self.player_list=self.args["device"]
    self.play("media_player.office","Initializing Speak")
    self.log("initialization complete")

  def handle_speak_event(self, event_name, data, kwargs):
    self.log("handling speak event {} media_player={} message={}".format(event_name,data["media_player"],data["message"]),"INFO")
    if data["media_player"]=="all":
      for mp in self.player_list:
        self.play(self.player_list[mp],data["message"])
    else:
      self.play(data["media_player"],data["message"])              # Add it to priority list for processing 

  ########################
  #  Send file to omxplayer over local speaker
  ########################
  def play(self,player,mess):
      self.log("About to play {} on {}".format(mess,player))
      self.call_service("media_player/alexa_tts", entity_id=player, message=mess)

