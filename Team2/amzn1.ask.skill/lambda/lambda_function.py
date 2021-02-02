# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
#https://www.sqlshack.com/getting-started-with-amazon-s3-and-python/
import logging
import ask_sdk_core.utils as ask_utils
import pandas as pd
from random import *

#persistence
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



# Überprüfung ob game_state = ENDED
def isended(handler_input):
    session_attr = handler_input.attributes_manager.session_attributes
    if session_attr['game_state'] == 'ENDED':
        return True
    else:
        return False

# Überprüfung ob game_state = STARTED
def isstart(handler_input):
    session_attr = handler_input.attributes_manager.session_attributes
    if session_attr['game_state'] == 'STARTED':
        return True
    else:
        return False

# Überprüfung ob game_state = FRAGEN
def isfragen(handler_input):
    session_attr = handler_input.attributes_manager.session_attributes
    if session_attr['game_state'] == 'FRAGEN':
        return True
    else:
        return False


# Erster Intent welcher nach dem Start aufgerufen wird
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Session Attribute holen und setzen
        session_attr = handler_input.attributes_manager.session_attributes

        session_attr['kategorie'] = ""
        session_attr['Fragenanzahl'] = 2
        session_attr['grad'] = ""
        session_attr['game_state'] = 'ENDED'
        session_attr['gestellteFragen'] = 0
        session_attr['korrekteAntworten'] = 0

        #Persistente Attribute erstellen und initialisieren
        attributes_manager = handler_input.attributes_manager

        stat_attributes = {
            "korrekteAntworten": 0,
            "gestellteFragen" : 0,
            "anteilKorrekt": 0,
            "meisteKorrekteAntwortenInFolge" : 0,
            "korrekteAntwortenInFolge" : 0
        }
        
        attributes_manager.persistent_attributes = stat_attributes
        attributes_manager.save_persistent_attributes()
        
        # Output einlesen
        output = pd.read_csv("output.csv", sep = ';')

        # Zufälligen output wählen
        out = output.loc[output.Intent == "LaunchRequestHandler"].sample(n=1).iloc[0].name

        speak_output = (str(output.iloc[out]['Text']))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

#neuer Intent Handler, der schaut, ob bereits ein persistentes Attribut vorhanden ist.
class HasPersistentAttributeLaunchRequestHandler(AbstractRequestHandler):
    """Handler for launch after they have set a persistent attribute"""

    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("korrekteAntworten" in attr)

        return attributes_are_present and ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
         # Session Attribute holen und setzen
        session_attr = handler_input.attributes_manager.session_attributes

        session_attr['kategorie'] = ""
        session_attr['Fragenanzahl'] = 2
        session_attr['grad'] = ""
        session_attr['game_state'] = 'ENDED'
        session_attr['gestellteFragen'] = 0
        session_attr['korrekteAntworten'] = 0

        #attr = handler_input.attributes_manager.persistent_attributes
        #attribute_a = attr['attribute_a']

        # Output einlesen
        output = pd.read_csv("output.csv", sep = ';')

        # Zufälligen output wählen
        out = output.loc[output.Intent == "LaunchRequestHandler"].sample(n=1).iloc[0].name

        speak_output = (str(output.iloc[out]['Text']))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
#ende

# Intent welcher beim Start des Quizzes aufgerufen wird
class StartIntentHandler(AbstractRequestHandler):
    """Handler for Start Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("StartIntent")(handler_input) or ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)) and isended(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Datensatz einlesen
        data = pd.read_csv("database.csv", sep = ';')


        # Zufällig eine Kategorie Auswählen
        kategorien = data.drop_duplicates(subset=['Kategorie'])['Kategorie'].sample(n=1)

        # Kategorie in Session Attribut abspeichern
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['kategorie'] = kategorien.iloc[0]

        # Anzahl der gestellten Fragen wieder auf 0 setzen und gamestate setzen
        session_attr['gestellteFragen'] = 0
        session_attr['game_state'] = 'STARTED'

        #test persistent attributes -------
        #attributes_manager = handler_input.attributes_manager

        #a = 5
        #test_attributes = {
        #    "attribute_a": a
        #}

        #attributes_manager.persistent_attributes = test_attributes
        #attributes_manager.save_persistent_attributes()
        #testende

        # Output einlesen
        output = pd.read_csv("output.csv", sep = ';')

        # Zufälligen output wählen
        out = output.loc[output.Intent == "StartIntentHandler"].sample(n=1).iloc[0].name

        # Ausgabe
        speak_output = (str(output.iloc[out]['Text']) + " " + str(kategorien.iloc[0]) + "! Welchen Schwierigkeitsgrad möchtest du? einfach, mittel oder schwer?")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# Intent welcher bei der beantwortung der Fragen aufgerufen wird und Antworten überprüft
class AnwserIntentIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AnwserIntent")(handler_input) and isfragen(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

         # Datensatz einlesen
        data = pd.read_csv("database.csv", sep = ';')

        # Session Attribute und Usereingabe holen
        input_user = str(handler_input.request_envelope.request.intent.slots["input"].value).upper()[0]
        session_attr = handler_input.attributes_manager.session_attributes
        
        # Einlesen Persistente Attribute
        #stat_attributes = handler_input.attributes_manager.persistent_attributes
        #korrekteAntwortenInFolge = stat_attributes['korrekteAntwortenInFolge']

        # Output einlesen
        output = pd.read_csv("output.csv", sep = ';')

        # Zufälligen outputs wählen
        out1 = output.loc[(output.Intent == "AnwserIntentIntentHandler") & (output.OutputNo == 1)].sample(n=1).iloc[0].name
        out2 = output.loc[(output.Intent == "AnwserIntentIntentHandler") & (output.OutputNo == 2)].sample(n=1).iloc[0].name
        out3 = output.loc[(output.Intent == "AnwserIntentIntentHandler") & (output.OutputNo == 3)].sample(n=1).iloc[0].name
        out4 = output.loc[(output.Intent == "AnwserIntentIntentHandler") & (output.OutputNo == 4)].sample(n=1).iloc[0].name

        # Antwort des Users überprüfen
        if str(data.loc[session_attr['Frage'+ str(session_attr['gestellteFragen']+1)]][input_user]) == str(data.loc[session_attr['Frage'+ str(session_attr['gestellteFragen']+1)]]['Korrekte Antwort']):
            addon = (str(output.iloc[out1]['Text']) + " ")
            #Counter für korrekte Antworten erhöhen
            session_attr['korrekteAntworten'] = session_attr['korrekteAntworten']+1
            #korrekteAntwortenInFolge = korrekteAntwortenInFolge+1
            
        else:
            addon = (str(output.iloc[out2]['Text']) + " " + str(data.loc[session_attr['Frage'+ str(session_attr['gestellteFragen']+1)]]['Korrekte Antwort']))
            #korrekteAntwortenInFolge = 0

        # Counter für gestellteFragen erhöhen!
        session_attr['gestellteFragen'] = session_attr['gestellteFragen']+1
        
         # Überschreiben der persistent attributes
        #attributes_manager = handler_input.attributes_manager
        #stat_attributes = {
        #"korrekteAntwortenInFolge" : korrekteAntwortenInFolge
        #}
        #attributes_manager.persistent_attributes = stat_attributes
        #attributes_manager.save_persistent_attributes()
            

        # Überprüfen ob noch einmal eine Frage kommt oder es die letzte Frage war
        if session_attr['gestellteFragen'] == session_attr['Fragenanzahl']:
            postadd = (str(output.iloc[out3]['Text']))
            session_attr['game_state'] = 'ENDED'

        else:
            postadd = (str(output.iloc[out4]['Text']) + " " + str(session_attr['gestellteFragen']+1) + " von " + str(session_attr['Fragenanzahl']) + ": " + str(data.loc[session_attr['Frage'+str(session_attr['gestellteFragen']+1)]]['Frage']) + " Es gibt folgende Antwortmöglichkeiten: Antwort A: " + str(data.loc[session_attr['Frage'+str(session_attr['gestellteFragen']+1)]]['A']) + " und Antwort B: " + str(data.loc[session_attr['Frage'+str(session_attr['gestellteFragen']+1)]]['B']))

        # Antwort zusammen setzen
        speak_output = (addon + ". " + str(data.loc[session_attr['Frage'+ str(session_attr['gestellteFragen'])]]['Erklaerung']) + " " + postadd)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# Intent welcher den Schwierigkeitsgrad abfragt und Fragen daraus zufällig auswählt
class DiffIntentHandler(AbstractRequestHandler):
    """Handler for Difficult Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DiffIntent")(handler_input) and isstart(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Output einlesen
        output = pd.read_csv("output.csv", sep = ';')

        # Zufälligen output wählen
        out = output.loc[output.Intent == "DiffIntentHandler"].sample(n=1).iloc[0].name

        # Session Attribute und Slot holen
        session_attr = handler_input.attributes_manager.session_attributes
        input_user = str(handler_input.request_envelope.request.intent.slots["diff"].value).lower()

        # Slot in Session Attribute speichern
        session_attr['grad'] = input_user

        # Datensatz einlesen
        data = pd.read_csv("database.csv", sep = ';')

        # gamestate auf fragen setzen
        session_attr['game_state'] = 'FRAGEN'

        # Daten filtern
        mögl_fragen = data.loc[(data.Kategorie == str(session_attr['kategorie'])) & (data.Level == str(session_attr['grad']))]

        # Zufällige Fragen wählen und als Session Attribute abspeichern
        fragen = mögl_fragen.sample(n = session_attr['Fragenanzahl'])
        for i in range(1,session_attr['Fragenanzahl']+1):
            session_attr['Frage' + str(i)] = int(fragen.iloc[i-1].name)

        # Frage stellen
        speak_output = (str(output.iloc[out]['Text']) + " " + str(session_attr['Fragenanzahl']) + ": " + str(data.loc[session_attr['Frage1']]['Frage']) + " Ist es entweder Antwort A: " + str(data.loc[session_attr['Frage1']]['A']) + ", oder Antwort B: " + str(data.loc[session_attr['Frage1']]['B']) + "! Antworte bitte mit \"Es ist A\" oder  \"Es ist B\"!")


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# Intent wenn das Quiz beendet wird
class NoIntentHandler(AbstractRequestHandler):
    """Handler for No Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Einlesen Persistente Attribute
        stat_attributes = handler_input.attributes_manager.persistent_attributes
        
        # Einlesen Session Attribute
        session_attr = handler_input.attributes_manager.session_attributes
        korrekteAntworten = session_attr['korrekteAntworten']
        gestellteFragen = session_attr['gestellteFragen']
        anteilKorrekt = korrekteAntworten / gestellteFragen * 100 #in %
        
        # Überschreiben der persistent attributes_manager
        attributes_manager = handler_input.attributes_manager
        stat_attributes = {
            "korrekteAntworten": korrekteAntworten,
            "gestellteFragen" : gestellteFragen,
            "anteilKorrekt": anteilKorrekt, #in %
            #"meisteKorrekteAntwortenInFolge" : 0
        }
        attributes_manager.persistent_attributes = stat_attributes
        attributes_manager.save_persistent_attributes()

        
        speak_output = ("Ich wünsche dir noch einen schönen Tag und bis zum nächsten mal. Dein Daily Quiz!")

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


# Intent um die Frage nochmal zu wiederholen
class WiederholungIntentHandler(AbstractRequestHandler):
    """Handler for Wiederholung Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("WiederholungIntent")(handler_input) and isfragen(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Session Attributes holen
        session_attr = handler_input.attributes_manager.session_attributes

        # Datensatz einlesen
        data = pd.read_csv("database.csv", sep = ';')

        speak_output = ("Die Frage lautete: " + str(data.loc[session_attr['Frage'+str(session_attr['gestellteFragen']+1)]]['Frage']) + " Ist es entweder Antwort A: " + str(data.loc[session_attr['Frage'+str(session_attr['gestellteFragen']+1)]]['A']) + ", oder Antwort B: " + str(data.loc[session_attr['Frage'+str(session_attr['gestellteFragen']+1)]]['B']))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# Intent welcher die Statistiken anzeigt
class StatIntentHandler(AbstractRequestHandler):
    """Handler for Stat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StatIntent")(handler_input) and isended(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Einlesen Persistente Attribute
        stat_attributes = handler_input.attributes_manager.persistent_attributes
        korrekteAntworten = stat_attributes['korrekteAntworten']
        gestellteFragen = stat_attributes['gestellteFragen']
        anteilKorrekt = stat_attributes['anteilKorrekt']
        
        speak_output = "Hier deine Statistikdetails vom letzten Mal: Von " + str(gestellteFragen) + " gestellten Fragen hast du " + str(korrekteAntworten) + " korrekt beantwortet. Das entspricht einem Anteil von " + str(anteilKorrekt) + "%." 


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


# INtent welcher bei nachfrage Hilfen gibt
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Daily Quiz ist deine eigene Quiz App um dein Wissen tagtäglich zu erweitern. Sage los oder start um mit dem Quiz zu beginnen. Willst du deine Statistiken anschauen, dann sage statistik. Konntest du dir eine Frage nicht merken oder hast Sie vergessen? Dann sage einfach wiederhole die frage. Ich hoffe ich konnte dir weiter helfen!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# Wenn prozedur gecncled oder gestoppt wird
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Ich wünsche dir noch einen schönen Tag und bis zum nächsten mal. Dein Daily Quiz!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Ich weis nicht genau was du meinst, bitte wiederhole deine Antwort."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)


sb.add_request_handler(HasPersistentAttributeLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StatIntentHandler())
sb.add_request_handler(WiederholungIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(AnwserIntentIntentHandler())
sb.add_request_handler(DiffIntentHandler())
sb.add_request_handler(StartIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

