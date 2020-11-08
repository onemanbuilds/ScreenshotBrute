import requests
from os import name,system
from random import choice,randint
from sys import stdout
from string import ascii_letters,digits
from time import sleep
from colorama import init,Style,Fore
from threading import Thread,active_count,Lock
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
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('useragents.txt','r')
        return choice(useragents)

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

    def __init__(self):
        self.SetTitle('One Man Builds Screenshot Brute Tool')
        self.clear()
        init(convert=True)
        self.title = Style.BRIGHT+Fore.RED+"""
                                  ╔═════════════════════════════════════════════════╗    
                                    ╔═╗╔═╗╦═╗╔═╗╔═╗╔╗╔╔═╗╦ ╦╔═╗╔╦╗  ╔╗ ╦═╗╦ ╦╔╦╗╔═╗
                                    ╚═╗║  ╠╦╝║╣ ║╣ ║║║╚═╗╠═╣║ ║ ║   ╠╩╗╠╦╝║ ║ ║ ║╣ 
                                    ╚═╝╚═╝╩╚═╚═╝╚═╝╝╚╝╚═╝╩ ╩╚═╝ ╩   ╚═╝╩╚═╚═╝ ╩ ╚═╝
                                  ╚═════════════════════════════════════════════════╝
                                                                                                    
                                
        """
        print(self.title)

        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        
        if self.use_proxy == 1:
            self.proxy_type = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Https ['+Fore.RED+'2'+Fore.CYAN+']Socks4 ['+Fore.RED+'3'+Fore.CYAN+']Socks5: '))
        
        self.download_picture = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Download ['+Fore.RED+'0'+Fore.CYAN+']No Download: '))
        self.option = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']PrntSC ['+Fore.RED+'2'+Fore.CYAN+']Imgur ['+Fore.RED+'3'+Fore.CYAN+']Both: '))
        self.threads = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        print('')
        self.lock = Lock()
        self.hits = 0
        self.downloads = 0
        self.removeds = 0
        self.bads = 0
        self.retries = 0
        

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def TitleUpdate(self):
        while True:
            self.SetTitle('One Man Builds Screenshot Brute Tool ^| HITS: {0} ^| DOWNLOADS: {1} ^| REMOVEDS: {2} ^| BADS: {3} ^| RETRIES: {4} ^| THREADS: {5}'.format(self.hits,self.downloads,self.removeds,self.bads,self.retries,active_count()-1))
            sleep(0.1)

    def ScrapePrntSc(self):
        try:
            random_end = ''.join(choice(ascii_letters+digits) for num in range(0,randint(6,7)))
            link = 'https://prnt.sc/{0}'.format(random_end)

            response = ''

            headers = {
                'User-Agent':self.GetRandomUserAgent()
            }

            if self.use_proxy == 1:
                response = requests.get(link,headers=headers,proxies=self.GetRandomProxy())
            else:
                response = requests.get(link,headers=headers)

            soup = BeautifulSoup(response.text,'html.parser')
            download_link = soup.find('meta',{'property':'og:image'})
            download_link = download_link['content']

            if 'image' in download_link:
                self.PrintText(Fore.CYAN,Fore.RED,'HIT',link)
                self.hits += 1
                with open('prntsc_good_links.txt','a') as f:
                    f.write(link+'\n')

                if self.download_picture == 1:
                    
                    response = requests.get(download_link,headers=headers)

                    filename = download_link.split('/')[-1]

                    with open('Downloads/prntsc/{0}'.format(filename),'wb') as f:
                        f.write(response.content)

                    self.downloads += 1
                    
            elif '//st.prntscr.com/' in download_link:
                self.PrintText(Fore.RED,Fore.CYAN,'IMAGE REMOVED',link)
                self.removeds += 1
                with open('prntsc_image_removed_links.txt','a') as f:
                    f.write(link+'\n')
            elif 'Access denied | image.prntscr.com used Cloudflare to restrict access' in response.text:
                self.retries += 1
                self.ScrapePrntSc()
            else:
                self.PrintText(Fore.RED,Fore.CYAN,'BAD',link)
                self.bads += 1
                with open('prntsc_bad_links.txt','a') as f:
                    f.write(link+'\n')
        except:
            self.retries += 1
            self.ScrapePrntSc()

    def ScrapeImgur(self):
        try:
            random_end = ''.join(choice(ascii_letters+digits) for num in range(0,7))
            link = 'https://imgur.com/{0}'.format(random_end)

            response = ''

            headers = {
                'User-Agent':self.GetRandomUserAgent()
            }

            if self.use_proxy == 1:
                response = requests.get(link,headers=headers,proxies=self.GetRandomProxy())
            else:
                response = requests.get(link,headers=headers)

            if response.status_code == 200:
                if 'og:image' in response.text:
                    self.PrintText(Fore.CYAN,Fore.RED,'HIT',link)
                    with open('imgur_good_links.txt','a') as f:
                        f.write(link+'\n')

                    if self.download_picture == 1:
                        soup = BeautifulSoup(response.text,'html.parser')
                        download_link = soup.find('meta',{'property':'og:image'})
                        download_link = download_link['content']
                        download_link = download_link.replace('?fb','')
                        
                        response = requests.get(download_link,headers=headers)

                        filename = download_link.split('/')[-1]

                        with open('Downloads/imgur/{0}'.format(filename),'wb') as f:
                            f.write(response.content)
                        self.downloads += 1
                else:
                    self.PrintText(Fore.RED,Fore.CYAN,'IMAGE REMOVED',link)
                    self.removeds += 1
                    with open('imgur_removed_links.txt','a') as f:
                        f.write(link+'\n')
                    
            elif response.status_code == 404:
                self.PrintText(Fore.RED,Fore.CYAN,'BAD',link)
                with open('imgur_bad_links.txt','a') as f:
                    f.write(link+'\n')
            else:
                self.retries += 1
                self.ScrapeImgur()
        except:
            self.retries += 1
            self.ScrapeImgur()

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        if self.option == 1:
            while True:
                if active_count() <= self.threads:
                    Thread(target=self.ScrapePrntSc).start()
                    
        elif self.option == 2:
            while True:
                if active_count() <= self.threads:
                    Thread(target=self.ScrapeImgur).start()
        else:
            while True:
                if active_count() <= self.threads:
                    Thread(target=self.ScrapePrntSc).start()
                    Thread(target=self.ScrapeImgur).start()
            
if __name__ == '__main__':
    main = Main()
    main.Start()