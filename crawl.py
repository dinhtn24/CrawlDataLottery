import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta, date


# function
def putInFile(domain, data):
    file_name = domain + "-" + date_choose
    file_path = ".\data_crawl\\" + file_name + ".csv"
    writeMode = 'w'

    with open(file_path, writeMode, encoding='utf8') as f:
        writer = csv.writer(f, skipinitialspace=True)
        writer.writerows(data)


def getXSMB():
    try:
        # open web
        browser.get(url + "/xsmb-" + date_choose + ".html")

        # find element
        table_result = browser.find_element(By.CLASS_NAME, "table-result")

        province = browser.find_element(
            By.XPATH, "/html/body/main/div/div[2]/section[1]/header/h2/a[4]").text

        # count row
        rows_table = table_result.find_elements(By.TAG_NAME, "tr")

        # crawl data
        data = []
        data_row = ["Miền Bắc", date_choose, province]
        for row_table in rows_table:
            row_prizeName = row_table.find_element(By.TAG_NAME, "th")
            row_prizeCodes = row_table.find_elements(By.TAG_NAME, "td")

            for row_prizeCode in row_prizeCodes:

                # pass fist row
                if len(row_prizeName.text) == 0:
                    continue
                data_row.append(row_prizeName.text)
                print(row_prizeName.text + ": ", end='')

                prizeCodes = row_prizeCode.find_elements(By.TAG_NAME, "span")

                for prizeCode in prizeCodes:
                    data_row.append(prizeCode.text)
                    data.append(data_row.copy())
                    print(prizeCode.text + " ", end='')
                    data_row.pop()

                data_row.pop()
                print()

        putInFile('xsmb', data)
    except:
        print("ERROR!!!NOT exist data")



def getXSMT_XSMN(domain):
    try:
        # open web
        browser.get(url + "/" + domain + "-" + date_choose + ".html")
       
        # find elements
            #get table
        table_result = browser.find_element(By.CLASS_NAME, "table-result")

            #count column table
        row_header = table_result.find_element(By.TAG_NAME, "thead")
                #get province name
        provinces = row_header.text.splitlines()[1:]

            #get body table, prize code at here
        body_tab = table_result.find_element(By.TAG_NAME, "tbody")
        rows_body = body_tab.find_elements(By.TAG_NAME, "tr")

            # crawl data
        data = []

        if domain == "xsmt" :
            data_row = ["Miền Tây", date_choose]
        else :
            data_row = ["Miền Nam", date_choose]
            
        for row in rows_body:
            prize_name = row.find_element(By.TAG_NAME, "th")
            prize_codes = row.find_elements(By.TAG_NAME, "td")
            for codes in prize_codes:
                data_row.append(provinces[prize_codes.index(codes)])
                data_row.append(prize_name.text)
                for code in codes.text.splitlines():
                    data_row.append(code)
                    data.append(data_row.copy())
                    data_row.pop()
                data_row.pop()
                data_row.pop()
        putInFile(domain, data)
    except:
        print("ERROR!!!NOT exist data")


#   Main
    #  browser
browser = webdriver.Chrome(executable_path="./chromedriver.exe")
url = "https://xoso.com.vn"

today = date.today()
date_choose = "{}-{}-{}".format(today.day, today.month, today.year)
print(date_choose)

getXSMB()
getXSMT_XSMN("xsmt")
getXSMT_XSMN("xsmn")
browser.close()