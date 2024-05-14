from datetime import datetime
import csv
import time
from multiprocessing import Pool
import requests

from lxml import etree
from finviz.helper_functions.request_functions import http_request_get

STOCK_URL = "https://finviz.com/quote.ashx"
NEWS_URL = "https://finviz.com/news.ashx"
STOCK_PAGE = {}

def get_page(ticker):
    global STOCK_PAGE
    if ticker not in STOCK_PAGE:
        STOCK_PAGE[ticker], _ = http_request_get(url=STOCK_URL, payload={"t": ticker}, parse=True)

def get_news(ticker):
    try:
        get_page(ticker)
    except requests.exceptions.HTTPError as e:
        print(f"심볼 {ticker}에 대한 데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return []

    page_parsed = STOCK_PAGE[ticker]
    news_table = page_parsed.cssselect('table[id="news-table"]')
    if not news_table:
        return []

    rows = news_table[0].xpath("./tr[not(@id)]")
    results = []
    for row in rows:
        raw_timestamp = row.xpath("./td")[0].xpath("text()")[0].strip()

        headline_elem = row.xpath("./td")[1].cssselect('a[class="tab-link-news"]')
        headline = headline_elem[0].text.strip() if headline_elem else "제목 없음"

        url_elem = row.xpath("./td")[1].cssselect('a[class="tab-link-news"]')
        url = url_elem[0].get("href") if url_elem else "URL 없음"

        results.append((raw_timestamp, headline, url))

    return results

def get_latest_news(symbol):
    news = get_news(symbol)
    if news:
        return news[0]
    else:
        return None

def crawl_symbol_news(symbol):
    start_time = time.time()
    latest_news = get_latest_news(symbol)
    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n{symbol}의 최신 뉴스:")
    if latest_news:
        timestamp, headline, url = latest_news
        print(f"타임스탬프: {timestamp}")
        print(f"제목: {headline}")
        print(f"URL: {url}")
        with open('Stock_news.txt', 'a', encoding='utf-8') as stock_news_file:
                stock_news_file.write(f"{symbol}\n{timestamp}\n{headline}\n{url}\n\n")
        if "Today" in timestamp:
            with open('Today.txt', 'a', encoding='utf-8') as today_file:
                today_file.write(f"{symbol}\n{timestamp}\n{headline}\n{url}\n\n")
            # Stock_news.txt에 추가 저장
           
    else:
        print("뉴스를 찾을 수 없습니다.")

    return total_time

def main():
    csv_file = 'mini_stock.csv'
    symbols = []

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 행 건너뛰기
        for line_count, row in enumerate(reader, start=1):
            if line_count <= 4118:
                symbols.append(row[0])
            else:
                break

    while True:
        total_time_list = []
        # 멀티 프로세싱 풀 3개 생성
        with Pool(processes=2) as pool:
            # 각 주식 심볼을 병렬로 처리
            total_time_list = pool.map(crawl_symbol_news, symbols)

        total_time = sum(total_time_list)

        print(f"\n총 크롤링된 뉴스 수: {len(total_time_list)}")
        print(f"크롤링에 소요된 총 시간: {total_time} 초")

        # 다음 반복을 시작하기 전에 60초 동안 대기
        time.sleep(60)

if __name__ == "__main__":
    main()
