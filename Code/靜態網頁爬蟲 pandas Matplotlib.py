import requests
from bs4 import BeautifulSoup
import csv
import re
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
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

#url='https://www.8591.com.tw/mobileGame-list.html?searchGame=27938&searchServer=0&searchType=&searchKey=&firstRow=0'
a=0
csvfile = "靜態網頁自動下載.csv"
f = open(csvfile, 'a+', newline='', encoding='big5',errors='ignore') #ignore 可以忽略讀寫的錯誤亂碼 
field_names = ['標題', '賣家會員編號', '賣家信用度', '賣家服務', '遊戲名稱', '物品', '伺服器', '手機系統', '刊登時間', '價格', '庫存', '瀏覽量']
field_names_en = ['Title', 'Seller_Member_ID', 'Seller_credit', 'Seller_Service', 'Game_Name', 'Items', 'Server', 'Mobile_Phone_System', 'Publish_Time', 'Price', 'Inventory', 'Views']

writer = csv.DictWriter(f, field_names_en)
           #writer = csv.writer(fp)
           #writer.writerow(field_names)
writer.writeheader()
def get_href(url):
         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
         resp=requests.get(url, headers=headers)
         resp.encoding = 'utf-8-sig'
         soup = BeautifulSoup(resp.text, "lxml")
         tag_table = soup.find(attrs={"id":"wrapper"})
         #span_tag = soup.find_all("span", class_="pageFirst")
         #for span_tag_text in span_tag:
             #span_tag_text = span_tag_text.text #頁數
         #print('總共頁數='+str(span_tag_text)+'請在右方輸入你要查詢到第幾頁=> ')
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
                 record_dict['Seller_credit'] = splitlines_text[0].strip()
                 record_dict['Seller_Service']  = splitlines_text[2].strip()
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
y = input('請你在右方輸入你要查詢到第幾頁=> ')
y = int(y)
aaaaa=y+1                    
for page in range(1,aaaaa):
    nextpage = 'https://www.8591.com.tw/mobileGame-list.html?searchGame=27938&searchServer=&searchType=&searchKey=&firstRow=' + str(a)
    a=a+40
    url = nextpage
    get_href(url = url)
    time.sleep(3) #防止被鎖IP ，已經被鎖一次
f.close()
# 建立資料庫連接
#db = pymysql.connect("120.108.115.115", "root", "", "mybooks", charset="utf8")
db = pymysql.connect("localhost", "root", "11111111", "DB_108021011", charset="utf8mb4")
cursor = db.cursor()  # 建立cursor物件
# 執行SQL指令SELECT
cursor.execute("SELECT Server,Mobile_Phone_System, count(*) FROM `Table_108021011` group by Server,Mobile_Phone_System")

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
plt.savefig("Bar Graph",   # 儲存圖檔
            bbox_inches='tight',               # 去除座標軸占用的空間
            dpi=500)                    # dpi=像素
plt.show()
plt.close()


#圓餅圖
dff_groupy =dff.groupby('伺服器',as_index=False).sum()
print(dff_groupy)  
#cccc= aaaa.rest_index(inplace=True)
#print(dff_groupy['伺服器'])
explode=( 0,0,0,0.1)
plt.pie(dff_groupy['總數'],labels=dff_groupy['伺服器'],autopct='%1.1f%%',explode=explode)
plt.rc('font', family='SimHei', size=13)
plt.title("伺服器比較")
plt.savefig("pie",   # 儲存圖檔
            bbox_inches='tight',               # 去除座標軸占用的空間
             dpi=500)                    # dpi=像素
plt.show()
plt.close()

#折線圖
plt.plot(x1,y2,'s-',color = 'r', label=y1[0])
plt.plot(x1[4:], y2[4:],'o-',color = 'g', label=y1[4])
plt.rc('font', family='SimHei', size=13)
plt.title("伺服器的系統比較", x=0.5, y=1.03)
# 设置刻度字体大小
# 標示x軸(labelpad代表與圖片的距離)
plt.xlabel("伺服器", labelpad = 15)
# 標示y軸(labelpad代表與圖片的距離)
plt.ylabel("total", labelpad = 20)
# 顯示出線條標記位置
plt.legend(loc = "best")
# 畫出圖片
plt.savefig("Line Graph",   # 儲存圖檔
            bbox_inches='tight',               # 去除座標軸占用的空間
             dpi=500)                    # dpi=像素
plt.show()
plt.close()

#散步圖
plt.scatter(x1, y2,label=y1[0])           #繪製第一組資料          
plt.scatter(x1[4:], y2[4:],label=y1[4])   #繪製第二組資料
plt.rc('font', family='SimHei', size=13)
plt.title("伺服器的系統比較", y=1.05)    #設定圖名
plt.xlabel("伺服器", labelpad = 15)               #設定X軸名稱
plt.ylabel("總數", labelpad = 20)               #設定Y軸名稱
plt.legend()
plt.savefig("scatter diagram",   # 儲存圖檔
            bbox_inches='tight',               # 去除座標軸占用的空間
             dpi=500)                    # dpi=像素
plt.show()                    #呈現所繪圖表
plt.close()
#融合一起的長方圖
plt.rc('font', family='SimHei', size=13) #中文顯示參考這篇 https://zhuanlan.zhihu.com/p/55404865  
plt.bar(x1, y2, width=-0.355, label=y1[0])
plt.bar(x1[4:], y2[4:],  width=0.355, label=y1[4])
plt.xlabel("伺服器名稱", labelpad = 15)
plt.ylabel("總數", labelpad = 20)
plt.title('伺服器的系統比較', y=1.05)
for a,b in zip(x1,y2):
    plt.text(a,b, b,ha='center', va='bottom', fontsize=20)
plt.legend()
plt.savefig("Bar Graph 2",   # 儲存圖檔
            bbox_inches='tight',               # 去除座標軸占用的空間
             dpi=500)                    # dpi=像素
plt.show()
plt.close()

#橫條圖
y_pos = np.arange(len(x1))
plt.rc('font', family='SimHei', size=13) #中文顯示參考這篇 https://zhuanlan.zhihu.com/p/55404865  
plt.barh(dff_groupy['伺服器'],dff_groupy['總數'], align = "center")
#plt.barh( y_pos,y2[4:], label=y1[4], align = "center")
plt.xlabel("伺服器名稱", labelpad = 15)
plt.ylabel("總數", labelpad = 20)
plt.title('伺服器比較', y=1.05)
for a,b in zip(dff_groupy['伺服器'],dff_groupy['總數']):
    plt.text(b,a,b,ha='center', va='bottom', fontsize=20)
plt.savefig("Bar Graph 3",   # 儲存圖檔
            bbox_inches='tight',               # 去除座標軸占用的空間
             dpi=500)                    # dpi=像素    
plt.show()
plt.close()