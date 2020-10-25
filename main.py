from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from random import choice
from threading import Thread,Lock,active_count
from fake_useragent import UserAgent
from string import ascii_letters,digits
from time import sleep
import requests

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        proxies = {
            "http":"http://{0}".format(choice(proxies_file)),
            "https":"https://{0}".format(choice(proxies_file))
            }
        return proxies

    def TitleUpdate(self):
        while True:
            self.SetTitle('One Man Builds Steam Username Checker Tool ^| AVAILABLE: {0} ^| TAKEN: {1} ^| RETRIES: {2} ^| THREADS: {3}'.format(self.available,self.taken,self.retries,active_count()-1))
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        self.clear()
        self.SetTitle('One Man Builds Steam Username Checker Tool')
        self.title = Style.BRIGHT+Fore.RED+"""                                        
                                                                                                    
                 ____ _____ _____    _    __  __   _   _ ____  _____ ____  _   _    _    __  __ _____ 
                / ___|_   _| ____|  / \  |  \/  | | | | / ___|| ____|  _ \| \ | |  / \  |  \/  | ____|
                \___ \ | | |  _|   / _ \ | |\/| | | | | \___ \|  _| | |_) |  \| | / _ \ | |\/| |  _|  
                 ___) || | | |___ / ___ \| |  | | | |_| |___) | |___|  _ <| |\  |/ ___ \| |  | | |___ 
                |____/ |_| |_____/_/   \_|_|  |_|  \___/|____/|_____|_| \_|_| \_/_/   \_|_|  |_|_____|
                                                                                                    
                                                                                                    
                                    ____ _   _ _____ ____ _  _______ ____                                               
                                   / ___| | | | ____/ ___| |/ | ____|  _ \                                              
                                  | |   | |_| |  _|| |   | ' /|  _| | |_) |                                             
                                  | |___|  _  | |__| |___| . \| |___|  _ <                                              
                                   \____|_| |_|_____\____|_|\_|_____|_| \_\                                             
                                                                                                        

                                                 
        """
        print(self.title)
        self.available = 0
        self.taken = 0
        self.retries = 0
        self.ua = UserAgent()
        self.lock = Lock()
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        self.method = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Brute ['+Fore.RED+'0'+Fore.CYAN+']From Usernames.txt: '))
        self.threads_num = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        print('')

    def GenName(self,length,include_digits,prefix,suffix):
        if include_digits == 1:
            name = prefix+''.join(choice(ascii_letters+digits) for num in range(length))+suffix
        else:
            name = prefix+''.join(choice(ascii_letters) for num in range(length))+suffix
        return name
        

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        if self.method == 1:
            username_length = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Length: '))
            include_digits = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Include Digits ['+Fore.RED+'1'+Fore.CYAN+']yes ['+Fore.RED+'0'+Fore.CYAN+']no: '))
            prefix = str(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Prefix (leave it blank if you dont want to use): '))
            suffix = str(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Suffix (leave it blank if you dont want to use): '))
            print('')
            Run = True
            while Run:
                if active_count()<=self.threads_num:
                    name = self.GenName(username_length,include_digits,prefix,suffix)
                    Thread(target=self.SteamProfileCheck,args=(name,)).start()
        else:
            usernames = self.ReadFile('usernames.txt','r')
            for username in usernames:
                Run = True

                if active_count()<=self.threads_num:
                    Thread(target=self.SteamProfileCheck,args=(username,)).start()
                    Run = False

    def SteamProfileCheck(self,name):
        try:
            session = requests.session()

            link = 'https://steamcommunity.com/id/{0}'.format(name)

            headers = {
                'User-Agent':self.ua.random,
                'Content-Type':'application/json',
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Connection':'keep-alive'
            }
            response = ''

            if self.use_proxy == 1:
                response = session.get(link,headers=headers,proxies=self.GetRandomProxy())
            else:
                response = session.get(link,headers=headers)

            if 'Steam Community :: Error' in response.text:
                self.available = self.available+1
                self.PrintText(Fore.CYAN,Fore.RED,'AVAILABLE',name)
                with open('availables.txt','a',encoding='utf8') as f:
                    f.write(name+'\n')
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