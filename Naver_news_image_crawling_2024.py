import pandas as pd
from selenium import webdriver
import os
import urllib.request
import re
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# CSV 파일 경로
csv_file_path = r"C:\Users\SAMSUNG\Documents\Crawling_2\BTS-20240305T021108Z-001\BTS\2023\방탄소년단_news.csv"

# 이미지를 저장할 폴더 경로
save_folder = r"C:\Users\SAMSUNG\Documents\Crawling_2\BTS-20240305T021108Z-001\BTS\2023\image"

# 폴더가 없는 경우 생성
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 웹 드라이버 초기화
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 화면없이 실행
driver = webdriver.Chrome(options=chrome_options)

# CSV 파일 읽어오기
df = pd.read_csv(csv_file_path)

# CSV 파일에서 링크 열 선택
urls = df['link']

for url in urls:
    try:
        # 기사 페이지 가져오기
        driver.get(url)

        # 이미지 찾기
        img_elements = driver.find_elements(By.CSS_SELECTOR, 'span.end_photo_org img')

        # 이미지 저장
        for img_tag in img_elements:
            src = img_tag.get_attribute('src')
            if src:
                # 파일명에서 확장자 추출
                file_extension = src.split('.')[-1].split('?')[0]  # 파일 형식 추출 및 ?type=w647 제거
                # 파일명 생성
                filename = f"{url.split('/')[-1]}_{img_elements.index(img_tag):03d}.{file_extension}"
                # 파일명에서 유효하지 않은 문자 제거
                filename = re.sub(r'[^\w\-_.]', '', filename)
                save_path = os.path.join(save_folder, filename)
                urllib.request.urlretrieve(src, save_path)
    except Exception as e:
        print(f"오류 발생: {e}")

print("이미지 크롤링 및 저장이 완료되었습니다.")

# 웹 드라이버 종료
driver.quit()
