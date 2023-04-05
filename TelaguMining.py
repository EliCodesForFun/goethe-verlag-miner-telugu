from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time


def download_mp3(url, filename):
    response = requests.get(url)
    print("Downloading file: " + filename + ".mp3")
    time.sleep(0.3)
    try:
        with open(f"C:\Mining\{filename}.mp3", 'wb') as f:
            f.write(response.content)
    except OSError:
        print("Was unable to download file due to name issue probably - " + filename + ".mp3")
        return

def bulk_download(mp3_list, english_text, telagu_text):
    for link, eng, tel in zip(mp3_list, english_text, telagu_text):
        download_mp3(link, f"{eng} - {tel}")

def get_mp3_links(soup):
    #Find links
    href_elements = soup.find_all(src=re.compile("mp3"))
    regex_for_mp3 = r'https://.*.mp3'
    re.search(regex_for_mp3, str(href_elements[0]))[0]
    mp3_list = [re.search(regex_for_mp3, str(ele))[0] for ele in href_elements]
    print("Number of mp3 links found: " + str(len(mp3_list)))
    del(mp3_list[0:2]) #remove the first two mp3 files links, which are in the heading I didn't grab lmao
    return mp3_list

def get_eng_and_telagu_elements(soup):
    #Get all <div class="Stil35">I </div>
    english_text_elements = soup.find_all('div', class_="Stil35")
    english_text =[]
    for ele in english_text_elements:
        english_text.append(ele.get_text().strip())
    for i, text in enumerate(english_text):
        english_text[i] = english_text[i].replace("\n", "")
        english_text[i] = english_text[i].replace("\r", "")
        english_text[i] = english_text[i].replace("/", "")
        english_text[i] = english_text[i].replace("?", "")
        english_text[i] = english_text[i].replace(".", "")

    len(english_text) #20
    english_text[17] #last good value

    #Get all <div class="Stil45">I </div>
    telagu_text_elements = soup.find_all('div', class_="Stil45")
    telagu_text =[]
    for ele in telagu_text_elements:
        telagu_text.append(ele.get_text().strip())
    for i, text in enumerate(telagu_text):
        telagu_text[i] = telagu_text[i].replace("\n", "")
        telagu_text[i] = telagu_text[i].replace("\r", "")
        telagu_text[i] = telagu_text[i].replace("/", "")
        telagu_text[i] = telagu_text[i].replace("?", "")
        telagu_text[i] = telagu_text[i].replace(".", "")

    len(telagu_text) #18 elements
    telagu_text[17] #last good value

    print("Number of telagu elements found: " + str(len(telagu_text)))
    return english_text, telagu_text


numlist = [1,2,3,4,5]
del(numlist[-2:])

#Get Links
url = r'https://www.goethe-verlag.com/book2/EM/EMTE/EMTE003.HTM'

#links = [f"https://www.goethe-verlag.com/book2/EM/EMTE/EMTE{num:03}.HTM" for num in range(3,103)]
#had to change vpn and start from 60 onward lmao
links = [f"https://www.goethe-verlag.com/book2/EM/EMTE/EMTE{num:03}.HTM" for num in range(85,103)]

for url in links:
    print("connecting to url: {}".format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())
    english_text, telagu_text = get_eng_and_telagu_elements(soup)
    bulk_download(get_mp3_links(soup), english_text, telagu_text)



import os
import re
filelist = os.listdir(r'C:\Mining')
regex_string = r'(.* - .*?)([A-Za-z])'
filelist2 = []
for file in filelist:
    filelist2.append(re.sub(regex_string, r'\1 - \2', file))

with open("derp.txt", "w") as f:
    for line in filelist2:
        f.writelines(filelist2)