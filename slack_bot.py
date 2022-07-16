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
        self.Id_Of_Channels = {}
        self.channels = channel
        self.slack_token = self.get_token()
        self.headers['Authorization'] = f"Bearer {self.slack_token}"
        if self.isExistChannel(self.channels) == 0 :
            return

        print("[+] Success : Find Channels")        


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

if __name__ == "__main__" :
    # Example : Constructor(Slack Channel)
    # if occured not_in_channel, you invite bot app in channel like @botname
    pass
