import pandas as pd

def find_related_info(keyword):
    df = pd.read_excel('stock_data.xlsx', header=None)
    related_info = df[(df.iloc[:, 0].str.contains(keyword, case=False)) | (df.iloc[:, 1].str.contains(keyword, case=False))]
    return related_info

def main():
    while True:
        keyword = input("찾고자 하는 종목명 또는 테마를 입력하세요 (exit로 종료): ")
        
        if keyword.lower() == 'exit':
            print("프로그램을 종료합니다.")
            break
        
        related_info = find_related_info(keyword)

        if not related_info.empty:
            themes = set()  # 중복된 테마를 제거하기 위해 set을 사용합니다.
            print(f"\n'{keyword}'와(과) 관련된 정보:")
            for index, row in related_info.iterrows():
                print(f"종목명: {row.iloc[1]}, 테마: {row.iloc[0]}")
                themes.add(row.iloc[0])  # 테마를 themes에 추가합니다.
            
            print("\n모아진 테마:")
            for theme in themes:
                print(theme)
        else:
            print(f"'{keyword}'와(과) 관련된 정보를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
