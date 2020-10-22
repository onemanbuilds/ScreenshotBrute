from os import name,system
import requests
from random import choice,randint
from sys import stdout
from string import ascii_letters
from time import sleep
from colorama import init,Fore
from threading import Thread,active_count,Lock
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from hashlib import md5
from sys import stdout

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

    def __init__(self):
        self.SetTitle('One Man Builds Screenshot Brute Tool')
        self.clear()
        init(convert=True)
        title = Fore.YELLOW+"""
                            
                    ____ ____ ____ ____ ____ _  _ ____ _  _ ____ ___    ___  ____ _  _ ___ ____ 
                    [__  |    |__/ |___ |___ |\ | [__  |__| |  |  |     |__] |__/ |  |  |  |___ 
                    ___] |___ |  \ |___ |___ | \| ___] |  | |__|  |     |__] |  \ |__|  |  |___ 
                                                                                                
                            
        """
        print(title)
        self.ua = UserAgent()
        self.use_proxy = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to use proxies [1]yes [0]no: '))
        self.download_picture = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to download pictures [1]yes [0]no: '))
        self.option = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to scrape from [1]PrntSC [2]Imgur [3]Both: '))
        self.threads = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Threads: '))
        print('')
        self.header = headers = {'User-Agent':self.ua.random}
        self.lock = Lock()

    def PrintText(self,info_name,text,info_color:Fore):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(info_color+'['+Fore.WHITE+info_name+info_color+f'] {text}\n')
        self.lock.release()

    def ScrapePrntSc(self):
        try:
            random_end = ''.join(choice(ascii_letters+'0123456789') for num in range(0,randint(6,7)))
            link = 'https://prnt.sc/{0}'.format(random_end)

            response = ''

            if self.use_proxy == 1:
                response = requests.get(link,headers=self.header,proxies=self.GetRandomProxy())
            else:
                response = requests.get(link,headers=self.header)

            soup = BeautifulSoup(response.text,'html.parser')
            download_link = soup.find('meta',{'property':'og:image'})
            download_link = download_link['content']

            if 'image' in download_link:
                self.PrintText('!','GOOD | {0}'.format(link),Fore.GREEN)
                with open('prntsc_good_links.txt','a') as f:
                    f.write(link+'\n')

                if self.download_picture == 1:
                    
                    response = requests.get(download_link,headers=self.header)

                    filename = download_link.split('/')[-1]

                    with open('Downloads/prntsc/{0}'.format(filename),'wb') as f:
                        f.write(response.content)
                    
            elif '//st.prntscr.com/' in download_link:
                self.PrintText('-','IMAGE REMOVED | {0}'.format(link),Fore.RED)
                with open('prntsc_image_removed_links.txt','a') as f:
                    f.write(link+'\n')
            elif 'Access denied | image.prntscr.com used Cloudflare to restrict access' in response.text:
                self.ScrapePrntSc()
            else:
                self.PrintText('-','BAD | {0}'.format(link),Fore.RED)
                with open('prntsc_bad_links.txt','a') as f:
                    f.write(link+'\n')
        except:
            self.ScrapePrntSc()

    def ScrapeImgur(self):
        try:
            random_end = ''.join(choice(ascii_letters+'0123456789') for num in range(0,7))
            link = 'https://imgur.com/{0}'.format(random_end)

            response = ''

            if self.use_proxy == 1:
                response = requests.get(link,headers=self.header,proxies=self.GetRandomProxy())
            else:
                response = requests.get(link,headers=self.header)

            if response.status_code == 200:
                if 'og:image' in response.text:
                    self.PrintText('!','GOOD | {0}'.format(link),Fore.GREEN)
                    with open('imgur_good_links.txt','a') as f:
                        f.write(link+'\n')

                    if self.download_picture == 1:
                        soup = BeautifulSoup(response.text,'html.parser')
                        download_link = soup.find('meta',{'property':'og:image'})
                        download_link = download_link['content']
                        download_link = download_link.replace('?fb','')
                        
                        response = requests.get(download_link,headers=self.header)

                        filename = download_link.split('/')[-1]

                        with open('Downloads/imgur/{0}'.format(filename),'wb') as f:
                            f.write(response.content)
                else:
                    self.PrintText('-','IMAGE REMOVED | {0}'.format(link),Fore.RED)
                    with open('imgur_removed_links.txt','a') as f:
                        f.write(link+'\n')
                    
            elif response.status_code == 404:
                self.PrintText('-','BAD | {0}'.format(link),Fore.RED)
                with open('imgur_bad_links.txt','a') as f:
                    f.write(link+'\n')
            else:
                self.PrintText('-','RATELIMITED WAITING FOR 10 SECONDS',Fore.RED)
                sleep(10)
        except:
            self.ScrapeImgur()
    
    def Start(self):
        if self.option == 1:
            while True:
                if active_count() <= self.threads:
                    threading = Thread(target=self.ScrapePrntSc).start()
                    
        elif self.option == 2:
            while True:
                if active_count() <= self.threads:
                    threading = Thread(target=self.ScrapeImgur).start()
        else:
            while True:
                if active_count() <= self.threads/2:
                    threading1 = Thread(target=self.ScrapePrntSc).start()
                    threading2 = Thread(target=self.ScrapeImgur).start()
            
if __name__ == '__main__':
    main = Main()
    main.Start()