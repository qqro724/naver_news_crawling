# # -*- coding: utf-8 -*-
# from bs4 import BeautifulSoup
# import requests
# import re
# import datetime
# from tqdm import tqdm
# import time
# import sys
# import pandas as pd

# # ConnectionError 방지를 위한 헤더
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
#     # 필요에 따라 추가 헤더를 여기에 포함시킬 수 있습니다.
# }

# # 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
# # 입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
# def makePgNum(num):
#     if num == 1:
#         return num
#     elif num == 0:
#         return num + 1
#     else:
#         return num + 9 * (num - 1)

# # 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
# def makeUrl(search, start_pg, end_pg):
#     if start_pg == end_pg:
#         start_page = makePgNum(start_pg)
#         url = "https://search.naver.com/search.naver?where=news&query=" + search + "&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2023.07.20&de=2023.08.30&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20230720to20230830&is_sug_officeid=0&office_category=0&service_area=0&start=" + str(start_page)
#         return url
#     else:
#         urls = []
#         for i in range(start_pg, end_pg + 1):
#             page = makePgNum(i)
#             url = "https://search.naver.com/search.naver?where=news&query=" + search + "&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2023.07.20&de=2023.08.30&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20230720to20230830&is_sug_officeid=0&office_category=0&service_area=0&start=" + str(page)
#             urls.append(url)
#         return urls

# # html에서 원하는 속성 추출하는 함수 만들기 (기사, 추출하려는 속성값)
# def news_attrs_crawler(articles, attrs):
#     attrs_content = []
#     for i in articles:
#         attrs_content.append(i.attrs[attrs])
#     return attrs_content

# # html생성해서 기사크롤링하는 함수 만들기(url): 링크를 반환
# def articles_crawler(url):
#     original_html = requests.get(url, headers=headers)
#     html = BeautifulSoup(original_html.text, "html.parser")
#     url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
#     url = news_attrs_crawler(url_naver, 'href')
#     return url

# # 검색어 입력
# search = input("검색할 키워드를 입력해주세요:")
# # 검색 시작할 페이지 입력
# page = int(input("\n크롤링할 시작 페이지를 입력해주세요. ex)1(숫자만입력):"))  
# print("\n크롤링할 시작 페이지: ", page, "페이지")
# # 검색 종료할 페이지 입력
# page2 = int(input("\n크롤링할 종료 페이지를 입력해주세요. ex)1(숫자만입력):")) 
# print("\n크롤링할 종료 페이지: ", page2, "페이지")

# # naver url 생성
# url = makeUrl(search, page, page2)

# # 뉴스 크롤러 실행
# news_url = []
# for i in url:
#     url = articles_crawler(i)
#     news_url.append(url)
#     time.sleep(2)

# # 제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
# def makeList(newlist, content):
#     for i in content:
#         for j in i:
#             newlist.append(j)
#     return newlist

# # 제목, 링크, 내용 담을 리스트 생성
# news_url_1 = []

# # 1차원 리스트로 만들기(내용 제외)
# makeList(news_url_1, news_url)

# # NAVER 뉴스만 남기기
# final_urls = []
# for i in tqdm(range(len(news_url_1))):
#     if "news.naver.com" in news_url_1[i]:
#         final_urls.append(news_url_1[i])
#     elif "n.news.naver.com"in news_url_1[i]:
#         final_urls.append(news_url_1[i])
#     else:
#         pass


# # 뉴스 내용 크롤링 및 데이터 정제
# news_companies = []
# news_titles = []
# news_contents = []
# news_dates = []

# for i in tqdm(final_urls):
#     # 각 기사 html get하기
#     news = requests.get(i, headers=headers)
#     news_html = BeautifulSoup(news.text, "html.parser")

#     # 언론사 이름 가져오기
#     html_company = news_html.select_one(
#         "#ct > div.media_end_head.go_trans > div.media_end_head_top > a.media_end_head_top_logo > img")
#     if html_company:
#         company = html_company.attrs['title']

#     # 뉴스 제목 가져오기
#     title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
#     if not title:
#         title = news_html.select_one("#content > div.end_ct > div > h2")

#     # 뉴스 본문 가져오기
#     content = news_html.select("div#newsct_article")
#     if not content:
#         content = news_html.select("#newsct_article _article_body")

#     # 기사 텍스트만 가져오기
#     # list합치기
#     content = ''.join(str(content))

#     # html태그제거 및 텍스트 다듬기
#     pattern1 = '<[^>]*>'
#     title = re.sub(pattern=pattern1, repl='', string=str(title))
#     content = re.sub(pattern=pattern1, repl='', string=content)
#     pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
#     content = content.replace(pattern2, '')

#     news_companies.append(company)
#     news_titles.append(title)
#     news_contents.append(content)

#     try:
#         html_date = news_html.select_one(
#             "div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
#         news_date = html_date.attrs['data-date-time']
#     except AttributeError:
#         news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
#         news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))
#     # 날짜 가져오기
#     news_dates.append(news_date)
#     time.sleep(2)

# print("검색된 기사 갯수: 총 ", (page2 + 1 - page) * 10, '개')

# # 데이터 프레임 만들기
# news_df = pd.DataFrame(
#     {'date': news_dates, 'title': news_titles, 'company': news_companies, 'link': final_urls, 'content': news_contents})

# # 중복 행 지우기
# news_df = news_df.drop_duplicates(subset='link', keep='first', ignore_index=True)
# print("중복 제거 후 행 개수: ", len(news_df))

# # 데이터 프레임 저장
# now = datetime.datetime.now()
# news_df.to_csv('{}_{}.csv'.format(search, now.strftime('%Y%m%d')), encoding='utf-8-sig', index=False)

import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import time

# ConnectionError 방지를 위한 헤더
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num + 1
    else:
        return num + 9 * (num - 1)

# 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지, 시작날짜, 끝날짜)
def makeUrl(search, start_pg, end_pg, s_date, e_date):
    s_date = s_date.replace(".", "")
    e_date = e_date.replace(".", "")

    if start_pg == end_pg:
        start_page = makePgNum(start_pg)
        url = f"https://search.naver.com/search.naver?where=news&query={search}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={s_date}&de={e_date}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{s_date}to{e_date}&is_sug_officeid=0&office_category=0&service_area=0&start={start_page}"
        return url
    else:
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = makePgNum(i)
            url = f"https://search.naver.com/search.naver?where=news&query={search}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={s_date}&de={e_date}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{s_date}to{e_date}&is_sug_officeid=0&office_category=0&service_area=0&start={page}"
            urls.append(url)
        return urls

# html에서 원하는 속성 추출하는 함수 만들기 (기사, 추출하려는 속성값)
def news_attrs_crawler(articles, attrs):
    attrs_content = []
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

# html생성해서 기사크롤링하는 함수 만들기(url): 링크를 반환
def articles_crawler(url):
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    url = news_attrs_crawler(url_naver, 'href')
    return url

def crawler(maxpage, query, sort, s_date, e_date):
    start_page = 1
    end_page = int(maxpage)

    # naver url 생성
    urls = makeUrl(query, start_page, end_page, s_date, e_date)

    # 뉴스 크롤러 실행
    news_url = []
    for url in urls:
        links = articles_crawler(url)
        news_url.extend(links)
        time.sleep(2)

    # 정규표현식을 사용하여 네이버 뉴스 링크만 남기기
    naver_news_urls = []
    for link in news_url:
        if re.search(r"(news\.naver\.com|n\.news\.naver\.com)", link):
            naver_news_urls.append(link)

    # 중복 제거
    naver_news_urls = list(set(naver_news_urls))

    print("검색된 기사 갯수: 총", len(naver_news_urls), "개")

    # 뉴스 내용 크롤링 및 데이터 정제
    news_companies = []
    news_titles = []
    news_contents = []
    news_dates = []

    for url in naver_news_urls:
        news = requests.get(url, headers=headers)
        news_html = BeautifulSoup(news.text, "html.parser")

        company = news_html.select_one("#main_content > div.article_header > div.press_logo > a > img")
        if company:
            company = company.attrs['title']

        title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if not title:
            title = news_html.select_one("#content > div.end_ct > div > h2")

        content = news_html.select_one("div#newsct_article")
        if not content:
            content = news_html.select("#newsct_article _article_body")

        content = ''.join(str(content))

        pattern1 = '<[^>]*>'
        title = re.sub(pattern=pattern1, repl='', string=str(title))
        content = re.sub(pattern=pattern1, repl='', string=content)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '')
        content = content.replace('&apos;', "'").replace('&quot;', '"').replace('&nbsp;', ' ')

        news_companies.append(company)
        news_titles.append(title)
        news_contents.append(content)

        # 날짜 가져오기
        try:
            html_date = news_html.select_one("div#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            if html_date:
                news_date = html_date.attrs['data-date-time']
            else:
                news_date = ""
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            if news_date:
                news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))
            else:
                news_date = ""

        news_dates.append(news_date)
        time.sleep(2)

    print("총 크롤링된 기사 개수:", len(news_titles))

    # 데이터 프레임 만들기
    if len(news_titles) == len(news_companies) == len(news_dates) == len(naver_news_urls) == len(news_contents):
        news_df = pd.DataFrame({
            'date': news_dates,
            'title': news_titles,
            'company': news_companies,
            'link': naver_news_urls,
            'content': news_contents
        })

        # 중복 행 제거
        news_df = news_df.drop_duplicates(subset='link', keep='first', ignore_index=True)
        print("중복 제거 후 기사 개수:", len(news_df))

        # CSV 파일로 저장
        now = datetime.datetime.now()
        file_name = f"{query}_news_{now.strftime('%Y%m%d%H%M%S')}.csv"
        news_df.to_csv(file_name, encoding='utf-8-sig', index=False)
        print("데이터를 저장했습니다:", file_name)
    else:
        print("데이터의 길이가 맞지 않습니다. 프로그램을 종료합니다.")

def main():
    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    
    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")  
    query = input("검색어 입력: ")  
    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")    #관련도순=0  최신순=1  오래된순=2
    s_date = input("시작날짜 입력(yyyy.mm.dd): ")  #yyyy.mm.dd
    e_date = input("끝날짜 입력(yyyy.mm.dd): ")   #yyyy.mm.dd
    
    crawler(maxpage, query, sort, s_date, e_date) 

main()

