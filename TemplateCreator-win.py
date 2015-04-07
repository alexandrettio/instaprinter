#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")
from fpdf import Template
import urllib2
from urllib import urlencode
import json
from datetime import datetime, date, time
import time
import sqlite3
import os
import re
import config

CLIENT_ID = config.CLIENT_ID
TAG = config.TAG

def call_api_inst(method, params):
    url = "https://api.instagram.com/v1/%s?%s" % (method, urlencode(params))
    response = json.loads(urllib2.urlopen(url).read())
    return response

def create_pdf(smth):
  creation_time = smth['created_time']
  if int(creation_time) < int(current_print_interval_begin):
    print int(creation_time), int(current_print_interval_begin)
    sys.exit(0)
  f = Template(elements=elements, title="Instaprinter", format=(w, h))
  f.pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
  f.pdf.add_font('ProximaNova', '', 'ProximaNova-Reg.ttf', uni=True)
  f.add_page()

  musername = smth['user']['username']
  mprofilepicture = smth['user']['profile_picture']
  mphotourl = smth['images']['standard_resolution']['url']
  if 'caption' in smth:
    if smth['caption'] != None:
      mtext = smth['caption']['text']
    else:
      return
  else:
    return
  if len(mtext) > 230:
    mtext = mtext[:230]+ '...'
  mtext = re.sub(u'[^\u0020-\u00BF\u0410-\u0451]', '', mtext)
  mtype = smth['type']
  mid =  smth['id']
  if mtype != 'image':
    return
  else:
    os.popen ('curl %s > images/content.jpg' %mphotourl)
    os.popen ('curl %s > images/profile.jpg' %mprofilepicture)  
    f["address"] = config.address
    f["avatar"] = '''.\images\profile.jpg'''
    f["photo"] = '''.\images\content.jpg'''
    f["username"] = musername
    f["logo"] = '''.\images\logo.jpg'''
    f["place"] = '''.\images\place.png'''
    f["clubname"] = config.clubname
    f["phone"] = config.phone
    f["description"] = mtext
    f.render('''.\results\%s.pdf''' %mid)
    # os.popen ("lpr -P%s results/%s-5.pdf" %(config.printer_name, mid))
    # os.popen ("move .\%s.pdf .\yesref" %mid)
    os.popen ("acrord32.exe /n /t .\results\%s.pdf" %mid)
    print "done %s.pdf" %mid
    
#Не, константы это круто, все таки
h = 150.0
w = 100.0
margin = 3.0
s_size = 4.0  
a_size = 12.5
p_size = w - 2 * margin 
dt = 1.0
elements = [
    { 
      'name': 'avatar', 
      'type': 'I', 
      'x1': margin, 
      'y1': margin, 
      'x2': margin + a_size, 
      'y2': margin + a_size, 
      'font': None, 
      'size': 0.0, 
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0, 
      'background': 0, 
      'align': 'I', 
      'text': 'logo', 
      'priority': 2,  
    },
    { 
      'name': 'username', 
      'type': 'T', 
      'x1': (margin + a_size + margin), 
      'y1': (margin + a_size/2 - s_size/2),  
      'x2': (margin + a_size + margin + 10.0), 
      'y2': (margin + a_size/2 + s_size/2),  
      'font': 'ProximaNova', 
      'size': 10.0, 
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0x3f729b, 
      'background': 0, 
      'align': 'L', 
      'text': 'logo', 
      'priority': 2,  
    },
    { 
      'name': 'photo', 
      'type': 'I', 
      'x1': margin, 
      'y1': (margin * 2 + a_size), 
      'x2': (w - margin), 
      'y2': (margin * 2 + a_size + p_size), 
      'font': None, 
      'size': 0.0, 
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0, 
      'background': 0, 
      'align': 'I', 
      'text': '', 
      'priority': 2,  
    },
    { 
      'name': 'description', 
      'type': 'T', 
      'x1': margin, 
      'y1': (margin * 3 + a_size + p_size), 
      'x2': (w - margin), 
      'y2': (margin * 3 + a_size + p_size + s_size), 
      'font': 'ProximaNova', 
      'size': 8.0, 
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0x222, 
      'background': 0, 
      'align': 'I', 
      'text': '', 
      'multiline': 1,
      'priority': 2,  
    },
    { 
      'name': 'adres', 
      'type': 'T', 
      'x1': (3 * margin + a_size), 
      'y1': (h-(3 * margin) - dt), 
      'x2': (w - margin), 
      'y2': (h-(2 * margin) - dt), 
      'font': 'DejaVu',
      'size': 7.0,
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0, 
      'background': 0, 
      'align': 'L', 
      'text': '', 
      'multiline': 1,
      'priority': 2,  
    },
    { 
      'name': 'logo', 
      'type': 'I', 
      'x1': margin, 
      'y1': (h-(margin + a_size)), 
      'x2': margin+a_size, 
      'y2': (h-margin), 
      'font': None, 
      'size': 0.0, 
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0, 
      'background': 0, 
      'align': 'I', 
      'text': '', 
      'priority': 2,
    },
    { 
      'name': 'place', 
      'type': 'I', 
      'x1': (2 * margin + a_size), 
      'y1': (h-(3 * margin) - dt), 
      'x2': (3 * margin + a_size), 
      'y2': (h-(2 * margin) - dt), 
      'font': None, 
      'size': 0.0, 
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0, 
      'background': 0, 
      'align': 'I', 
      'text': '', 
      'priority': 2,
    },
    { 
      'name': 'clubname', 
      'type': 'T', 
      'x1': (2 * margin + a_size), 
      'y1': (h-(4.5 * margin)  - dt), 
      'x2': (3 * margin + a_size), 
      'y2': (h-(3.5 * margin)  - dt), 
      'font': 'DejaVu', 
      'size': 12.0, 
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0, 
      'background': 0, 
      'align': 'L', 
      'text': '', 
      'priority': 2,
    },
    { 
      'name': 'phone', 
      'type': 'T', 
      'x1': (2 * margin + a_size), 
      'y1': (h-(2 * margin) - dt), 
      'x2': (3 * margin + a_size), 
      'y2': (h-margin  - dt), 
      'font': 'DejaVu', 
      'size': 7.0, 
      'bold': 0, 
      'italic': 0, 
      'underline': 0, 
      'foreground': 0, 
      'background': 0, 
      'align': 'L', 
      'text': '', 
      'priority': 2,
    },
]

current_print_interval_begin = int(time.time())-config.DELTA*60
response = call_api_inst('/tags/%s/media/recent'%TAG, [('client_id', CLIENT_ID)])
if 'pagination' in response:
    if 'data' in response:
        a = response['data']
    else:
        # print 'Ошибочка'
        pass
    for smth in a:
        create_pdf(smth)
    while 'next_url' in response['pagination']:

       url = response['pagination']['next_url']
       response = json.loads(urllib2.urlopen(url).read())  
       if 'data' in response:
         a = response['data']
       else:
         # print 'Ошибочка'
         pass
       for smth in a:
         create_pdf(smth)
else:
    if 'data' in response:
        a = response['data']
    else:
        # print 'Ошибочка'
        pass
    for smth in a:
        create_pdf(smth)
    pass
  

# alexandret:results Alexandret$ lpr -PSamsung_SCX_4x21_Series 835551343043089489_528383012-5.pdf 
# alexandret:results Alexandret$ lpq -PSamsung_SCX_4x21_Series

