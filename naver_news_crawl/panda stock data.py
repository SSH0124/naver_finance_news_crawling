import pandas as pd
import FinanceDataReader as fdr

def load_allstock_KRX_fdr():
    df_krx = fdr.StockListing("KRX")
    df_krx = df_krx[['Code', 'Name', 'MarketId']]
    return df_krx

def add_zero_prefix(df):
    # 종목 코드 앞에 0을 추가
    df['Code'] = df['Code'].astype(str).apply(lambda x: x.zfill(6))
    return df

# 함수 호출하여 데이터프레임을 가져옴
stock_data = load_allstock_KRX_fdr()

# 종목 코드에 0 추가
stock_data = add_zero_prefix(stock_data)

# 한글 인코딩을 UTF-8로 설정하여 CSV 파일로 저장하고 첫 번째 열에 종목코드를 넣기
stock_data.to_csv('stock_data_fdr.csv', index=False, encoding='utf-8-sig')
print("CSV 파일이 생성되었습니다.")
