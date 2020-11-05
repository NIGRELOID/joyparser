#!/usr/bin/env python
import os
import sys
import requests
import re
from bs4 import BeautifulSoup
import shutil
from urllib.parse import unquote
from pathlib import Path
import time

headers = {
  'Host': 'img1.reactor.cc',
  #	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
  'Accept': 'image/webp,*/*',
  #	'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  #	'Referer': 'http://joyreactor.cc/',
  'Connection': 'keep-alive',
  'Cache-Control': 'max-age=0',
  'Pragma': 'no-cache'
}

termsize = shutil.get_terminal_size((80, 20))


def download_file(url, name, headers):
  if not os.path.isfile(name):
    with requests.get(url, stream=True, headers=headers) as r:
      r.raise_for_status()
      with open(name, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
  else:
    print('File already exists, skipping.')
    time.sleep(0.1)


for link in sys.argv[1:]:
  if '#' in link or not link:
    continue
  elif '!' in link:
    parseComments = True
    link = link[1:]

  print('=' * termsize[0])
  print(('Downloading: ' + link).center(termsize[0], ' '))
  print('=' * termsize[0])

  with requests.Session() as req:
    page = req.get(link)
    bs = BeautifulSoup(page.text, 'html.parser')
    page.raise_for_status()

    exclude = ['default_avatar.jpeg', '/tag',
           '/images/icon_en.png', '/thumbnail', '/avatar', '/comment']
    if parseComments:
      exclude = exclude[:-1]

    path = "downloads/" + link.split('/')[-1] + "/"
    Path(path).mkdir(parents=True, exist_ok=True)

    links = bs.find_all('img')
    filtered = [link for link in links if not any(
      word in link['src'] for word in exclude)]

    for index, image in enumerate(filtered):
      if parseComments:
        fullLink = image['src']
      else:
        dlLink = 'http://img1.joyreactor.cc/pics/post/full/'
        fullLink = dlLink + image['src'].split('/')[-1]
      filename = image['src'].split('/')[-1]

      print('Downloading %d/%d: %s' %
          (index + 1, len(filtered), unquote(filename)))
      download_file(fullLink, path + unquote(filename), headers)
