from bs4 import BeautifulSoup
import requests
import html5lib
import os
#import _thread
count = 0
def CrawlPages(http_url, history_url):
    '''request the http_url page and returns the urls on that page'''
    
    global count
    # The file to store the URLs
    path = 'C:\\Users\\wangd\\Desktop\\'
    file = open(path + 'results.txt', 'a') 
    print("Page URL: ", http_url)

    # Request the page
    # delete the if clause when more pages is wanted 
    if "NSFW_GIF" not in http_url:
        print('No info. Skipping...')
        print()
        return set()
    try:
        user_agent = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(http_url, headers=user_agent)
        if response.status_code != 200:
            print('Page Load Error! Skipping...')
            print()
            return set()
        html_doc = response.text
        soup = 	BeautifulSoup(html_doc, "html5lib")
    except:
        print("Get error. Skipping...\n")
        return set()

    # Get the picture on the page if qualified
    if "https://imgur.com/r/NSFW_GIF/" in http_url:
        # analyze the filename and download urls
        if(soup.h1 != None):
            image_name = soup.h1.string
            file.write(image_name + '\n' + http_url + '\n')
            # delete the illegal chars for a file name in win and add to the file path
            image_filename = path + 'results\\' + image_name.replace("\"", "").replace("\'", "").replace("*", "").replace("/", "").replace("?", "").replace("|", "").replace("<", "").replace(">", "").replace(":", "") + '.gif'
            image_id = http_url.split('/')[-1]
            image_url = "http://imgur.com/download/" + image_id + '/'+ image_name
            print('Page URL:', http_url)
            print('Download URL:', image_url)
            #try:
            if os.path.isfile(image_filename):
                print('File already exists.')
            else:
                print('Downloading...')
                image_response = requests.get(image_url)
                if response.status_code != 200:
                    print('Download error, maybe not a picture.')
                else:
                    image_file = open(image_filename, 'wb')
                    image_file.write(image_response.content)
                    image_file.close()
                    count += 1
                    print('Done! Download count=' + str(count))
            #except: 
            #    print('An error occured. Abandon file.')

    # Get the qualified URLs on the page
    print('Analyzing links...')
    url_set = set()
    link_list = soup.find_all('a')
    for x in link_list:
        url_tmp = x.get('href')
        # filter the urls to maintain only ones from imgur.com and have not been crawled
        if 'https://' not in url_tmp and 'http://' not in url_tmp:
            url_tmp = "https://imgur.com" + url_tmp
        if 'reddit.com' in url_tmp:
            continue
        if 'https://imgur.com' not in url_tmp:
            continue
        if url_tmp in history_url:
            continue
        url_set.add(url_tmp)
        history_url.add(url_tmp);

    file.close()
    print('Done!\n')
    return url_set

init_url = "https://imgur.com/r/NSFW_GIF"
depth = -1
history_url = {init_url}
while(depth < 10):
    if depth == -1:
        depth = 0
        url_set = CrawlPages(init_url, history_url)
    else:
        depth += 1
        result_set = set()
        #sorted(url_set)
        for sub_url in url_set:
            print("Depth:", depth)
            #_thread.start_new_thread(CrawlPages, [sub_url, history_url])
            result_set |= CrawlPages(sub_url, history_url)
        url_set = result_set

wait = input("press any key to continue")
