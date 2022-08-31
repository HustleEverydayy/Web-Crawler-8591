from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import csv
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
driver = webdriver.Chrome()
driver.get("https://www.8591.com.tw/") #限定手機遊戲，線上遊戲不能爬取。
xpath = '//*[@id="TS_gameList"]/li[2]' 
xpath1 = '//div[@id="po_searchServer"]/ul/li[1]' 
xpath2 = '//div[@id="po_searchType"]/ul/li[1]'
xpath3 = '//div[@id="po_searchType"]/ul/li[1]'
driver.maximize_window()
time.sleep(2)
print('請在下方輸入你要爬的手機遊戲  注意：只能手機遊戲，線上遊戲不行')
driver.find_element_by_class_name("ts_search").send_keys(input()) #輸入遊戲
time.sleep(2)
driver.find_element_by_xpath(xpath).click()
time.sleep(2)
driver.find_element_by_id("searchServer").click()
time.sleep(2)
driver.find_element_by_xpath(xpath1).click()
time.sleep(2)
driver.find_element_by_id("searchType").click()
time.sleep(2)
driver.find_element_by_xpath(xpath2).click()
time.sleep(2)
driver.find_element_by_id("searchBtn").click()
time.sleep(2)
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="11111111"
)
mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS `DB_108021011`") #有建立的話刪掉資料庫
mycursor.execute("CREATE DATABASE IF NOT EXISTS `DB_108021011`") #重創一個新的資料庫
mydb1 = pymysql.connect(
  host="localhost",
  user="root",
  password="11111111",
  database="DB_108021011"
)
mycursor = mydb1.cursor()
mycursor.execute("DROP TABLE IF EXISTS `Table_108021011`") #清除table裡的資料
mycursor.execute("CREATE TABLE IF NOT EXISTS `Table_108021011` (`Title` varchar(250) NOT NULL,`Seller_Member_ID` varchar(20) NOT NULL,`Seller_credit` varchar(50) NOT NULL,`Seller_Service` varchar(50) NOT NULL,`Game_Name` varchar(50) NOT NULL,`Items` varchar(50) NOT NULL,`Server` varchar(50) NOT NULL,`Mobile_Phone_System` varchar(50) NOT NULL,`Publish_Time` varchar(50) NOT NULL,`Price` varchar(50) NOT NULL,`Inventory` varchar(50) NOT NULL,`Views` varchar(50) NOT NULL)ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
db = pymysql.connect("localhost", "root", "11111111", "DB_108021011", charset="utf8mb4")      
cursor = db.cursor()  # 建立cursor物件
Table = "Table_108021011"
FieldNamesInOrder = "(Title, Seller_Member_ID, Seller_credit, Seller_Service, Game_Name, Items, Server, Mobile_Phone_System, Publish_Time, Price, Inventory, Views)"
csvfile = "動態網頁自動下載.csv"
print('請在下方輸入你要爬到的頁數')
cccc = input()
cccc=int(cccc)
aaaa=cccc+1
f = open(csvfile, 'a+', newline='', encoding='big5',errors='ignore') 
field_names = ['標題', '賣家會員編號', '賣家信用度', '賣家服務', '遊戲名稱', '物品', '伺服器', '手機系統', '刊登時間', '價格', '庫存', '瀏覽量']
field_names_en = ['Title', 'Seller_Member_ID', 'Seller_credit', 'Seller_Service', 'Game_Name', 'Items', 'Server', 'Mobile_Phone_System', 'Publish_Time', 'Price', 'Inventory', 'Views']
writer = csv.DictWriter(f, field_names_en)
           #writer = csv.writer(fp)
           #writer.writerow(field_names)
writer.writeheader()
for i in range(1,aaaa):
    htmltext = driver.page_source
    soup = BeautifulSoup(htmltext, 'html.parser')
    tag_table = soup.find(attrs={"id":"wrapper"})
    ALL_Professors = tag_table.find_all("div",class_="w-currency")
    for title in ALL_Professors:
                 record_dict = {'Title':"", 'Seller_Member_ID':"", 'Seller_credit':"", 'Seller_Service':"", 'Game_Name':"", 'Items':"", 'Server':"", 'Mobile_Phone_System':"", 'Publish_Time':"", 'Price':"", 'Inventory':"", 'Views':""}
                 ALL_title= title.find('a', 'show-title').text
                 #title_remove = emoji.demojize(ALL_title).replace("\u54b2","").replace("\u10ef","").replace("\u5239","").replace("\u2473","")
                 #title_remove2 = re.sub('\W+', '', title_remove).replace("_", '')
                 record_dict['Title'] = ALL_title.strip()
                 card_descriptions = title.find_all('div', class_='c-title-line')
                       #print(card_descriptions[4].text)
                 splited_text = card_descriptions[2].text.split('：')
                 record_dict['Seller_Member_ID'] = splited_text[1].strip()
                 split_text = card_descriptions[3].text.split('：')
                 splitlines_text= split_text[1].splitlines()
                       #print(splitlines_text[2])
                 record_dict['Seller_credit'] = splitlines_text[0]
                 record_dict['Seller_Service']  = splitlines_text[2]
                 split_game = card_descriptions[4].text.rsplit('/',2)
                       #print(split_game[0])
                 record_dict['Game_Name'] = split_game[0].strip()
                 record_dict['Items'] = split_game[1].strip()
                       #print(split_game[2])
                 splitlines_game = split_game[2].splitlines()
                       #print(splitlines_game)
                 splitchinese_game = re.split(r'[\u0061-\u007a,\u0020]',splitlines_game[1].lower().strip())
                       #print(splitchinese_game[0]) 分割中英文的方法 40行 分割英文 得到中文
                 if splitchinese_game[0] =="":
                     record_dict['Server'] = "共通伺服器"
                 else:    
                     record_dict['Server'] = splitchinese_game[0]
                 uncn = re.compile(r'[\u0061-\u007a,\u0020]')
                 en_splitlines = "".join(uncn.findall(splitlines_game[1].lower()))
                       #print(en_splitlines.strip()) re中文 得到英文
                 if en_splitlines.strip() =="":
                     record_dict['Mobile_Phone_System'] = '其他'
                 else:
                     record_dict['Mobile_Phone_System'] = en_splitlines.strip()
                 record_dict['Publish_Time'] = splitlines_game[2]
                 ALL_money= title.find('div', 'cl-wrap c-price').text
                       #print(ALL_money)
                 record_dict['Price'] = ALL_money.strip()
                 ALL_stock = title.find('div', 'cl-wrap c-store').text
                       #print(ALL_stock)
                 record_dict['Inventory'] = ALL_stock.strip()
                 ALL_Pageviews = title.find('div', 'cl-wrap c-pv').text
                       #print(ALL_Pageviews)
                 record_dict['Views'] = ALL_Pageviews.strip()
                 #print(record_dict)
                 writer.writerow(record_dict)            
                 sql = "INSERT INTO "+Table +" "+FieldNamesInOrder +" VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',{11})"
                 sql = sql.format(record_dict['Title'],
                                 record_dict['Seller_Member_ID'],
                                 record_dict['Seller_credit'],
                                 record_dict['Seller_Service'],
                                 record_dict['Game_Name'],
                                 record_dict['Items'],
                                 record_dict['Server'],
                                 record_dict['Mobile_Phone_System'],
                                 record_dict['Publish_Time'],
                                 record_dict['Price'],
                                 record_dict['Inventory'],
                                 record_dict['Views'])
                 print(sql)
                 try:
                     cursor.execute(sql)   # 執行SQL指令
                     db.commit() # 確認交易
                     print("新增一筆記錄...")
                 except:
                     db.rollback() # 回復交易 
                     print("新增記錄失敗...")    
    pos=0             
    for i in range(6):  
        pos += i*500 # 每次下滾500  
        js = "document.documentElement.scrollTop=%d" % pos  
        driver.execute_script(js)  
        time.sleep(2)
    driver.find_element_by_class_name("next01").click()
    time.sleep(3)          
driver.quit()            
f.close()
db = pymysql.connect("localhost", "root", "11111111", "DB_108021011", charset="utf8mb4")
cursor = db.cursor()  # 建立cursor物件
# 執行SQL指令SELECT
cursor.execute("SELECT Server,Mobile_Phone_System, count(*) FROM `table_108021011` group by Server,Mobile_Phone_System")

data = cursor.fetchall()   # 取出所有記錄

Server = []
Mobile_Phone_System = []
Total = []
# 取出查詢結果的每一筆記錄
for row in data:
    Server.append(row[0])
    Mobile_Phone_System.append(row[1])
    Total.append(row[2])
db.close()  # 關閉資料庫連接
dic = {"伺服器":Server,
     "系統":Mobile_Phone_System,
     "總數":Total}    
#dic_sort = sorted(dic.items(),key=lambda item:item[1])
#print(dic_sort)
df = pd.DataFrame(dic,index=['']*len(Server))
dff = df.sort_values(by=["系統","總數"])
print(dff)

#直方圖
x1 = dff['伺服器']
y1 = dff['系統']
y2 = dff['總數']
#plt.subplot(221)
plt.style.use("ggplot")
plt.rc('font', family='SimHei', size=13) #中文顯示參考這篇 https://zhuanlan.zhihu.com/p/55404865  
plt.bar(x1, y2, width=-0.355, label=y1[0], align = "edge")
if (len(y1)>=2):
    for i in range(len(y1)):
        b=0
        a=0
        c=0
        d=0
        if(y1[i]!=y1[i+1]):
            b=y1[i+1]
            a=x1[i+1:]
            c=y2[i+1:]
            d=i+1
            break      
    plt.bar(a, c,  width=0.355, label=b, align = "edge")
    d=i+1
    for i in range(len(y1)):
        try:
            if (y1[d]!=y1[d+1+i]):
                for i in range(len(y1)):
                    e=0
                    f=0
                    g=0
                    i=d
                    if(y1[i]!=y1[i+1]):
                        f=y1[i+1]
                        e=x1[i+1:]
                        g=y2[i+1:]
                        break   
                plt.bar(e, g, label=f)
                break
        except:
            print('')
            break
plt.xlabel("伺服器名稱", labelpad = 15)
plt.ylabel("總數", labelpad = 20)
plt.title('伺服器的系統比較', y=1.05)
plt.legend()
for a,b in zip(x1,y2):
    plt.text(a,b, b,ha='center', va='bottom', fontsize=20)
plt.savefig("selenium Bar Graph",   # 儲存圖檔
            bbox_inches='tight',               # 去除座標軸占用的空間
            dpi=500)                    # 去除所有白邊
plt.show()
plt.close()

