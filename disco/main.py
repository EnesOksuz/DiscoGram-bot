import discord,instaloader,json,time,os
from datetime import datetime
USER =""  #instagram mail
PASSWORD= "" #instagram password
target ="" #the id of target account. not name surname
loader = instaloader.Instaloader()
loader.login(USER, PASSWORD)
    
def store(list):
    json_object = json.dumps(list)
    f = open("data.json","w+")
    f.write(json_object)
def get_follows(target):
        profile = instaloader.Profile.from_username(loader.context,target)
        get_followers = profile.get_followers()
        get_followees = profile.get_followees()
        followers =[]
        followees =[]
        for follower in get_followers:
            #get_followees() and get_followers() returns a different type of object like <Profile username (0000000)> so This code gets only username
            followers.append(str(follower).split(" ")[1])

        for followee in get_followees:
            followees.append(str(followee).split(" ")[1])

        time = datetime.now()
        time= time.strftime('%Y-%m-%d %H:%M:%S')

        
        result=[]
        result.append(str(time))
        result.append(followers)
        result.append(followees)
        

        return result

def check_follows(list):
    file_size = os.path.getsize('data.json')
    if not file_size > 1:
        return
    f = open('data.json')
    data = json.load(f)
    unfollowers=[]
    new_followers=[]
    unfollowees=[]
    new_followees=[]
    followee_but_not_follower=[]
    follower_but_not_followee=[]

    for x in range(len(data[1])):
        if not data[1][x] in list[1]:
            unfollowers.append(data[1][x])
    for x in range(len(list[1])):
        if not list[1][x] in data[1]:
            new_followers.append(list[1][x])
    for x in range(len(data[2])):
        if not data[2][x] in list[2]:
            unfollowees.append(data[2][x])
    for x in range(len(list[2])):
        if not list[2][x] in data[2]:
            new_followees.append(list[2][x])
    for x in range(len(data[2])):
        if not data[2][x] in data[1]:
            followee_but_not_follower.append(data[2][x])
    for x in range(len(data[1])):
        if not data[1][x] in data[2]:
            follower_but_not_followee.append(data[1][x])
    changes=[]
    changes.append(unfollowers)
    changes.append(new_followers)
    changes.append(unfollowees)
    changes.append(new_followees)
    changes.append(followee_but_not_follower)
    changes.append(follower_but_not_followee)

    return changes
        


def track():
    __get_follows = get_follows(target=target)
    __check_follows =check_follows(__get_follows)
    result =[]

    when = __get_follows[0]
    number_of_followers = len(__get_follows[1])
    number_of_followees = len(__get_follows[2])
    result.append(when)
    result.append(number_of_followers)
    result.append(number_of_followees)
    result.append(__check_follows)
    store(__get_follows)

    
    

    return result

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
__track = track()

while True:
    @client.event
    async def on_ready():
        print(f"we have logged {client.user}")
        channel = client.get_channel() #get channel id.
        
        if len(__track)==3:
            msg=f"Target is : {target} \n checking time is : {__track[0]} \n number of followers : {__track[1]} \n number of followees : {__track[2]} \n nothing has changed since last check"
            await channel.send(msg)
            await channel.send("want to see follower and followees stats ? type $stats")

        else:
            msg = f"Target is : {target} \n checking time is : {__track[0]} \n number of followers : {__track[1]} \n number of followees : {__track[2]} \n"
            msg1 = f"unfollowers{__track[3][0]} \n newfollowers{__track[3][1]} \n unfollowees{__track[3][2]} \n newfollowees{__track[3][3]} \n"
            await channel.send(msg)
            await channel.send(msg1)
            await channel.send("want to see follower and followees stats ? type $stats")

            
    



    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith("$stats"):
            msg2 =f"he or she follows but not followed by it{__track[3][4]}\n he or she followed by but not follow {__track[3][5]} "
            await message.channel.send(msg2)

    token = "" #needed to get bot token from discord
    client.run(token)
    time.sleep(360)
    
    





