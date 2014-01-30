# encoding:utf-8
# Author: Chi Gao
# version History: 
                   #alpha 1.0  01/20/2014
 
 
import urllib2
import sys
import re
import time
import email
import smtplib
 
 
 
def send_email(keyword,posturl, title, author):
    to = 'receiver_account@gmail.com'
    gmail_user = 'sender_account@gmail.com'
    gmail_pwd = 'sender_account_password'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Alert:'+ title + ' \n'
    print header
    msg = header + '\n Title: ' + title + ' \n URL: ' + posturl +' \n' + 'Author: '+ author + '\n'
    smtpserver.sendmail(gmail_user, to, msg)
    print 'done!'
    smtpserver.close()
 
 
 
def monitor(keyword,flag=0,url="http://www.mitbbs.com/bbsdoc/FleaMarket.html"):
#keyword:   the item you want to sell/buy. for example, keyword = "beats". It is case insensitive.
#flag       = 0: buy (default=0)
#           = 1: sell
#url:       default = http://www.mitbbs.com/bbsdoc/FleaMarket.html
 
    #read page content
    try:
        page = urllib2.urlopen(url).read()
    except:
        return False
    #print non-unicode characters
    webpage_encoding = re.search('charset=(.+?)\"',page,re.IGNORECASE).group(1)
    system_encoding = sys.getfilesystemencoding()
    #print page.decode(webpage_encoding).encode(system_encoding)
    if flag==0:
        position = '出售'
        position_alt = '出'
    else:
        position = '求购'
        position_alt = '求'
    #for line in page.split('\n'):
    tmp=page.split('\n')
    for i in range(0,len(tmp)-1):
        try:
            line=tmp[i].decode(webpage_encoding).encode(system_encoding)
        #find post with correct keyword and position
        except:
            return False
        if ((position in line) or (position_alt in line)) and  (keyword.lower() in line.lower()):
            print line
            #http://stackoverflow.com/questions/1970028/python-regexp-find-two-keywords-in-a-line
            #<a class="news1" href="/article_t/FleaMarket/34365113.html">● [出售]itunes gift card 两百张 $10 @ 0.85</a>(607b)
            #    </strong></td>
            #        <td align="center">9/82</td><td><a href="/user_info/ImIn/cfdaad0153301130f68362d598cfc3bd"
            #get suburl and title
            suburl=re.findall('href="(.*)">', line)[0]
            posturl = 'http://www.mitbbs.com'+suburl
            title=re.findall('html">(.*)</a>',line)[0]
            #go to next 2 line and get author
            i=i+2
            line=tmp[i]
            author=re.findall(r'user_info/(.*?)/',line)[0]
            send_email(keyword,posturl, title, author)
 
 
if __name__ == '__main__':
    while 1:
        keywords=['item1','item2']
        flag=[0,1] # 0(出售)；  1(求购)
        for i in range(0,len(keywords)):
            print 'keyword '+keywords[i]
            monitor(keywords[i],flag=flag[i],url="http://www.mitbbs.com/bbsdoc/FleaMarket.html")
        time.sleep(600);
    
