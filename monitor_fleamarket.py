#monitor_fleamarket.py

import urllib2
import sys
import re
import time
import email
import smtplib



def send_email(keyword,posturl, title, author):
    # I would suggest to use gmail for both send-to and send-from emails
    to = 'send-to@email-address'
    gmail_user = 'send-from@email-address'
    gmail_pwd = 'send-from-email-password'
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
    #since some point in 07/2014, mitbbs blocked direct data retrieval／bulk content download using bots.
    #So I need to DOWNLOAD DATA DUMPS (use req)
    try:  
        #page = urllib2.urlopen(url).read()
        req = urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0'})      
        page = urllib2.urlopen(req).read()
    except:
        print 'unable to load page. existing...'
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
            print i
            print line
            #http://stackoverflow.com/questions/1970028/python-regexp-find-two-keywords-in-a-line
            #<a class="news1" href="/article_t/FleaMarket/34365113.html">● [出售]itunes gift card 两百张 $10 @ 0.85</a>(607b)
            #    </strong></td>
            #        <td align="center">9/82</td><td><a href="/user_info/ImIn/cfdaad0153301130f68362d598cfc3bd"
            #get suburl and title
            
            # As of 04/14, the format on mitbbs is changed
            #
            #                   <a class="news1" href="/article_t/FleaMarket/34573663.html">
            #            ● 【求购】Bose soundlink MINI  And  soundlink III小                    </a>(242b)
            #</strong></td>
            #<td align="center">2/15</td><td><a href="/user_info/Eks/3283ee582c15e6ecf9756cd8bbe63c25" class="news">Eks</a><br><span class="black10">2014-04-28</span></td><td align="left"><a href="/user_info/Eks" class="news">Eks</a><br><span class="black10">04-28 19:11</span></td>      </tr>
            line2=tmp[i-1].decode(webpage_encoding).encode(system_encoding)            
            suburl=re.findall('href="(.*)">', line2)[0]
            posturl = 'http://www.mitbbs.com'+suburl
            #title=re.findall('html">(.*)</a>',line)[0]
            title=re.findall(' (.*)</a>',line)[0]
            #go to next 2 line and get author
            i=i+2
            line=tmp[i]
            author=re.findall(r'user_info/(.*?)/',line)[0]
            send_email(keyword,posturl, title, author)


if __name__ == '__main__':
    keywords=['item1','item2']
    flag=[0,1] # 0(出售)；  1(求购)
    for i in range(0,len(keywords)):
        print 'keyword '+keywords[i] 
        monitor(keywords[i],flag=flag[i],url="http://www.mitbbs.com/bbsdoc/FleaMarket.html")

