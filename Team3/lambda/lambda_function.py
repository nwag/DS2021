# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

# from ask_sdk.standard import StandardSkillBuilder


from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

#import XML utils
import xmltodict
import dicttoxml

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Willkommen bei SmartChef. Nenne mir bitte drei Zutaten! Wenn du Rezepte einer bestimmten Kategorie suchst, nenne bitte zunächst die Kategorie! "
        reprompt = "Nenne mir bitte drei Zutaten oder eine Rezeptkategorie!"
        

        session_attr= handler_input.attributes_manager.session_attributes
        
        # attr = handler_input.attributes_manager.persistent_attributes
        
        
        xmlRd = XMLReader()
        categories, recipes = xmlRd.readXMLFile()
        session_attr['recipes']= recipes
        session_attr['questionAsked']= 'Welcome'
        
        speak_output = speak_output #+ str(categories[0])
        
        # for i in categories:
            # speak_output = speak_output + str(i)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class FoodCategoryIntentHandler(AbstractRequestHandler):
    """Handler for Category Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FoodCategoryIntent")(handler_input) and handler_input.attributes_manager.session_attributes['questionAsked']=='Welcome'

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # session_attr = handler_input.attributes_manager.session_attributes
        # cat = session_attr["category"]
        selected_category = str(handler_input.request_envelope.request.intent.slots["category"].value)
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['category'] = selected_category
        speak_output = "Du möchtest also {} kochen! Welche Zutaten hast du denn?".format(selected_category)
        reprompt = "Nenne mir bitte drei Zutaten!"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class NotOkIntentHandler(AbstractRequestHandler):
    """Handler for No Intent after IngredientsIntentHandler"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input) and handler_input.attributes_manager.session_attributes['questionAsked']=='Ingredients'

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = "Wenn du eine Rezeptkategorie hinzufügen oder ändern möchtest, nenne bitte eine Kategorie! Wenn du deine Zutaten ändern möchtest, nenne bitte drei neue Zutaten!"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class IngredientsIntentHandler(AbstractRequestHandler):
    """Handler for Ingredients Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            ask_utils.is_intent_name("IngredientsIntent")(handler_input) 
            or (ask_utils.is_intent_name("FoodCategoryIntent")(handler_input) and handler_input.attributes_manager.session_attributes['questionAsked']=='Ingredients')
            )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        
        if ask_utils.is_intent_name("FoodCategoryIntent")(handler_input):
            # saves category if category is added later
            session_attr['category']= str(handler_input.request_envelope.request.intent.slots["category"].value)
        else:
            # saves user ingredients (default)
            selected_ingr_one = str(handler_input.request_envelope.request.intent.slots["ingredient_one"].value)
            selected_ingr_two = str(handler_input.request_envelope.request.intent.slots["ingredient_two"].value)
            selected_ingr_three = str(handler_input.request_envelope.request.intent.slots["ingredient_three"].value)
            
            session_attr['user_ingredients'] = [selected_ingr_one, selected_ingr_two, selected_ingr_three]
        
        session_attr['questionAsked']='Ingredients'
        
        speak_output = "Deine Zutaten sind {},{} und {}!".format(session_attr['user_ingredients'][0], session_attr['user_ingredients'][1], session_attr['user_ingredients'][2])
        # speak_output = "Deine Zutaten sind {}!".format(selected_ingr_one)
        if 'category' not in session_attr:
            speak_output += "Du hast keine Rezeptkategorie genannt! "
        else: 
            session_attr = handler_input.attributes_manager.session_attributes
            speak_output += "Deine Rezeptkategorie ist {}! ".format(session_attr['category'])
        speak_output += "Ist das ok?"
        reprompt = 'Bestätige bitte mit ja oder nein!'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class RecipeProposalIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent after Ingredients Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (
            (ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input) and session_attr['questionAsked']=='Ingredients')
            or (ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input) and session_attr['questionAsked']=='Recipe'))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = ''
        if session_attr['questionAsked']=='Ingredients':
            # When called for the first time -> check category and remove entries which don't have selected category
            if 'category' in session_attr:
                recipes_with_category = {}
                for recipe_k, recipe_v in session_attr['recipes'].items():
                    for r_category in recipe_v['category']:
                        if r_category.lower() == session_attr['category'].lower():
                            recipes_with_category[recipe_k]= recipe_v
                if not recipes_with_category:
                    speak_output += 'Leider habe ich keine Rezepte in deiner gewünschten Kategorie gefunden!'
                else:
                    session_attr['recipes']= recipes_with_category
            
            # matching user Ingredients with recipe Ingredients         
            user_ingredients = session_attr['user_ingredients']
            session_attr['best_recipes']= dict()
            
            session_attr['recipe_ranks'] = dict()
            rank_counter = 0
            for recipe_k, recipe_v in session_attr['recipes'].items():
                for ingr in recipe_v['foods'].values():
                    for user_ingr in user_ingredients:
                        if ingr[0].lower() == user_ingr.lower():
                            rank_counter += 1
                if rank_counter > 0:
                    session_attr['recipe_ranks'][str(recipe_k)] = rank_counter
                    
                    
                    
                    session_attr['best_recipes'][recipe_k]=recipe_v
                rank_counter=0
            
            if not session_attr['best_recipes']:
                speak_output = "Ich konnte leider kein passendes Rezept für dich finden!"
                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        .response)
            
            #sort dict by rank
            {k: v for k, v in sorted(session_attr['recipe_ranks'].items(), key=lambda item: item[1])}
        
        recipe_sugg_name = list(session_attr['recipe_ranks'])[0]
        del session_attr['recipe_ranks'][recipe_sugg_name]
        recipe_sugg = session_attr['best_recipes'].pop(str(recipe_sugg_name))
        session_attr['recipe_sugg']= recipe_sugg
        speak_output += "Wie wäre es mit: {}? ".format(recipe_sugg_name)
        speak_output+= "Dafür bräuchtest du:"
        for ingr in recipe_sugg['foods'].values():
            speak_output += ' {} {}!'.format(ingr[1], ingr[0])
        session_attr['questionAsked']= 'Recipe'
        speak_output+=' Möchtest du das kochen?'
        
        
        # if (len(best_recipes)>=3):
        #     speak_output = "Wie wäre es mit: {}, {}, oder {}? Was davon magst du kochen?'".format(list(best_recipes)[0], list(best_recipes)[1], list(best_recipes)[2])
        #     session_attr['vorschlag_1']= list(best_recipes)[0]
        #     session_attr['vorschlag_2']= list(best_recipes)[1]
        #     session_attr['vorschlag_3']= list(best_recipes)[2]
        #     # speak_output ='drei'
        # elif (len(best_recipes)==2):
        #     speak_output = "Wie wäre es mit: {} oder {}? Was davon magst du kochen?".format(list(best_recipes)[0], list(best_recipes)[1])
        #     session_attr['vorschlag_1']= list(best_recipes)[0]
        #     session_attr['vorschlag_2']= list(best_recipes)[1]
        #     # speak_output ='zwei'
        # elif (len(best_recipes)==1):
        #     speak_output = "Wie wäre es mit: {}? Möchtest du das kochen?".format(list(best_recipes)[0])
        #     session_attr['vorschlag_1']= list(best_recipes)[0]
        #     # speak_output ='eins'
        # else:
        #     speak_output = "Ich konnte leider kein passendes Rezept für dich finden!"
        
        # first_recipe = list(session_attr['recipes'].keys())[0]
        
        reprompt = 'Sag ja oder nein!'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class RecipeFoundIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent after Recipe Proposal Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input) and handler_input.attributes_manager.session_attributes['questionAsked']=='Recipe'
        
    def handle(self, handler_input):
        
        session_attr = handler_input.attributes_manager.session_attributes
        
        #################################
        #set User Preferences
        #################################
        
        #add the current recipe to user Preferences in persistence attributes
        
        # pers_attr = handler_input.attributes_manager.getPersistentAttributes()
        
        # session_attr['userPreferences'] = dict()
        # session_attr['recipe_sugg']
        
        
        #################################
        #################################
        
        
        session_attr['questionAsked']= 'Instructions'
        speak_output = "Ok! Viel Spaß beim kochen! Brauchst du beim kochen unterstützung?"
        reprompt = "Antworte mir bitte mit ja, oder nein,"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )
    
class InstructionsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            (ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input) and handler_input.attributes_manager.session_attributes['questionAsked']=='Instructions')
            or (ask_utils.is_intent_name('NextInstructionIntent')(handler_input)
            and handler_input.attributes_manager.session_attributes['questionAsked']=='Instructions_next')
        )

    def handle(self, handler_input):
        
        session_attr = handler_input.attributes_manager.session_attributes
        if session_attr['questionAsked']=='Instructions':
            instr = session_attr['recipe_sugg']['instructions'].split("|||\n")
            instr.reverse()
            session_attr['recipe_instructions']= instr
            session_attr['questionAsked']='Instructions_next'
        
        speak_output = "Schritt {}".format(session_attr['recipe_instructions'].pop())
        
        if not session_attr['recipe_instructions']:
            speak_output += " Fertig! Guten Appetit!"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .response
        )
        else:
            endOfSpeak = speak_output[len(speak_output)-1]
            if (endOfSpeak != ".") or (endOfSpeak != "!"):
                speak_output = speak_output + "."
            speak_output+= ' Wenn du fertig bist, sage bitte weiter.'
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

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
        speak_output = "Goodbye!"

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

        speak_output = "Entschuldige, es ist ein Fehler aufgetreten. Bitte starte Smart Chef noch einmal."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

class XMLReader():
    

    def readXMLFile(self):
        
        #initializing Variables
        recipes = {}
        AllCategories = []
        
        
        #read XML File
        with open('recipes_Default.xml', 'r') as xmlFile:
            xmlList = xmlFile.readlines()
        xmlFile.close()
        xmlString = ""
        for i in range(len(xmlList)):
            xmlString = xmlString + xmlList[i]
        
        #parse XML File to Dict Structure
        myDict = xmltodict.parse(xmlString)
        myDict = myDict["root"]
        
        #Convert it from Ordered Dict to a normal Dict
        
        #Try except Statements are for backwards compability to older versions of recipes_Default
        try:
            subDictCategory = myDict["Category"]
            for i in range(len(list(subDictCategory["item"]))):
                category = subDictCategory["item"][i]["#text"]
                AllCategories.append(category)
            
            myDict.pop("Category")

        except KeyError:
            pass
        
        for i in myDict.keys():
            try:
                subDict = myDict[i]["foods"]    
                catDict = myDict[i]["category"]
                try:

                    instructTxt = myDict[i]["instructions"]["#text"]
                except KeyError:
                    instructTxt = ""
                catList = []
                try:
                    
                    for l in range(len(list(catDict["item"]))):
                        catList.append(catDict["item"][l]["#text"])
                except KeyError:
                    catList.append(catDict["item"]["#text"])
                    
            except KeyError:
                subDict = myDict[i]["foods"]
            
            #items of subDict are the names of the Ingredients
            subDictKeys = list(subDict.keys())[1::]
            k = 0
            foodDict = {}
            for j in subDictKeys:
                food = ""
                amount = ""
                #[0] is Foodname
                #[1] is amount
                try:
                    food = subDict[j]["item"][0]["#text"]
                except KeyError:
                    food = subDict[j]["item"]["#text"]
                try:                    
                    amount = subDict[j]["item"][1]["#text"]
                except KeyError:
                    amount = subDict[j]["item"]["#text"]
                foodDict["food "+ str(k)] = [food, amount]
                k = k+1
            recipes[i]= {"foods": foodDict,
                                "category": catList,
                                "instructions": instructTxt}
                                
        return AllCategories, recipes


sb = SkillBuilder()

# sb = StandardSkillBuilder(table_name="Smart Chef", auto_create_table=True)
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(IngredientsIntentHandler())
sb.add_request_handler(FoodCategoryIntentHandler())
sb.add_request_handler(RecipeProposalIntentHandler())
sb.add_request_handler(NotOkIntentHandler())
sb.add_request_handler(RecipeFoundIntentHandler())
sb.add_request_handler(InstructionsIntentHandler())
# sb.add_request_handler(SelectRecipeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()