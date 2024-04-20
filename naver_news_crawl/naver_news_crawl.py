import pandas as pd
import requests
from bs4 import BeautifulSoup

def load_stock_codes(filename):
    # CSV 파일에서 종목 코드를 읽어와서 DataFrame으로 반환
    stock_data = pd.read_csv(filename)
    return stock_data[['Code', 'Name']]

def get_news_links(stock_code, stock_name):
    # 주어진 종목코드에 해당하는 네이버 금융 뉴스 페이지 URL
    url = f"https://finance.naver.com/item/news_news.nhn?code={stock_code}"
    
    # HTTP GET 요청으로 HTML 페이지 가져오기
    response = requests.get(url)
    
    # 응답이 성공적이면 HTML을 파싱
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 뉴스 링크를 담을 리스트
        news_links = []
        # 뉴스 링크가 있는 tr 태그들을 찾아서 리스트에 추가
        for tr_tag in soup.find_all('tr', class_='first'):
            a_tag = tr_tag.find('a', class_='tit')
            date_tag = tr_tag.find('td', class_='date')
            if a_tag:
                news_title = a_tag.text.strip()  # 뉴스 제목
                news_url = a_tag['href']  # 뉴스 링크
                news_date = date_tag.text.strip()  # 뉴스 게시일
                news_links.append({'title': news_title, 'url': news_url, 'date': news_date})
        return news_links
    else:
        print("HTTP 요청 실패:", response.status_code)
        return None

def save_news_links(filename, news_links, stock_code, stock_name):
    # 뉴스 링크를 'naver_news.txt' 파일에 저장
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"종목코드: {stock_code} ({stock_name})\n\n")
        for link in news_links:
            f.write(f"제목: {link['title']}\n")
            f.write(f"URL: {link['url']}\n")
            f.write(f"게시일: {link['date']}\n\n")

if __name__ == "__main__":
    # CSV 파일에서 종목 코드 및 종목명을 로드
    stock_data = load_stock_codes('stock_data_fdr.csv')
    
    # 종목별로 뉴스 링크 가져와서 'naver_news.txt' 파일에 저장
    for index, row in stock_data.iterrows():
        stock_code = row['Code']
        stock_name = row['Name']
        print(f"종목코드: {stock_code} ({stock_name})")
        news_links = get_news_links(stock_code, stock_name)
        if news_links:
            save_news_links('naver_news.txt', news_links, stock_code, stock_name)
            print(f"{stock_code} 종목의 뉴스를 저장했습니다.")
        else:
            print(f"{stock_code} 종목의 뉴스가 없습니다.")
