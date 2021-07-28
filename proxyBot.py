from bs4 import BeautifulSoup
import random
import requests
import time

#grabs proxy list form https://free-proxy-list.net/
def proxy_grab():
    proxy_site = 'https://free-proxy-list.net/'
    proxy_req = requests.get(proxy_site).text
    proxy_soup = BeautifulSoup(proxy_req, 'lxml')
    proxy_text = proxy_soup.find('textarea')
    proxy_list = proxy_text.text
    proxy_list = proxy_list.split('\n')
    proxy_list = proxy_list[3:]

#this "for loop" is for sites with HTTP protocol
# if the site you want to scrape has HTTPS protocol comment this for loop and uncomment next "for loop"
    for i in proxy_list:
        j = i.split(':')
        if j[-1] == '80':
            valid_proxy_list.append(i)


##for sites with HTTPS:
    # for i in proxy_list:
    #     valid_proxy_list.append(i)


valid_proxy_list = []
proxy_grab()

count = 0
while True:
    if len(valid_proxy_list) > 0:
        try:
            print('trying')
            proxy_index = random.randint(0, len(valid_proxy_list) - 1)
            proxies = {
                "http":f'http://{valid_proxy_list[proxy_index]}',
                "https":f'http://{valid_proxy_list[proxy_index]}'
                }
            # icanhazip.com shows your IP and it's just a test, put your scraper code instead of the next three lines
            
            url = 'http://icanhazip.com/' # This should change to sites you want to scrape, http://icanhazip.com/ is just for test to show proxies are working
            my_ip = requests.get(url, proxies=proxies, timeout=5).text # Don't forget to set timeout and proxies argument in requests.get()
            # soup = BeautifulSoup(my_ip, 'lxml') #Use your BeautifulSoup command for your own scraper
            # The previous three lines should change to your scraper command
            count += 1
            print(f'#{proxy_index}: {my_ip}')
            print(f'Healthy proxies: {len(valid_proxy_list)}')
            print(f'{count} requests')
        except requests.exceptions.ProxyError as err:
            #Deletes invalid proxies
            del valid_proxy_list[proxy_index]
            print('Proxy is broken: trying another proxy')
            print(f'Healthy proxies: {len(valid_proxy_list)}')
            continue
        except requests.exceptions.Timeout as e:
            #Deletes proxies with 5 second or greater timeout, look at timeout argument in requests.get()
            del valid_proxy_list[proxy_index]
            print('Timeout Error: trying another proxy')
            print(f'Healthy proxies: {len(valid_proxy_list)}')
            continue
        except:
            del valid_proxy_list[proxy_index]
            print('Proxy failed trying another proxy')
            print(f'Healthy proxies: {len(valid_proxy_list)}')
            continue
    else:
        valid_proxy_list = []
        proxy_grab()