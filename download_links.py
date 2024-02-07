import os, sys, glob, re
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import uuid

from config import LINK_LIST_PATH

# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def save_link(url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()

    # WRITE YOUR CODE HERE
    #########################################
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)

    rootURL = 'https://mfa.gov.lk/category/news/media-releases/' #add page id
    pageURL =rootURL
    for pid in range(start_page + 1, 274):
        if pid == 1:
            resp = requests.get(pageURL, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
        else:
            prefix = "page/"
            prefix += str(pid)
            pageURL = '{}{}'.format(rootURL, prefix)
            resp = requests.get(pageURL, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})

        #print(pageURL)

        soup = bs(resp.text, "html.parser")
   
        articles = soup.find_all("article", {"class": "post"})

        for item in articles:
           
            # Save the collected url in the variable "collected_url"
            collected_url = (item.find('header').find("h2").find("a").get("href")) # buraya + "weburl" koymalı mıyım

            # Save the page that the url is taken from in the variable "page"
            page = pid
   
    # The following code block saves the collected url and page
    # Save the collected urls one by one so that if an error occurs
    # you do not have to start all over again
    
            if collected_url not in downloaded_url_list:
                print("\t", collected_url, flush=True)
                save_link(collected_url, page)
        #break  
    #########################################
        

if __name__ == "__main__":
    download_links_from_index()
