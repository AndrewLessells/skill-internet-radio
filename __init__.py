# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

import time
import requests
import random
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
try:
    from mycroft.skills.audioservice import AudioService
except:
    from mycroft.util import play_mp3
    AudioService = None

__author__ = 'nmoore'


LOGGER = getLogger(__name__)


class RNZRadioSkill(MycroftSkill):
    def __init__(self):
        super(InternetRadioSkill, self).__init__(name="InternetRadioSkill")
        self.audioservice = None
        self.process = None

    def initialize(self):
        intent = IntentBuilder("InternetRadioIntent").require(
             "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_intent)

        intent = IntentBuilder("HarkIntent").require(
             "HarkKeyword").require("RadioSearch").build()
        self.register_intent(intent, self.handle_hark_intent)

        intent = IntentBuilder("RNZNationalIntent").require(
            "InternetRadioKeyword").require(
            "RNZNationalKeyword").build()
        self.register_intent(intent, self.handle_rnznational_intent)

        intent = IntentBuilder("RNZConcertIntent").require(
            "InternetRadioKeyword").require(
            "RNZConcertKeyword").build()
        self.register_intent(intent, self.handle_rnzconcert_intent)

        if AudioService:
            self.audioservice = AudioService(self.emitter)

    def handle_rnznational_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play('http://radionz-ice.streamguys.com/national.mp3')
        else:  # othervice use normal mp3 playback
            self.process = play_mp3('http://radionz-ice.streamguys.com/national.mp3')

    def handle_rnzconcert_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play('http://radionz-ice.streamguys.com/concert.mp3')
        else:  # othervice use normal mp3 playback
            self.process = play_mp3('http://radionz-ice.streamguys.com/concert.mp3')

    def handle_stop(self, message):
        self.stop()
        self.speak_dialog('internet.radio.stop')

    def stop(self):
        if self.audioservice:
           self.audioservice.stop()
        else:
            if self.process and self.process.poll() is None:
               self.process.terminate()
               self.process.wait()

def create_skill():
    return RNZRadioSkill()
