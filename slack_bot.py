# Author : Qerogram
import requests, json

class SlackBot() :
    headers = {
            "Content-Type": "application/x-www-form-urlencoded",
    }

    params = {

    }

    Id_Of_Channels = {}

    def __init__(self, channel) :
        self.channels = channel
        self.slack_token = self.get_token()
        self.headers['Authorization'] = f"Bearer {self.slack_token}"
        self.params["token"] = self.slack_token
        if self.isExistChannel(self.channels) == 0 :
            return

        print("[+] Success : Find Channels")        

        # self.getChannelList()

    def get_token(self) :
        return open("token.txt","r").read()
    
    def getChannelList(self) :
        print("\n" + "=" * 30)
        for name, id in self.Id_Of_Channels.items() :
            print(f"  [-] {name} : {id}")
        print("=" * 30 + "\n")

    def isExistChannel(self, channels) :
        URL = "https://slack.com/api/conversations.list"
        res = requests.get(URL, params=self.params, headers=self.headers)

        response = res.json()

        for element in response['channels'] :
            for channel in channels :
                if element['name'] == channel :
                    self.Id_Of_Channels[element['name']] = element['id']

        return len(channels)
    
    def sendMessage(self, Message) :
        isDup = self.isDuplicated(Message)
        if isDup == True : 
            print(f"[System] Duplicated Link : {Message}")
            return
        elif isDup == -1 : 
            print(f"[System] Error : {Message}")
            return

        URL = "https://slack.com/api/chat.postMessage"

        for Channel in self.Id_Of_Channels.values() :
            data = self.params
            data['channel'] = Channel
            data['text'] = Message
            res = requests.post(URL, data=data, headers=self.headers)

            if res.json()['ok'] != False : 
                print(f"[+] Success : Send Message({Message}) to {Channel}")
            else :
                print(f"[+] Fail : Send Message({Message}) to {Channel}")
    
    def isDuplicated(self, Message) :
        URL = "https://slack.com/api/conversations.history"

        for Channel in self.Id_Of_Channels.values() :
            data = self.params
            data['channel'] = Channel
            data['query'] = Message
            res = requests.get(URL, params=data, headers=self.headers)
            
            if res.json()['ok'] == False : 
                return -1 # Error
            
            else :
                for msg in res.json()['messages'] :
                    if f"{Message}" in msg['text'] :
                        return True
                return False

class SubSlackModule() :
    def __init__(self) : 
        pass

    def sendMessage(self, Channel, Message) :
        if Message != None or Message != "" :
            Bot = SlackBot([Channel])
            Bot.sendMessage(Message)


if __name__ == "__main__" :
    # Example : Constructor(Slack Channel)
    # if occured not_in_channel, you invite bot app in channel like @botname
    pass