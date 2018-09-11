import appdaemon.plugins.hass.hassapi as hass
#import appdaemon.appapi as appapi
            
class talk(hass.Hass):
    #appapi.AppDaemon):

  def initialize(self):
    self.log("about to fire SPEAK event")
    self.run_in(self.say_something,2)

  def say_something(self, kwargs):
    priority="1"
    lang = "en"
    #speaktext= "ahlexa, Turn on den fan light"
    speaktext="I am alive   !!!"
    media_player="media_player.office"
    self.fire_event("SPEAK_EVENT",message=speaktext, media_player=media_player)
