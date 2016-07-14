#from django.shortcuts import render

import json, requests, random, re
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import *


PAGE_ACCESS_TOKEN = "EAAXffOTVZAtYBAJo5ghtI5X10bIQgjQKZAgnvAjTgXFHbvisxsPwlQysdZChKvF7vu30MyxV3pccn37PuhPjE6WakRmvKsNeAAMZBycZBjYNeFPTOV9FQIkOko1uIZBn9EXQQMIF3M66MqA5XpWGeflawrx4bd06C0ZBfTZBhaG5EwZDZD"
VERIFY_TOKEN = "tinkerbell"
FACEBOOK_GRAPH = "https://graph.facebook.com/v2.6/me"

handler = Handler()


def get_started():
    post_message_url = "%s/thread_settings?access_token=%s" % (FACEBOOK_GRAPH, PAGE_ACCESS_TOKEN)
    response_msg = json.dumps({
        "setting_type":"call_to_actions",
        "thread_state":"new_thread",
        "call_to_actions":[
            {
                "payload":"GET_STARTED"
            }
        ]
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())

def call_send_api(message_data):
    post_message_url = "%s/messages?access_token=%s" % (FACEBOOK_GRAPH, PAGE_ACCESS_TOKEN)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=message_data)
    pprint(status.json())

def send_message(fb_id, message):
    message_data = json.dumps(
        {"recipient":
             {"id": fb_id},
         "message":
             {"text": message}
        })
    call_send_api(message_data)

def send_image(fb_id, image_url):
    message_data = json.dumps(
        {"recipient":
             {"id": fb_id},
         "message":
             {"attachment":
                  {"type":"image",
                   "payload":
                       {"url":image_url}
                   }
              }
         }
    )
    call_send_api(message_data)

def send_choice(fb_id, img):
    message_data = json.dumps(
        {"recipient": {"id": fb_id},
         "message":{ "attachment":{"type":"template","payload":{"template_type":"generic",
         "elements":[{
            "title":"Name",
            "image_url":img,
            "subtitle":"description",
            "buttons":[
              {
                "type":"postback",
                "title":"Yes",
                "payload": "USER_PRESSED_YES"
              },
              {
                "type":"postback",
                "title":"No",
                "payload":"USER_PRESSED_NO"
              },
              {
                "type":"postback",
                "title":"Give me more!",
                "payload":"USER_PRESSED_GIVE_ME_MORE"
              }]}]}}}})
    call_send_api(message_data)

def get_profile(UID):
    user_url = "https://graph.facebook.com/v2.6/%s?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=%s" %(UID, PAGE_ACCESS_TOKEN)
    response = requests.get(user_url)
    if response.status_code == 200:
        return response.json()
    else:
        pprint("ERROR getting profile")
        return None

def initialize(UID):
    profile = get_profile(UID)
    result = handler.check_user(UID)
    pprint( result )
    handler.update_user(UID, {'first_name': profile['first_name'], 'last_name':profile['last_name']})
    handler.update_user(UID, {'temp':'nick_name'})
    user = handler.get_user(UID)
    send_message(UID, "Welcome %s! What would you like to be called?" % user.first_name)

def submit_first_pic(UID):
    #submit the first picture to start
    send_message(UID, "Please submit a photo to start your journey!")
    handler.update_user(UID,{'temp':'profile_pic'})

def setting_buttons(fb_id):
    message_data = json.dumps(
        {"recipient": {"id": fb_id},
         "message":{ "attachment":{"type":"template","payload":{
         "template_type":"button",
         "text":"Setting",
         "buttons":[
              {
                "type":"postback",
                "title":"Set Nickname",
                "payload": "USER_SET_NAME"
              },
              {
                "type":"postback",
                "title":"Set Gender Filter",
                "payload":"USER_SET_GENDER"
              },
              {
                "type":"postback",
                "title":"Set Age Filter",
                "payload":"USER_SET_AGE"
              }]
              }}}})
    call_send_api(message_data)

def setting_gender(fb_id):
    message_data = json.dumps(
        {"recipient": {"id": fb_id},
         "message":{ "attachment":{"type":"template","payload":{
         "template_type":"button",
         "text":"Gender Filter",
         "buttons":[
              {
                "type":"postback",
                "title":"MALE",
                "payload": "GENDER_MALE"
              },
              {
                "type":"postback",
                "title":"FEMALE",
                "payload":"GENDER_FEMALE"
              },
              {
                "type":"postback",
                "title":"BOTH",
                "payload":"GENDER_BOTH"
              }]
              }}}})
    call_send_api(message_data)


def setting_age(fb_id):
    message_data = json.dumps(
        {"recipient": {"id": fb_id},
         "message":{ "attachment":{"type":"template","payload":{
         "template_type":"button",
         "text":"Age Range",
         "buttons":[
              {
                "type":"postback",
                "title":"MAX",
                "payload": "AGE_MAX"
              },
              {
                "type":"postback",
                "title":"MIN",
                "payload":"AGE_MIN"
              }]
              }}}})
    call_send_api(message_data)

def handle_payload(UID, payload):
    pprint("Handling payload..")
    if payload == "USER_PRESSED_YES":
        #handler.update_relation
        send_message(UID, "You said yes!")
    elif payload == "USER_PRESSED_NO":
        send_message(UID, "You said no!" )
    elif payload == "USER_PRESSED_GIVE_ME_MORE":
        send_message(UID, "You said give me more!")
    elif payload == "GET_STARTED":
        initialize(UID)
    elif payload == "USER_SET_NAME":
        send_message(UID,"What would you like to be called?")
        handler.update_user(UID,{'temp':'nick_name'})
    elif payload == "USER_SET_AGE":
        setting_age(UID)
    elif payload == "AGE_MIN":
        send_message(UID,"Please enter a number for the minimum age.")
        handler.update_user(UID,{'temp':'preferred_age_above'})
    elif payload == "AGE_MAX":
        send_message(UID,"Please enter a number for the maximum age.")
        handler.update_user(UID,{'temp':'preferred_age_below'})
    elif payload == "USER_SET_GENDER":
        setting_gender(UID)
    elif payload == "GENDER_FEMALE":
        handler.update_user(UID,{'preferred_gender':0, 'temp':'profile_pic'})
        send_message(UID,"Preferred gender set to female.")
        #if not handler.get_user(UID).flag:
        #    send_message(UID,"Please upload your first picture.")
    elif payload == "GENDER_MALE":
        handler.update_user(UID,{'preferred_gender':1, 'temp':'profile_pic'})
        send_message(UID,"Preferred gender set to male.")
    elif payload == "GENDER_BOTH":
        handler.update_user(UID,{'preferred_gender':2, 'temp':'profile_pic'})
        send_message(UID,"Preferred gender set to both.")



# Create your views here.
class NeverlandView(generic.View):

    #GET request. Only called when it's hooked, by Facebook
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            #get_started()
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    #POST. Called when user is sends a message
    def post(self, request, *args, **kwargs):
        pprint("Message received")
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        pprint("print incoming_message:")
        pprint(incoming_message)

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                UID = message['sender']['id']
                #send_message(UID, "UID: %s" % UID)
                if not handler.is_exists(UID):
                    handle_payload(UID, "GET_STARTED")
                # #else:
                if 'postback' in message:
                    handle_payload(UID, message['postback']['payload'])
                if 'message' in message:
                    msg = message['message']
                    if 'text' in msg:
                        text = msg['text']
                        item = handler.get_user(UID).temp
                        #send_message(UID, "temp: %s" % item)
                       
                        if item != "null":
                            handler.update_user(UID, {item:text})
                            user = handler.get_user(UID)
                            pprint( "Item: %s, text: %s" % ( item, text ) )
                            if not handler.get_user(UID).flag:
                                if item == "nick_name":
                                    handle_payload(UID,"AGE_MIN")
                                    
                                    pprint("Above: %s" % user.preferred_age_above)

                                    #handler.update_user(UID, {'flag': True})
                                elif item == "preferred_age_above":
                                    
            
                                    handle_payload(UID,"AGE_MAX")

                                elif item == "preferred_age_below":
          
                                    handle_payload(UID,"USER_SET_GENDER")

                        if text == "settings":
                            setting_buttons(UID)
                        else:
                            send_message(UID, text)

                    elif 'attachments' in msg:
                        if 'sticker_id' in msg:
                            send_message(UID, "Oh, a sticker!")
                        else:
                            for attachment in message['message']['attachments']:
                                if attachment['type'] == 'image':
                                    img = attachment['payload']['url']
                                    pprint("IMAGE: %s" % img)
                                    item = handler.get_user(UID).temp
                                    if item == "profile_pic":
                                        handler.update_user(UID,{item:img,"flag":True})
                                        user = handler.get_user(UID)
                                        send_choice(UID,user.profile_pic)
                                        #send_message(UID,"Done setting.")
                                    #send_choice(UID, img)
                                    handler.update_user(UID, {"temp":"null"})
        return HttpResponse()

