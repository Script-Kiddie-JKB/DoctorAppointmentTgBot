import requests
import datetime 
import json
from scheduler import book_timeslot
import re 
#create a python file called api_key 
#that contains a dictionary api={"api_key":"your_api_key"}
import api_key
api_key=api_key.api['api_key']



def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        print("Valid Email") 
        return True
    else:  
        print("Invalid Email")  
        return False

def getLastMessage():
    url = "https://api.telegram.org/bot{}/getUpdates".format(api_key)
    response = requests.get(url)
    data=response.json()
    last_msg=data['result'][len(data['result'])-1]['message']['text']
    chat_id=data['result'][len(data['result'])-1]['message']['chat']['id']
    update_id=data['result'][len(data['result'])-1]['update_id']
    if len(data['result']) < 100:
        return last_msg,chat_id,update_id
    else:
        print('offseting updates limit...')
        url = "https://api.telegram.org/bot{}/getUpdates?offset={}".format(api_key,update_id)
        response = requests.get(url)
        data=response.json()
        last_msg=data['result'][len(data['result'])-1]['message']['text']
        chat_id=data['result'][len(data['result'])-1]['message']['chat']['id']
        update_id=data['result'][len(data['result'])-1]['update_id']
        return last_msg,chat_id,update_id


def sendMessage(chat_id,text_message):
    url='https://api.telegram.org/bot'+str(api_key)+'/sendMessage?text='+str(text_message)+'&chat_id='+str(chat_id)
    response = requests.get(url)
    return response

def sendInlineMessageForService(chat_id):
    text_message='Hi! I am your Booking Appointments Bot!\nI can help you book an appointment.\n\nYou can control me using these commands\n\n/start-to start chatting with the bot\n\nFor more information please contact MultiSpecialityHospital@gmail.com'
    keyboard={'keyboard':[
                        [{'text':'General Physician'},{'text':'Cardiologist'}],
                        [{'text':'Dentist'},{'text':'Dermatologists'}],
                        [{'text':'Gynecologists'},{'text':'Orthopedic Surgeons'}]
                        ]}
    key=json.JSONEncoder().encode(keyboard)
    url='https://api.telegram.org/bot'+str(api_key)+'/sendmessage?chat_id='+str(chat_id)+'&text='+str(text_message)+'&reply_markup='+key
    response = requests.get(url)
    return response

def sendInlineMessageForDoctor(chat_id):
    text_message='Available Doctors\n1.DOC A\n2.DOC B\n3.DOC C\n4.DOC D\n5.DOC E\n6.DOC F'
    keyboard={'keyboard':[
                        [{'text':'Doc A'},{'text':'Doc B'}],
                        [{'text':'Doc C'},{'text':'Doc D'}],
                        [{'text':'Doc E'},{'text':'Doc F'}]
                        ]}
    key=json.JSONEncoder().encode(keyboard)
    url='https://api.telegram.org/bot'+str(api_key)+'/sendmessage?chat_id='+str(chat_id)+'&text='+str(text_message)+'&reply_markup='+key
    response = requests.get(url)
    return response    

def sendInlineMessageForBookingTime(chat_id):
    text_message='Please choose a time slot...'
   # text_message1='Available Doctors\n1.DOC A\n2.DOC B\n3.DOC C\n4.DOC D\n5.DOC E\n6.DOC F\n7.DOC G'
    current_time=datetime.datetime.now()
    current_hour=str(current_time)[11:13]
    # ----------- Chunk of if statement to determine which inline keyboard to reply user ----------------
    if int(current_hour) < 8:
        keyboard={'keyboard':[
                            [{'text':'08:00'}],[{'text':'10:00'}],
                            [{'text':'12:00'}],[{'text':'14:00'}],
                            [{'text':'16:00'}],[{'text':'18:00'}],
                            ]}
    elif 8<=int(current_hour)<10:
        keyboard={'keyboard':[
                            [{'text':'10:00'}],
                            [{'text':'12:00'}],[{'text':'14:00'}],
                            [{'text':'16:00'}],[{'text':'18:00'}],
                            ]}
    elif 10<=int(current_hour)<12:
        keyboard={'keyboard':[
                            [{'text':'12:00'}],[{'text':'14:00'}],
                            [{'text':'16:00'}],[{'text':'18:00'}],
                            ]}
    elif 12<=int(current_hour)<14:
        keyboard={'keyboard':[
                            [{'text':'14:00'}],
                            [{'text':'16:00'}],[{'text':'18:00'}],
                            ]}
    elif 14<=int(current_hour)<16:
        keyboard={'keyboard':[
                            [{'text':'16:00'}],[{'text':'18:00'}],
                            ]}
    elif 16<=int(current_hour)<18:
        keyboard={'keyboard':[
                            [{'text':'18:00'}],
                            ]}
    elif 18<=int(current_hour)<24:
        keyboard={'keyboard':[
                            [{'text':'20:00'}],
                            ]}                       
    else:
        return sendMessage(chat_id,'Please try again tomorrow')
    #----------------------------------------------------------------------------------------------------
    key=json.JSONEncoder().encode(keyboard)
    url='https://api.telegram.org/bot'+str(api_key)+'/sendmessage?chat_id='+str(chat_id)+'&text='+str(text_message)+'&reply_markup='+key
   # url1='https://api.telegram.org/bot'+str(api_key)+'/sendmessage?chat_id='+str(chat_id)+'&text='+str(text_message1)+'&reply_markup='+key
    response = requests.get(url)
  #  response = requests.get(url1)
    return response


def run():
    update_id_for_booking_of_time_slot=''
    doc_name_update=''
    prev_last_msg,chat_id,prev_update_id=getLastMessage()
    while True:
        current_last_msg,chat_id,current_update_id=getLastMessage()
        if prev_last_msg==current_last_msg and current_update_id==prev_update_id:
            print('continue')
            continue
        else:
            if current_last_msg=='/start':
                sendInlineMessageForService(chat_id)   
            if current_last_msg in ['General Physician','Cardiologist','Dentist','Dermatologists','Gynecologists','Orthopedic Surgeons']:
                event_description=current_last_msg
                sendInlineMessageForBookingTime(chat_id)
            if current_last_msg in ['08:00','10:00','12:00','14:00','16:00','18:00','20:00']:
                booking_time=current_last_msg
                update_id_for_booking_of_time_slot=current_update_id
                sendInlineMessageForDoctor(chat_id)
            if current_last_msg in ['Doc A','Doc B','Doc C','Doc D','Doc E','Doc F']:
                doc_name = current_last_msg
                doc_name_update = current_update_id
                sendMessage(chat_id,"Please enter email address:")
            if current_last_msg=='/cancel':
               doc_name_update=''
                # return
               continue
            if doc_name_update!=current_update_id and doc_name_update!= '':
                if check_email(current_last_msg)==True:
                    update_id_for_booking_of_time_slot=''
                    doc_name_update=''
                    sendMessage(chat_id,"Booking please wait.....")
                    input_email=current_last_msg
                    response=book_timeslot(event_description,booking_time,input_email,doc_name)
                    if response == True:
                        sendMessage(chat_id,f"Appointment is booked. for {doc_name} of {event_description} Department Take Care..!!\n\nSee you at {booking_time}\n\n/start- To Book New Appointment")
                        continue
                    else:
                        update_id_for_booking_of_time_slot=''
                        doc_name_update=''
                        sendMessage(chat_id,"Please try another timeslot Or  try again tomorrow")
                        continue
                else:
                    sendMessage(chat_id,"Please enter a valid email.\nEnter /cancel to quit chatting with the bot\nThanks!")
          
        prev_last_msg=current_last_msg
        prev_update_id=current_update_id
        
            
if __name__ == "__main__":
    run()
