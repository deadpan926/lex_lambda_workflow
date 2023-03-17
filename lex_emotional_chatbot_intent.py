import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']


def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}


def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        logger.debug('resolvedValue={}'.format(slots[slotName]['value']['resolvedValues']))
        return slots[slotName]['value']['resolvedValues']
    else:
        return None


def build_validation_result(isvalid, violated_slot):
    return {'isValid': isvalid,
            'violatedSlot': violated_slot,
            }


def validate_slots(slots):
    if not slots["LifeStyleOfficework"]:
        return build_validation_result(False, "LifeStyleOfficework")
    elif not slots["LifeStyleMajor"]:
        # print("check Hyper is not valid")
        return build_validation_result(False, "LifeStyleMajor")
    elif not slots["LifeStyleWorkout"]:
        return build_validation_result(False, "LifeStyleWorkout")
    elif not slots["LifeStyleSocial"]:
        return build_validation_result(False, "LifeStyleSocial")
    elif not slots["LifeStyleSubstance"]:
        return build_validation_result(False, "LifeStyleSubstance")
    elif not slots["LifeStyleDiet"]:
        return build_validation_result(False, "LifeStyleDiet")
    elif not slots["LifeStyleAvailability"]:
        return build_validation_result(False, "LifeStyleAvailability")
    elif not slots["LifeStyleAvailabilityhour"]:
        return build_validation_result(False, "LifeStyleAvailabilityhour")
    return {"isValid": True}


def elicit_slot(slotToElicit, intent_name, slots):
    response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": slotToElicit,
                "type": "ElicitSlot"
            },
            "intent": {
                "name": intent_name,
                "slots": slots
            }
        }
    }
    return response


def delegate(intent_name, slots):
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"
            },
            "intent": {
                "name": intent_name,
                "slots": slots
            }
        }
    }
    return response


def elicit_intent(intent_name, slots, messages):
    response = {"sessionState": {
        "dialogAction": {
            # "slotElicitationStyle":"",
            "type": "ElicitIntent"
            # "type": "Close"
        },
        "intent": {
            "name": intent_name,
            "slots": slots,
            "state": "Fulfilled"
        }
    },
        "messages": [{
            "contentType": "PlainText",
            "content": messages
        }]
    }
    return response


def phyc_survey_lifestyle(intent_request):
    slots = get_slots(intent_request)
    validation_result = validate_slots(slots)
    intent_name = intent_request["sessionState"]["intent"]["name"]
    # print("hooktype", intent_request["invocationSource"])
    if intent_request["invocationSource"] == "DialogCodeHook":
        # print("validation_result:", validation_result)
        if not validation_result["isValid"]:
            return elicit_slot(validation_result["violatedSlot"], intent_name, slots)
        else:
            # print("isValid is True")
            response = delegate(intent_name, slots)
            # print("delegate response", response)
            return response
            # return elicit_intent(intent_name,slots,messages)
    if intent_request["invocationSource"] == "FulfillmentCodeHook":
        messages = "You have answered all the lifestyle questions!"
        print("here is the result")
        return elicit_intent(intent_name, slots, messages)


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot
    """
    intent_name = intent_request["sessionState"]["intent"]["name"]
    response = None
    # print(json.dumps(intent_request))
    # print("intent_name 1", intent_name)
    if intent_name == "PhycSurveyLifestyle":
        # print("intent_name 2")
        response = phyc_survey_lifestyle(intent_request)
    # print("response is", response)
    return response


def lambda_handler(event, context):
    # TODO implement
    response = dispatch(event)
    return response
