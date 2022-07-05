from decouple import config
import time
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
import os

cluster = MongoClient('mongodb+srv://Tonysmile:iam.123.purple@cluster0.cwi8j.mongodb.net/?retryWrites=true&w=majority')

db = cluster['Bakery']
users = db['User']
orders = db ['Order']

app = Flask(__name__)

@app.route('/', methods=['get', 'post'])

def reply():
    res = MessagingResponse()
    text = request.form.get('Body')
    number = request.form.get('From')
   
    img = 'https://drive.google.com/file/d/1SmydZgK__IVu_wspT27AO9vu8fCIFIPC/view?usp=drivesdk'
    img = img.replace('file/d/', 'uc?export=view&id=').replace('/view?usp=drivesdk','')
  
    user = users.find_one({"number": number})
    if bool(user) == False:
        msg = res.message("Hi, thanks for contacting *Chizzy Cakes😂*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n  1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
        msg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
        users.insert_one({"number": number, "status": "main", "messages": []})
    
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid Response😉")
            return str(res)
        if option ==1:
            msg = res.message(
                    "💁 *Need More Info?*\nYou can contact us through phone or e-mail.\n\n📲 *Phone*: +2349032570130 or +2348058472265 \n📧 *E-mail* : anthonyugwuja.dev@gmail.com")
            msg.media(img)
        elif option == 2:
            res.message("You have entered *ordering mode*😄.")
            users.update_one({"number": number}, {"$set":{"status": "ordering"}})
            msg = res.message(
                    "🍰You can select one of the following cakes to order: \n\n1️⃣ Red Velvet  \n2️⃣ Dark Forest \n3️⃣ Ice Cream Cake"
                    "\n4️⃣ Plum Cake \n5️⃣ Sponge Cake \n6️⃣ Genoise Cake \n7️⃣ Angel Cake \n8️⃣ Carrot Cake \n9️⃣ Fruit Cake  \n0️⃣ Go Back")
            msg.media(img)
        elif option == 3:
            msg = res.message("⏲️We work from *9 a.m. to 5 p.m*. Daily")
          
            msg.media('https://raw.githubusercontent.com/Tony-smile/images-icons/master/images/twittercoverpage.png')
    
        elif option == 4:
            msg =res.message(
                    "🏢We have multiple stores across the city. Our main center is at *4/54, Ogige Market*")
            msg.media(img)
        else:
            res.message("Please enter a valid Response😉")
            return str(res)

    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid Response😉")
            return str(res) 
        if option == 0:
            users.update_one({"number": number}, {"$set":{"status": "main"}})
            msg = res.message("You can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
            msg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
        elif 1<= option <=9:
            cakes = ["Red Velvet Cake", "Dark Forest Cake", "Ice Cream Cake",
                    "Plum Cake", "Sponge Cake", "Genoise Cake", "Angel Cake", "Carrot Cake", "Fruit Cake"]
            selected = cakes[option - 1]
            users.update_one(
                 {"number": number}, {"$set": {"status": "address"}})
            users.update_one(
                 {"number": number}, {"$set": {"item": selected}})
            msg = res.message("Excellent choice✔️")
            msg.media(f"{img}")
            res.message("Please enter your address🏠 to confirm the order")
            res.message(f"And Transfer to the following address 🏦 *xxxxxxxx*\nUse *{number}* as your Payment Summary note")
        else:
            res.message("Please enter a valid response😉")
    elif user["status"] == "address":
        selected = user["item"]
        res.message("Thanks for shopping with us❣️😃")
        res.message(f"Your order for *{selected}* has been received and will be delivered within an hour💯")
        orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now().strftime('%I:%M%p:%A, %d %b %Y.')})
        users.update_one(
             {"number": number}, {"$set": {"status": "ordered"}})
    elif user["status"] == "ordered":
        msg = res.message("Hi, thanks for contacting again😅.\nYou can choose from one of the options below: "
                     "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                     "To get our *address*")
        msg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
        users.update_one(
             {"number": number}, {"$set": {"status": "main"}})
    users.update_one({"number":number}, {"$push": {"messages":{"text" : text, "date": datetime.now().strftime('%I:%M%p:%A, %d %b %Y.')}}})
    return str(res)
if __name__ == '__app__':
   app.run()
    