import os
import requests
import random
import sys
import string
from time import sleep
from colorama import init,Fore
from threading import Thread, Lock
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from hashlib import md5


class Main:
    def clear(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):
            os.system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        os.system("title {0}".format(title_name))
        
    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        proxies = {
            "http":"http://{0}".format(random.choice(proxies_file)),
            "https":"https://{0}".format(random.choice(proxies_file))
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
        self.use_proxy = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to use proxies [1] yes [0] no: '))
        self.download_picture = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to download pictures [1] yes [0] no: '))
        self.option = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to scrape from [1]PrntSC [2]Imgur [3] Both: '))
        print('')
        self.header = headers = {'User-Agent':self.ua.random}

    def ScrapePrntSc(self):
        lock = Lock()
        while True:
            try:
                lock.acquire()
                random_end = ''.join(random.choice(string.ascii_letters+'0123456789') for num in range(0,random.randint(6,7)))
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
                    print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] GOOD | {0}'.format(link))
                    with open('prntsc_good_links.txt','a') as f:
                        f.write(link+'\n')

                    if self.download_picture == 1:
                        
                        response = requests.get(download_link,headers=self.header)

                        filename = download_link.split('/')[-1]

                        with open('Downloads/prntsc/{0}'.format(filename),'wb') as f:
                            f.write(response.content)
                        
                elif '//st.prntscr.com/' in download_link:
                    print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] IMAGE REMOVED | {0}'.format(link))
                    with open('prntsc_image_removed_links.txt','a') as f:
                        f.write(link+'\n')
                else:
                    print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] BAD | {0}'.format(link))
                    with open('prntsc_bad_links.txt','a') as f:
                        f.write(link+'\n')

                lock.release()
            except:
                self.ScrapePrntSc()

    def ScrapeImgur(self):
        lock = Lock()
        while True:
            try:
                lock.acquire()
                random_end = ''.join(random.choice(string.ascii_letters+'0123456789') for num in range(0,7))
                link = 'https://imgur.com/{0}'.format(random_end)

                response = ''

                if self.use_proxy == 1:
                    response = requests.get(link,headers=self.header,proxies=self.GetRandomProxy())
                else:
                    response = requests.get(link,headers=self.header)

                if response.status_code == 200:
                    if 'og:image' in response.text:
                        print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] GOOD | {0}'.format(link))
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
                        print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] IMAGE REMOVED | {0}'.format(link))
                        with open('imgur_removed_links.txt','a') as f:
                            f.write(link+'\n')
                        
                elif response.status_code == 404:
                    print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] BAD | {0}'.format(link))
                    with open('imgur_bad_links.txt','a') as f:
                        f.write(link+'\n')
                else:
                    print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] RATELIMITED WAITING FOR 10 SECONDS')
                    sleep(10)

                lock.release()
            except:
                self.ScrapeImgur()
    
    def Start(self):
        if self.option == 1:
            threading = Thread(target=self.ScrapePrntSc).start()
        elif self.option == 2:
            threading = Thread(target=self.ScrapeImgur).start()
        else:
            threading1 = Thread(target=self.ScrapePrntSc).start()
            threading2 = Thread(target=self.ScrapeImgur).start()
            
if __name__ == '__main__':
    main = Main()
    main.Start()