# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, csv



def drivePref(pref):
    pref_shopdic_list=list()
    page = 1
    while 1:
        shopdic_list=drivePage(pref,page)
        pref_shopdic_list.extend(shopdic_list)
        if(len(driver.find_elements_by_link_text(u"次へ"))!=0):
            page = page+1
        else:
            return pref_shopdic_list
    
def drivePage(pref,page):
    print "drive: pref: "+str(pref)+" page:"+str(page)
    driver.get(base_url + "/game/facility/e-AMUSEMENT/p/result.html?finder=area&gkey=GITADORAGF&area=-1&pref="+str(pref)+"&page="+str(page))
    
    time.sleep(10)

    shopdic_list=parsePage()

    return shopdic_list
    
def parsePage():
    shopInfos=driver.find_elements_by_class_name("shopInfo")
    
    shopdic_List=list()
    pref_name=re.findall(">\s.*?(.*)",driver.find_element_by_id("shopList").find_element_by_tag_name("form").find_element_by_tag_name("h4").text)[0].encode("utf-8")

    for shopInfo in shopInfos:
       shopdic_List.append(parseShopInfo(shopInfo,pref_name))

    return shopdic_List

def parseShopInfo(shopInfo,pref_name):
    #各店舗情報を保有する辞書を作成
    shopdic=dict()
    
    shopInfo_text=shopInfo.text.encode("utf-8")
    #店舗名
    shopdic["Name"]=shopInfo.find_element_by_tag_name("h5").text.encode("utf-8")
    #住所
    address_s = re.findall('(.*?)\n',shopInfo_text)
    if(len(address_s)!=1):
        shopdic["Address"]=pref_name+address_s[1]
    else:
        shopdic["Address"]="NULL"
    #営業時間
    eigyo_s=re.findall('営業時間:(.*)',shopInfo_text)
    if(len(eigyo_s)!=0):
        shopdic["Time"]=eigyo_s[0]
    else:
        shopdic["Time"]="NULL"
    
    #定休日
    teikyu_s=re.findall('定休日:(.*)',shopInfo_text)
    if(len(teikyu_s)!=0):
        shopdic["Close"]=teikyu_s[0]
    else:
        shopdic["Close"]="NULL"
    
    #電話番号
    tel_s=re.findall('電話番号:(.*)',shopInfo_text)
    if(len(tel_s)!=0):
        shopdic["Tel"]=tel_s[0]
    else:
        shopdic["Tel"]="NULL"
    
    #PASELI
    if(re.search('PASELI',shopInfo_text) is None):
        shopdic["PASELI"]="0"
    else:
        shopdic["PASELI"]="1"
            
    return shopdic

driver = webdriver.Firefox()
base_url = "http://p.eagate.573.jp/"
shopdic_whole_list = list()

CSV_header=['Name','Address','Time','Close','Tel','PASELI']

for pref in range(1, 48):
    pref_shopdic_list=drivePref(pref)
    shopdic_whole_list.extend(pref_shopdic_list)
    print shopdic_whole_list
    exit(1)
    #CSV書き込み
    header = dict([(val,val)for val in CSV_header])
    with open(str(pref)+".csv", mode='w') as f:
        pref_shopdic_list.insert(0,header)
        for shopdic in pref_shopdic_list:
            writedata=""
            for header in CSV_header:
                if(header==CSV_header[0]):#最初のカラムかどうかで,の位置が変わる
                    writedata=shopdic[header]
                else:
                    writedata=writedata+","+shopdic[header]
            writedata=writedata+"\n"
            f.write(writedata)
#        writer = csv.DictWriter(f, CSV_header,extrasaction='ignore')
#        writer.writerows(shopdic_whole_list)
