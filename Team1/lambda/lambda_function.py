# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from datetime import datetime
from pytz import timezone
from random import choice

import pollen
import clothing
import calendar_custom
import locate
import forgottenlist
import superanswer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["stageID"] = 1000
        
        output_list = [" Wenn du wissen möchtest wass du alles machen kannst, dann sage einfach Hilfe.", " Wenn du einen Termin hinzufügen möchtest, dann sage Termin hinzufügen.", " Wenn du wissen möchtest welche Termine du heute hast, dann sage zum Beispiel: Termine heute.",
        " Wenn du eine Kleidungsempfehlung für heute haben möchtest, dann frage mich zum Beispiel: Was muss ich heute anziehen?", " Wenn du Elemente deiner Liste gerne vergessener Sachen hinzufügen möchtest, dann kannst du zum Beispiel sagen: Füge Schlüssel meiner Liste hinzu.",
        " Wenn du über den aktuellen Pollenflug informiert werden möchtest, dann frage mich zum Beispiel: Welche Pollen sind gerade in der Luft?", " Wenn du du deine Einstellungen ändern möchtest, sage zum Beispiel: Einstellungen öffnen.",
        " Wenn du deine Liste gerne vergessener Dinge abfragen möchtest. Frage mich zum Beispiel: Was vergesse ich gerne?", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        
        speak_output = "Willkommen zurück bei deiner Packliste.{} Was kann ich für dich tun?".format(choice(output_list))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class FirstLaunchRequestHandler(AbstractRequestHandler):
    """Handler for First Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        pers_attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_not_present = not bool(pers_attr)
        
        return attributes_are_not_present and ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["stageID"] = 1010
        
        
        tz = timezone("Europe/Berlin")
        now = datetime.now(tz=tz)
        now_str = now.strftime("%Y-%m-%d %H:%M")
        
        pers_attr = {"calendar": {},

             "ForgottenList": [],

             "settings": {"frequency": {"forgottenlist": [1, now_str]},  # 1,3, 7
                          "functions": {"pollen": True,
                                        "calendar": True,
                                        "clothing": True,
                                        "forgottenlist": True},
                          "user_info": {"location_cloth": "",   # 10838 Ulm
                                        "location_pol": []}, # 110, 112 BW, Oberschwaben
                          "first_launch": True}
             }
        
        
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()
        
        
        speak_output = """<speak>Willkommen bei deiner Packliste. Dieser Skill kann dir helfen, dass du wichtige Unterlagen für einen Termin oder deine Schlüsselkarte morgens nicht vergisst. 
                        Außerdem kann ich dir helfen morgens eine Jacke auszuwählen und dich über den aktuellen Pollenflug informieren.
                        Das ist das erste Mal, dass du den Skill startest. 
                        Jetzt am Anfang brauche ich ein paar Informationen und Einstellungen von dir, dass alles funktionieren kann. 
                        Als Erstes brauche ich deine Postleitzahl, dass ich dir genaue Informationen über Wetter und Pollenflug geben kann. 
                        Sage dazu einfach: Meine Postleitzahl ist, zum Beispiel, <say-as interpret-as="spell-out">89081</say-as>.</speak>"""

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"
        pers_attr = handler_input.attributes_manager.persistent_attributes
        print("pers_attr", pers_attr)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class SettingsIntentHandler(AbstractRequestHandler):
    """Handler for Settings Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SettingsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        session_attr = handler_input.attributes_manager.session_attributes
        
        speak_output = "Möchtest du deine Einstellungen überarbeiten?"
        session_attr["stageID"] = 1010
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output + " Sage einfach ja oder nein.")
                .response
        )


class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Init session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        pers_attr = handler_input.attributes_manager.persistent_attributes
        attributes_manager = handler_input.attributes_manager

        # Dialog differentiation using the stage ID
        if session_attr["stageID"] == 1000:
            speak_output = "Was möchtest du wissen? Wenn du eine Liste der möglichen Befehle haben möchtest, sage einfach Hilfe."
            
        elif session_attr["stageID"] == 1010:
            speak_output = "Willkommen bei den Einstellungen. Möchtest du über das Wetter informiert werden und entsprechende Kleidungsempfehlungen erhalten?"
            session_attr["stageID"] = 1020

        elif session_attr["stageID"] == 1020:
            pers_attr["settings"]["functions"]["clothing"] = True
            speak_output = "Ok, ich werde dir Kleidungsempfehlungen geben. Möchtest du über den derzeitigen Pollenflug informiert werden?"
            session_attr["stageID"] = 1030

        elif session_attr["stageID"] == 1030:
            pers_attr["settings"]["functions"]["pollen"] = True
            speak_output = "Ok, dann informiere ich dich über den aktuellen Pollenflug. Wie oft soll ich dich an deine Liste gerne vergessener Dinge erinnern? Täglich, dreitägig oder wöchentlich?"
            session_attr["stageID"] = 1000

        else:
            speak_output = "Tut mir leid, das verstehe ich nicht. Versuche es noch einmal."
            session_attr["stageID"] = 1010
        
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class NoIntentHandler(AbstractRequestHandler):
    """Handler for No Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Init session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        pers_attr = handler_input.attributes_manager.persistent_attributes
        attributes_manager = handler_input.attributes_manager

        # Dialog differentiation using the stage ID
        if session_attr["stageID"] == 1000:
            speak_output = "Was möchtest du wissen? Wenn du eine Liste der möglichen Befehle haben möchtest, sage einfach Hilfe."
            
        elif session_attr["stageID"] == 1010:
            speak_output = "Möchtest du etwas anderes wissen oder machen?"
            session_attr["stageID"] = 1000
            
        elif session_attr["stageID"] == 1020:
            pers_attr["settings"]["functions"]["clothing"] = False
            speak_output = "Ok, dann werde ich dir keine Kleidungsempfehlungen geben. Möchtest du über den derzeitigen Pollenflug informiert werden?"
            session_attr["stageID"] = 1030

        elif session_attr["stageID"] == 1030:
            pers_attr["settings"]["functions"]["pollen"] = False
            speak_output = "Ok, dann informiere ich dich nicht über den aktuellen Pollenflug. Wie oft soll ich dich an deine Liste gerne vergessener Dinge erinnern? Täglich, dreitägig oder wöchentlich?"
            session_attr["stageID"] = 1000

        else:
            speak_output = "Tut mir leid, das verstehe ich nicht"
            session_attr["stageID"] = 1010
        
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class ForgottenListFrequencyIntentHandler(AbstractRequestHandler):
    """Handler for ForgottenListFrequency Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ForgottenListFrequencyIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        pers_attr = handler_input.attributes_manager.persistent_attributes
        session_attr = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        tz = timezone("Europe/Berlin")
        now = datetime.now(tz=tz)
        now_str = now.strftime("%Y-%m-%d %H:%M")
        first_launch_flag = pers_attr["settings"]["first_launch"]
        
        if first_launch_flag:
            speak_output = "Alles klar, du bist nun mit der Einrichtung fertig. Um eine Liste aller Befehle zu bekommen sage Hilfe."
            pers_attr["settings"]["first_launch"] = False
        else:
            speak_output = "Ok, deine Einstellungen sind eingerichtet"
            
        ask_output = "Was möchtest du machen? Falls du Hilfe brauchst, sage Hilfe."
        
        if slots["frequency"].value == "täglich":
            pers_attr["settings"]["frequency"]["forgottenlist"] = [1, now_str]
        elif slots["frequency"].value == "dreitägig":
            pers_attr["settings"]["frequency"]["forgottenlist"] = [3, now_str]
        elif slots["frequency"].value == "wöchentlich":
            pers_attr["settings"]["frequency"]["forgottenlist"] = [7, now_str]
        else:
            speak_output = "Da ist etwas schief gelaufen. Versuche es noch einmal. Du kannst täglich, dreitägig oder wöchentlich sagen."
            ask_output = "Da ist etwas schief gelaufen. Versuche es noch einmal. Du kannst täglich, dreitägig oder wöchentlich sagen."

        # session_attr["stageID"] = 1000
        
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(ask_output)
                .response
        )


class LocateIntentHandler(AbstractRequestHandler):
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LocateIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        pers_attr = handler_input.attributes_manager.persistent_attributes
        slots = handler_input.request_envelope.request.intent.slots
        attributes_are_not_present = not bool(pers_attr)
        plz = slots["plz"].value
        
        first_launch_flag = pers_attr["settings"]["first_launch"]
        
        try:
            loc = locate.Locate(plz)
            loc.main_loc_cloth()
            loc.look_up_state()
            # b = loc.result_weatherstation_id
            # c = loc.region_id
            # d = loc.partregion_id
            if first_launch_flag:
                speak_output = "Sehr gut, ich habe die Postleitzahl gespeichert. Nun müssen wir festlegen, welche Funktionen du nutzen möchtest. Wenn du bereit bist, sage ja, wenn nicht sage aus, dann schließt sich der Skill."
                ask_output = "Sehr gut, ich habe die Postleitzahl gespeichert. Nun müssen wir festlegen, welche Funktionen du nutzen möchtest. Wenn du bereit bist, sage ja, wenn nicht sage aus, dann schließt sich der Skill."
                # pers_attr["settings"]["first_launch"] = False
            else:
                speak_output = "Ich habe deine Postleitzal gespeichert."
                ask_output = "Was möchtest du noch machen?"
        except KeyError:
            speak_output = "Da hat etwas nicht funktioniert. Versuche es nochmal."
        
        pers_attr["settings"]["user_info"]["location_cloth"] = loc.result_weatherstation_id
        pers_attr["settings"]["user_info"]["location_pol"] = [loc.region_id, loc.partregion_id]
        
        
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()
        
        # speak_output = "Die nächste Wetterstation ist in {}, mit der id {}. Der Regions Code ist {} und die Teilregion {}. Das bedeuted du bist in {}".format(a, b, c, d, e)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(ask_output)
                .response
        )


class SuperAnswerIntentHandler(AbstractRequestHandler):
    """Handler for SuperAnswer Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SuperAnswerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        pers_attr = handler_input.attributes_manager.persistent_attributes
        
        su_an = superanswer.SuperAnswer(pers_attr)
        su_an.todays_functions()
        su_an.generate_speech_output()
        
        speak_output = su_an.speech_output

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("Möchtest du noch etwas wissen?")
                .response
        )


class ClothingIntentHandler(AbstractRequestHandler):
    """Handler for Clothing Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ClothingIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        pers_attr = handler_input.attributes_manager.persistent_attributes
        
        # weatherst_id = "10838"
        
        try:
            weatherst_id = pers_attr["settings"]["user_info"]["location_cloth"]
            cloth = clothing.Clothing(weatherst_id)
            cloth.main_rec()
            speak_output = cloth.speech_output
            
        except KeyError:
            speak_output = "Da ist wohl etwas schief gelaufen. Bitte speichere deine Postleitzahl nochmal, in dem du sagst: Meine Postleitzahl ist und dann deine Postleitzahl."
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Möchtest du noch etwas machen?")
                .response
        )


class PollenIntentHandler(AbstractRequestHandler):
    """Handler for Pollen Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PollenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        pers_attr = handler_input.attributes_manager.persistent_attributes        
        
        # region_id = 110
        # partregion_id = 112
        
        try:
            region_id = pers_attr["settings"]["user_info"]["location_pol"][0]
            partregion_id = pers_attr["settings"]["user_info"]["location_pol"][1]
            poll = pollen.Pollen(region_id, partregion_id)
            poll.main_all()
            speak_output = poll.speech_output
        except KeyError:
            speak_output = "Das tut mir Leid. Da ist ein Problem aufgetreten. Um dies zu beheben, speichere bitte nochmal deine Postleitzahl ab. Sage dazu einfach MEine Postleitzahl ist: und dann deine Postleitzahl."
        


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Was möchtest du machen?")
                .response
        )


class ForgottenListIntentHandler(AbstractRequestHandler):
    """Handler for ForgottenList Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ForgottenListIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        pers_attr = handler_input.attributes_manager.persistent_attributes
        
        try:
            list_f = pers_attr["ForgottenList"]
        except KeyError:
            list_f = []
        
        forli = forgottenlist.ForgottenList(list_f)
        forli.generate_speech_output_forgotten_list()
        
        speak_output = forli.speech_output

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Möchstest du noch etwas machen?")
                .response
        )


class AddElementIntentHandler(AbstractRequestHandler):
    """Handler for AddElement Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddElementIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        pers_attr = handler_input.attributes_manager.persistent_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        try:
            list_f = pers_attr["ForgottenList"]
        except KeyError:
            list_f = []
        
        slot_list = str(slots["list"].value).lower().split(" ")
        
        try:
            for e in slot_list:
                slot_list.remove("und")
        except ValueError:
            pass
        
        forli = forgottenlist.ForgottenList(list_f)
        
        for e in slot_list:
            forli.add_element(e)
        
        pers_attr["ForgottenList"] = forli.pers_list
        
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()
        
        if len(slot_list) > 1:
            speak_output = "Ich habe die Elemente deiner Liste hinzugefuegt."
        else:
            speak_output = "Ich habe das Element deiner Liste hinzugefuegt."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Möchstest du noch etwas machen?")
                .response
        )


class RemoveElementIntentHandler(AbstractRequestHandler):
    """Handler for ForgottenList Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RemoveElementIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        pers_attr = handler_input.attributes_manager.persistent_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        try:
            list_f = pers_attr["ForgottenList"]
        except KeyError:
            list_f = []
        
        e = str(slots["element"].value).lower()
        
        forli = forgottenlist.ForgottenList(list_f)
        
        try:
            forli.remove_element(e)
            speak_output = "Ich habe das Element erfolgreich aus deiner Liste entfernt."
        except ValueError:
            speak_output = "Ich habe dieses Element nicht in deiner Liste gefunden. Versuche es noch einmal."
            
        
        pers_attr["ForgottenList"] = forli.pers_list
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Möchstest du noch etwas machen?")
                .response
        )


class TodaysEventsIntentHandler(AbstractRequestHandler):
    """Handler for TodaysEvents World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TodaysEventsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        
        pers_attr = handler_input.attributes_manager.persistent_attributes
        
        cal_dict = {}
        try:
            cal_dict = pers_attr["calendar"]
        except KeyError:
            pass
        
        cal = calendar_custom.CalendarCustom(cal_dict)
        cal.look_for_events_today()
        cal.generate_speech_output()
        speak_output = cal.speech_output
        
        pers_attr["calendar"] = cal.pers_dict_calendar
        
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Möchtest du noch etwas wissen?")
                .response
        )

class AddEventIntentHandler(AbstractRequestHandler):
    """Handler for AddEvent Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddEventIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        pers_attr = handler_input.attributes_manager.persistent_attributes
        
        try:
            cal_dict = pers_attr["calendar"]
        except KeyError:
            pers_attr["calendar"] = {}
        
        attributes_manager.persistent_attributes = pers_attr
        attributes_manager.save_persistent_attributes()
        
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["new_event"] = {}
        
        speak_output = "Wie soll der Termin heißen? Sag einfach: Der Termin heißt, zum Beispiel, Essen mit Alexa."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Sage zum Beispiel: Der Termin heißt Essen mit Alexa.")
                .response
        )

class AddEventNameIntentHandler(AbstractRequestHandler):
    """Handler for AddEventName Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddEventNameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        name = str(slots["name"].value).lower()
        
        session_attr["new_event"]["event_name"] = name
        
        speak_output = "Wann soll dein Termin {} sein?".format(name)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Sage zum Beispiel: Nächsten Montag um 14 Uhr")
                .response
        )

class AddEventDateIntentHandler(AbstractRequestHandler):
    """Handler for AddEventDate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddEventDateIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        pers_attr = handler_input.attributes_manager.persistent_attributes
        session_attr = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        tz = timezone("Europe/Berlin")
        now = datetime.now(tz=tz)
        now_str = now.strftime("%Y-%m-%d")
        
        date = str(slots["date"].value)
        time = str(slots["time"].value)
        
        if date == "None":
            date = now_str
        
        event_date = "{} {}".format(date, time)
        
        cal = calendar_custom.CalendarCustom(pers_attr["calendar"])
        
        if cal.check_if_date_is_valid(event_date):
            free_flag = cal.check_if_date_occupied(event_date)
            # print("event_date", event_date)
            
            if free_flag == 0:
                speak_output = "Du hast dort schon einen Termin. Versuche eine andere Zeit."
                ask_ouput = "Sage zum Beispiel: Nächsten Montag um 14 Uhr"
            else:
                speak_output = "Okay, dein Termin ist am {} um {}. Was brauchst du für diesen Termin? Sage beispielsweise: Ich brauche Messer und Gabel.".format(date, time)
                ask_ouput = "Sage einfach: Ich brauche Messer und Gabel."
                session_attr["new_event"]["event_date"] = event_date
        else:
            speak_output = "Das tut mir Leid. Es ist ein Problem mit dem Datum aufgetreten. Versuche es bitte nochmal einmal. Sage aber dieses Mal bitte das volle Datum. Zum Beispiel: Am 01-30-2021 um 14 Uhr."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(ask_ouput)
                .response
        )

class AddEventListIntentHandler(AbstractRequestHandler):
    """Handler for AddEventList Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddEventListIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        pers_attr = handler_input.attributes_manager.persistent_attributes
        session_attr = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        cal = calendar_custom.CalendarCustom(pers_attr["calendar"])
        
        tmp = str(slots["list"].value).lower()
        list_e = tmp.split(" ")
        
        try:
            for e in list_e:
                list_e.remove("und")
        except ValueError:
            pass
        
        event_name = session_attr["new_event"]["event_name"]
        event_date = session_attr["new_event"]["event_date"]
        event_packlist = list_e
        
        try:
            cal.add_event(event_name, event_date, event_packlist)
            str_list_e = ", ".join(list_e)
            
            # speak_output = "Du brauchst für diesen Termin also {}.".format(str_list_e)
            
            speak_output = "Okay, ich habe den Termin deinem Kalender hinzugefügt."
            
            pers_attr["calendar"] = cal.pers_dict_calendar
            
            attributes_manager.persistent_attributes = pers_attr
            attributes_manager.save_persistent_attributes()
            
        except:
            speak_output = "Es gab einen Fehler beim abspeichern des Termins. Versuche es nochmal von vorne."
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Was möchtest du machen?")
                .response
        )


class RemoveEventIntentHandler(AbstractRequestHandler):
    """Handler for RemoveEvent Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RemoveEventIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        attributes_manager = handler_input.attributes_manager
        pers_attr = handler_input.attributes_manager.persistent_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        cal = calendar_custom.CalendarCustom(pers_attr["calendar"])
        
        name = str(slots["name"].value).lower()
        
        try:
            flag = cal.remove_event_name(name)
            
            if flag == 1:
                speak_output = "Der Termin wurde erfolgreich gelöscht."
            else:
                speak_output = "Ich konnte den Termin leider nicht finden. Versuche es noch einmal."
            
            pers_attr["calendar"] = cal.pers_dict_calendar
            
            attributes_manager.persistent_attributes = pers_attr
            attributes_manager.save_persistent_attributes()
            # print(pers_attr)
        except:
            speak_output = "Es gab einen Fehler beim entfernen des Termins. Versuche es nochmal von vorne."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Was möchtest du machen?")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = """<speak>
                            Willkommen bei der Hilfe.
                            
                            Wenn du deine Packliste für heute abrufen möchtest, kannst du mich fragen: Was muss ich heute mitnehmen?
                            
                            Wenn du deine Packliste schnell und direkt haben möchtest, kann ich sie dir direkt ausgeben ohne dass du zuerst den Skill starten musst. 
                            Dies kannst du durch die Aussage machen: Alexa, frage meine Packliste nach heute.
                            
                            Wenn du wissen möchtest, was auf deiner Liste gerne vergessener Dinge steht, kannst du fragen: Was vergesse ich gerne?
                            
                            Wenn du deiner Liste gerne vergessener Dinge etwas hinzufügen möchtest, kannst du sagen: Füge, zum Beispiel, Schlüssel meiner Liste hinzu.
                            
                            Wenn du ein Element aus deiner Liste gerne vergessener Dinge entfernen möchtest. Sage einfach: Entferne Schlüssel aus meiner Liste.
                            
                            Wenn du deine Termine für heute abrufen möchtest, kannst du einfach sagen: Termine heute.
                            
                            Wenn du einen Termin hinzufügen möchtest, kannst du dies tun indem du sagst: Termin hinzufügen.
                            
                            Einen Termin entfernen kannst du, wenn du sagst: Entferne Termin und dann den Namen des Termins. Zum Beispiel: Entferne Termin Essen mit Alexa.
                            
                            Um Kleidungsempfehlungen zu erhalten kannst du mich fragen: Was soll ich heute anziehen?
                            
                            Um Informationen über den aktuellen Pollenflug zu erhalten, kannst du mich fragen: Welche Pollen sind gerade in der Luft?
                            
                            Die Einstellungen kannst du einfach mit der Aussage: Einstellungen öffnen bearbeiten.
                            
                            Um deine Postleitzahl zu ändern kannst du einfach sagen: Meine Postleitzahl ist und dann deine Postleitzahl. Zum Beispiel: Meine Postleitzahl ist <say-as interpret-as="spell-out">89081</say-as>.
                            
                            So, das waren die Befehle, die du zum Bedienen des Skills brauchst. Viel Spaß dabei!
                            </speak>"""

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bis bald!"

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

        speak_output = "Es tut mir Leid. Da ist leider ein Problem aufgetreten. Versuche es bitte noch einmal."

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

sb.add_request_handler(FirstLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(SuperAnswerIntentHandler())
sb.add_request_handler(SettingsIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(ForgottenListFrequencyIntentHandler())
sb.add_request_handler(AddEventIntentHandler())
sb.add_request_handler(AddEventNameIntentHandler())
sb.add_request_handler(AddEventDateIntentHandler())
sb.add_request_handler(AddEventListIntentHandler())
sb.add_request_handler(TodaysEventsIntentHandler())
sb.add_request_handler(RemoveEventIntentHandler())
sb.add_request_handler(LocateIntentHandler())
sb.add_request_handler(ClothingIntentHandler())
sb.add_request_handler(PollenIntentHandler())
sb.add_request_handler(ForgottenListIntentHandler())
sb.add_request_handler(AddElementIntentHandler())
sb.add_request_handler(RemoveElementIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()