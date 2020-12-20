from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from random import choice
from threading import Thread,Lock,active_count
from string import ascii_letters,ascii_lowercase,ascii_uppercase,digits
from time import sleep
from datetime import datetime
import requests
import json

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title:str):
        if name == 'posix':
            stdout.write(f"\x1b]2;{title}\x07")
        elif name in ('ce', 'nt', 'dos'):
            system(f'title {title}')
        else:
            stdout.write(f"\x1b]2;{title}\x07")

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('useragents.txt','r')
        return choice(useragents)
    
    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        proxies = {}
        if self.proxy_type == 1:
            proxies = {
                "http":"http://{0}".format(choice(proxies_file)),
                "https":"https://{0}".format(choice(proxies_file))
            }
        elif self.proxy_type == 2:
            proxies = {
                "http":"socks4://{0}".format(choice(proxies_file)),
                "https":"socks4://{0}".format(choice(proxies_file))
            }
        else:
            proxies = {
                "http":"socks5://{0}".format(choice(proxies_file)),
                "https":"socks5://{0}".format(choice(proxies_file))
            }
        return proxies

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'One Man Builds Steam Username Checker Tool ^| AVAILABLE: {self.available} ^| TAKEN: {self.taken} ^| RETRIES: {self.retries} ^| WEBHOOK RETRIES: {self.webhook_retries} ^| THREADS: {active_count()-1}')
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        self.clear()
        self.SetTitle('One Man Builds Steam Username Checker Tool')
        self.title = Style.BRIGHT+Fore.RED+"""                                        
                          ╔══════════════════════════════════════════════════════════════════╗
                            ╔═╗╔╦╗╔═╗╔═╗╔╦╗  ╦ ╦╔═╗╔═╗╦═╗╔╗╔╔═╗╔╦╗╔═╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
                            ╚═╗ ║ ║╣ ╠═╣║║║  ║ ║╚═╗║╣ ╠╦╝║║║╠═╣║║║║╣   ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
                            ╚═╝ ╩ ╚═╝╩ ╩╩ ╩  ╚═╝╚═╝╚═╝╩╚═╝╚╝╩ ╩╩ ╩╚═╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═
                          ╚══════════════════════════════════════════════════════════════════╝                                          
                                                                                                                                               
        """
        print(self.title)
        self.available = 0
        self.taken = 0
        self.retries = 0
        self.webhook_retries = 0

        self.lock = Lock()
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        
        if self.use_proxy == 1:
            self.proxy_type = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Https ['+Fore.RED+'2'+Fore.CYAN+']Socks4 ['+Fore.RED+'3'+Fore.CYAN+']Socks5: '))

        self.method = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Brute ['+Fore.RED+'0'+Fore.CYAN+']From Usernames.txt: '))
        
        self.enable_webhook = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Enable Webhook ['+Fore.RED+'0'+Fore.CYAN+']No Webhook: '))
        
        if self.enable_webhook == 1:
            self.webhook_url = str(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Webhook URL: '))
        
        self.threads_num = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        print('')

    def GenName(self,length,include_digits,case,prefix,suffix):
        if case == 1:
            if include_digits == 1:
                name = prefix+''.join(choice(ascii_lowercase+digits) for num in range(length))+suffix
            else:
                name = prefix+''.join(choice(ascii_lowercase) for num in range(length))+suffix
        elif case == 2:
            if include_digits == 1:
                name = prefix+''.join(choice(ascii_uppercase+digits) for num in range(length))+suffix
            else:
                name = prefix+''.join(choice(ascii_uppercase) for num in range(length))+suffix
        elif case == 3:
            if include_digits == 1:
                name = prefix+''.join(choice(ascii_letters+digits) for num in range(length))+suffix
            else:
                name = prefix+''.join(choice(ascii_letters) for num in range(length))+suffix
        elif case == 4:
            name = prefix+''.join(choice(digits) for num in range(length))+suffix
        else:
            if include_digits == 1:
                name = prefix+''.join(choice(ascii_lowercase+digits) for num in range(length))+suffix
            else:
                name = prefix+''.join(choice(ascii_lowercase) for num in range(length))+suffix
            
        return name
        

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        if self.method == 1:
            username_length = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Length: '))
            case = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Lowercase ['+Fore.RED+'2'+Fore.CYAN+']Uppercase ['+Fore.RED+'3'+Fore.CYAN+']Both ['+Fore.RED+'4'+Fore.CYAN+']Only Digits: '))
            
            include_digits = 0

            if case != 4:
                include_digits = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Include Digits ['+Fore.RED+'1'+Fore.CYAN+']yes ['+Fore.RED+'0'+Fore.CYAN+']no: '))
            
            prefix = str(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Prefix (leave it blank if you dont want to use): '))
            suffix = str(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Suffix (leave it blank if you dont want to use): '))
            print('')
            Run = True
            while Run:
                if active_count()<=self.threads_num:
                    name = self.GenName(username_length,include_digits,case,prefix,suffix)
                    Thread(target=self.SteamProfileCheck,args=(name,)).start()
        else:
            usernames = self.ReadFile('usernames.txt','r')
            for username in usernames:
                Run = True
                while Run:
                    if active_count()<=self.threads_num:
                        Thread(target=self.SteamProfileCheck,args=(username,)).start()
                        Run = False

    def SendWebhook(self,message,proxy):
        try:
            timestamp = str(datetime.utcnow())

            message_to_send = {"embeds": [{"title": "STEAM AVAILABLE USERNAME","description": message,"color": 65362,"author": {"name": "AUTHOR'S DISCORD SERVER [CLICK HERE]","url": "https://discord.gg/33UzcuY","icon_url": "https://media.discordapp.net/attachments/774991492690608159/774991574953623582/onemanbuildslogov3.png"},"footer": {"text": "MADE BY ONEMANBUILDS","icon_url": "https://media.discordapp.net/attachments/774991492690608159/774991574953623582/onemanbuildslogov3.png"},"timestamp": timestamp,"image": {"url": "https://media.discordapp.net/attachments/775255291499511808/775267475284688956/1530917611_steam_loading-avatar-dark.gif?width=467&height=467"}}]}
            
            headers = {
                'User-Agent':self.GetRandomUserAgent(),
                'Pragma':'no-cache',
                'Accept':'*/*',
                'Content-Type':'application/json'
            }

            payload = json.dumps(message_to_send)

            if self.use_proxy == 1:
                response = requests.post(self.webhook_url,data=payload,headers=headers,proxies=proxy)
            else:
                response = requests.post(self.webhook_url,data=payload,headers=headers)

            if response.text == "":
                self.PrintText(Fore.CYAN,Fore.RED,'WEBHOOK',f'MESSAGE {message} SENT')
            elif "You are being rate limited." in response.text:
                self.SendWebhook(message,proxy)
                self.webhook_retries += 1
                #self.PrintText(Fore.RED,Fore.CYAN,'WEBHOOK','YOU ARE RATELIMITED')
            else:
                #self.PrintText(Fore.RED,Fore.CYAN,'WEBHOOK','SOMETHING WENT WRONG RETRY')
                self.SendWebhook(message,proxy)
                self.webhook_retries += 1
        except:
            self.SendWebhook(message,proxy)
            self.webhook_retries += 1

    def SteamProfileCheck(self,name):
        try:
            session = requests.session()

            link = 'https://steamcommunity.com/id/{0}'.format(name)

            headers = {
                'User-Agent':self.GetRandomUserAgent(),
                'Content-Type':'application/json',
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Connection':'keep-alive'
            }
            response = ''

            proxy = self.GetRandomProxy()

            if self.use_proxy == 1:
                response = session.get(link,headers=headers,proxies=proxy)
            else:
                response = session.get(link,headers=headers)

            if 'Steam Community :: Error' in response.text:
                self.available = self.available+1
                self.PrintText(Fore.CYAN,Fore.RED,'AVAILABLE',name)
                with open('availables.txt','a',encoding='utf8') as f:
                    f.write(name+'\n')
                if self.enable_webhook == 1:
                    self.SendWebhook(name,proxy)
            elif 'Steam Community :: {0}'.format(name) in response.text:
                self.taken = self.taken+1
                self.PrintText(Fore.RED,Fore.CYAN,'TAKEN',name)
                with open('taken.txt','a',encoding='utf8') as f:
                    f.write(name+'\n')
            else:
                self.retries = self.retries+1
                self.SteamProfileCheck(name)
            
        except:
            self.retries = self.retries+1
            self.SteamProfileCheck(name)

if __name__ == '__main__':
    main = Main()
    main.Start()