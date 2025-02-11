
# step1. Importing required packages and modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
chrome_options = webdriver.ChromeOptions()

import csv
import time
import pandas as pd
from tqdm import tqdm

# step2. Function to collect Naver news comments information
def get_naver_news_comments(wait_time=5, delay_time=0.1):
    # Connect to the specified URL using the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Waiting for the driver to find elements, maximum wait_time seconds
    driver.implicitly_wait(wait_time)

    # Download the article URL
    df = pd.read_csv(r'C:\Users\SAMSUNG\Documents\Crawling_2\BTS-20240305T021108Z-001\BTS\2022\방탄소년단_news.csv', encoding='utf-8')
    company_list = df['company'].tolist()
    url_list = df['link'].tolist()
    comment_url_list = [url.replace('article', 'article/comment') for url in url_list]

    nicknames_list_2 = []
    datetimes_list_2 = []
    contents_list = []
    url_list_2 = []
    company_list_2 = []

    for url, company in tqdm(zip(comment_url_list, company_list)):
        # . 
        time.sleep(2)
        try:
            driver.get(url)
            while True:
                try:
                    more = driver.find_element(by=By.CSS_SELECTOR, value="a.u_cbox_btn_more")
                    more.click()
                    time.sleep(delay_time)
                except:
                    break

            # Crawl comments
            nicknames = driver.find_elements(by=By.CSS_SELECTOR, value="span.u_cbox_nick")
            datetimes = driver.find_elements(by=By.CSS_SELECTOR, value="span.u_cbox_date")
            contents = driver.find_elements(by=By.CSS_SELECTOR, value="span.u_cbox_contents")

            for nickname, datetime, content in zip(nicknames, datetimes, contents):
                nicknames_list_2.append(nickname.text)
                datetimes_list_2.append(datetime.text)
                contents_list.append(content.text)
                url_list_2.append(url)
                company_list_2.append(company)
        except Exception as e:
            print(f"Error processing URL: {url}")
            print(e)
            continue

    # Save to CSV
    with open(r'C:\Users\SAMSUNG\Documents\Crawling_2\BTS-20240305T021108Z-001\BTS\2022\방탄소년단_news_comments_2022.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['작성자', '작성날짜', '언론사', '_', 'url', '댓글내용'])
        for nickname, datetime, company, url, content in tqdm(zip(nicknames_list_2, datetimes_list_2, company_list_2, url_list_2, contents_list)):
            writer.writerow([nickname, datetime, company, 0, url, content])

# Execute the function
get_naver_news_comments()
