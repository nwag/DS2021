# -*- coding: utf-8 -*-

# This is a High Low Guess game Alexa Skill.
# The skill serves as a simple sample on how to use the
# persistence attributes and persistence adapter features in the SDK.
import random
import logging
import os
import boto3

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

SKILL_NAME = 'Hukinator'
ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)
sb = CustomSkillBuilder(persistence_adapter=dynamodb_adapter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    # type: (HandlerInput) -> Response

    speech_text = ("Willkommen zum Hukinator, ich versuche deinen Studiengang rauszufinden. "
                    "Studierst du im Lehramt, berufbegeleitend oder auf English? Oder studierst du im Bachelor/Master? ")
    reprompt = ("Willkommen zum Hukinator, ich versuche deinen Studiengang rauszufinden. "
                "Studierst du im Lehramt, berufbegeleitend oder auf English? Oder studierst du im Bachelor/Master? ")

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response



@sb.request_handler(can_handle_func=is_intent_name("Lehramt"))
def lehramt_intent_handler(handler_input):
    """Handler for Lehramt Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Mandala-Kunst und Krankenschein, der muss Student auf Lehramt sein. Du studierst Lehrarmt Gymnasium!"
    reprompt = "Du studierst Lehrarmt Gymnasium!"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("Berufbegleitend"))
def berufbegleitend_intent_handler(handler_input):
    """Handler for Berufbegleitend Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Dann studierst du Sensorsystemtechnik!"
    reprompt = "Du studierst Sensorsystemtechnik!"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("English"))
def english_intent_handler(handler_input):
    """Handler for English Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Interessierst du dich eher für psychologische-technik mix oder nur Technik?"
    reprompt = "Interessierst du dich eher für psychologische oder technische Fächer?"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("PsychoTechnik"))
def psychotechnik_intent_handler(handler_input):
    """Handler for PsychoTechnik Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Dann studierst du Cognitive Systems!"
    reprompt = "Dann studierst du Cognitive Systems!"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("Communication"))
def communication_intent_handler(handler_input):
    """Handler for Communication Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Dann studierst du Communication Technology!"
    reprompt = "Dann studierst du Cognitive Systems!"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("Bachelor"))
def bachelor_intent_handler(handler_input):
    """Handler for BachelorMaster Intent."""
    # type: (HandlerInput) -> Response
    speech_text = ("Interesstierst du dich eher in der Produktion von elektronischen Geräten, "
                    "um die Entwicklung neuer Hard- und Software Systeme, Programmieren oder Psychologie?")
    reprompt = ("Interesstierst du dich eher in der Produktion von elektronischen Geräten, "
                "um die Entwicklung neuer Hard- und Software Systeme oder Programmieren?")

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Master"))
def master_intent_handler(handler_input):
    """Handler for Master Intent."""
    # type: (HandlerInput) -> Response
    speech_text = ("Interesstierst du dich eher in der Produktion von elektronischen Geräten, "
                    "um die Entwicklung neuer Hard- und Software Systeme, Programmieren oder Psychologie?")
    reprompt = ("Interesstierst du dich eher in der Produktion von elektronischen Geräten, "
                "um die Entwicklung neuer Hard- und Software Systeme oder Programmieren?")

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Programmieren"))
def programmieren_intent_handler(handler_input):
    """Handler for Programmieren Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Hast du auch Interesse in Medien?"
    reprompt = "Hast du auch Interesse in Medien?"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("Informationstechnik"))
def informationstechnik_intent_handler(handler_input):
    """Handler for Informationstechnik Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Wer hätte gedacht, dass das Leben als Informationstechniker so Hardware?"
    reprompt = "Du studierst Informationstechnik."

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("Elektrotechnik"))
def elektrotechnik_intent_handler(handler_input):
    """Handler for Elektrotechnik Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Schön und in der Hose mächtig, dann studierst du Elektrotechnik."
    reprompt = "Schön und in der Hose mächtig, dann studierst du Elektrotechnik."

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("Psychologie"))
def psychologie_intent_handler(handler_input):
    """Handler for Psychologie Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Burnout und ohne Energie, Patient und Student der Psychologie."
    reprompt = "Dann studierst du Psychologie!"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response



@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = ("Ich versuche deinen Studiengang rauszufinden. "
                    "Studierst du im Lehramt, berufbegeleitend oder auf English? ")
    reprompt = ("Ich versuche deinen Studiengang rauszufinden. "
                "Studierst du im Lehramt, berufbegeleitend oder auf English? ")

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda input:
        is_intent_name("AMAZON.CancelIntent")(input) or
        is_intent_name("AMAZON.StopIntent")(input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "War schön mit dir zu spielen!"

    handler_input.response_builder.speak(
        speech_text).set_should_end_session(True)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    logger.info(
        "Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
    return handler_input.response_builder.response


def currently_playing(handler_input):
    """Function that acts as can handle for game state."""
    # type: (HandlerInput) -> bool
    is_currently_playing = False
    session_attr = handler_input.attributes_manager.session_attributes

    if ("game_state" in session_attr
            and session_attr['game_state'] == "STARTED"):
        is_currently_playing = True

    return is_currently_playing


@sb.request_handler(can_handle_func=lambda input:
                    is_intent_name("AMAZON.YesIntent")(input))
def yes_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Ist es nicht witzig wenn Medieninformatiker denken Sie wären echte Informatiker? Hauptsache du studierst was mit Medien."
    reprompt = "Medieninformatik."
    
    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
                    is_intent_name("Ja")(input))
def Ja_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Ist es nicht witzig wenn Medieninformatiker denken Sie wären echte Informatiker? Hauptsache du studierst was mit Medien."
    reprompt = "Medieninformatik."
    
    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=lambda input:
                    is_intent_name("Nein")(input))
def nein_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Was sagt ein Informatiker, wenn er auf die Welt kommt? Hello World!"

    handler_input.response_builder.speak(speech_text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
                    is_intent_name("AMAZON.NoIntent")(input))
def no_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Was sagt ein Informatiker, wenn er auf die Welt kommt? Hello World!"

    handler_input.response_builder.speak(speech_text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input:
                    is_intent_name("AMAZON.FallbackIntent")(input) or
                    is_intent_name("AMAZON.YesIntent")(input) or
                    is_intent_name("AMAZON.NoIntent")(input))
def fallback_handler(handler_input):
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes

    if ("game_state" in session_attr and
            session_attr["game_state"]=="STARTED"):
        speech_text = (
            "Der {} skill kann dir damit nicht weiterhelfen  "
            "Ich versuche deinen Studiengang rauszufinden. ".format(SKILL_NAME))
        reprompt = "Antworte mir meine Fragen."
    else:
        speech_text = (
            "Der {} skill kann dir damit nicht weiterhelfen  "
            "Ich versuche deinen Studiengang rauszufinden. ".format(SKILL_NAME))
        reprompt = "Antworte mir meine Fragen."

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=lambda input: True)
def unhandled_intent_handler(handler_input):
    """Handler for all other unhandled requests."""
    # type: (HandlerInput) -> Response
    speech = "Antworte die letzte Frage bitte, damit ich deinen Studiengang erraten kann!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)
    speech = "Sorry, I can't understand that. Please say again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Response logger."""
    # type: (HandlerInput, Response) -> None
    logger.info("Response: {}".format(response))


lambda_handler = sb.lambda_handler()
