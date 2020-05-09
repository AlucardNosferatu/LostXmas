# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action
from rasa_sdk.events import SlotSet


class ActionStateChange(Action):

    def name(self):
        return "action_state_change"

    def run(self, dispatcher, tracker, domain):
        temp = tracker.latest_message.get('text')
        if temp == "/mood_unhappy":
            return [SlotSet('state', 'Normal')]
        elif temp == "/mood_great":
            return [SlotSet('state', 'Topic')]
