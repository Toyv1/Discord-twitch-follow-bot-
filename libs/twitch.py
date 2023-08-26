import httpx, json, time, threading, random


class Tools:

    def user_id(self, user):
        headers = {'Connection': 'keep-alive','Pragma': 'no-cache','Cache-Control': 'no-cache','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"','Accept-Language': 'en-US','sec-ch-ua-mobile': '?0','Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36','Content-Type': 'text/plain;charset=UTF-8','Client-Session-Id': '51789c1a5bf92c65','Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko','X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr','sec-ch-ua-platform': '"Windows"','Accept': '*/*','Origin': 'https://www.twitch.tv','Sec-Fetch-Site': 'same-site','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://www.twitch.tv/',}
        data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
        try:
            response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
            return response.json()[0]['data']['user']['id']
        except:
            return False



class Follow:

    def __init__(self,):
        self.followed_tokens = {}

    def send_follow(self, target_id, follow_count, tokens_data):

        class Threads():
                tha = 0
        
        def follow(i):
            Threads.tha = Threads.tha + 1
            try:
                data = None

                for i in range(len(tokens_data)):
                    
                    data = json.loads(random.choice(tokens_data))
                    token = data['access']

                    if not token in self.followed_tokens:
                        break
                    elif not target_id in self.followed_tokens[token]:
                        break
                    else:
                        data = None

                if data == None:
                    return
                

                Authorization = data['access']
                Integrity = data['integrity']['token']
                proxy = "http://" + data['integrity']['proxy']
                X_Device_Id = data['integrity']['data']['X-Device-ID']
                Client_Id = data['integrity']['data']['Client-ID']
                User_Agent = data['integrity']['data']['User-Agent']


                payload = '[{"operationName":"FollowButton_FollowUser","variables":{"input":{"disableNotifications":false,"targetID":"'+str(target_id)+'"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"800e7346bdf7e5278a3c1d3f21b2b56e2639928f86815677a7126b093b2fdd08"}}}]'
                headers = {
                    
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Authorization': 'OAuth '+Authorization,
                    'Client-Id': Client_Id,
                    'Client-Integrity': Integrity,
                    'User-Agent': User_Agent,
                    'X-Device-Id': X_Device_Id,


                    }
                res = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers,proxies=proxy,timeout=40)
                
                if not Authorization in self.followed_tokens:
                    self.followed_tokens[Authorization] = []
                self.followed_tokens[Authorization].append(target_id)
                

                print(res.text)
            except:
                pass

            Threads.tha = Threads.tha - 1

        def start():
            for i in range(follow_count):
                while True:
                    time.sleep(0.01)
                    if Threads.tha < 20:
                        threading.Thread(
                            target=follow, args=(i,)).start()
                        break
                    else:
                        time.sleep(1)

        threading.Thread(target=start).start()









