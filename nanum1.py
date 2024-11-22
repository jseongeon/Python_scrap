import pandas as pd
from playwright.sync_api import sync_playwright
import time
import os

# 엑셀 파일로 저장할 데이터 리스트
data = []

try:
    # Playwright 사용하여 네이버 블로그 스크래핑
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 디버깅을 위해 headless=False로 설정
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        # 페이지 열기
        page = context.new_page()
        blog_url = "https://blog.naver.com/kazena"  # 블로그 URL
        page.goto(blog_url)
        print("블로그 페이지에 접속했습니다.")
        
        # iframe 로드 대기 및 접근
        try:
            page.wait_for_selector("iframe#mainFrame", timeout=20000)  # 대기 시간을 20초로 증가
            iframe = page.frame(name="mainFrame")  # iframe의 이름을 사용하여 접근
            print("iframe에 접근했습니다.")
        except Exception as e:
            print(f"iframe 로드에 실패했습니다: {e}")
            raise e

        # 좌측 카테고리에서 '전체보기' 클릭
        try:
            # "전체보기" 버튼의 id를 사용하여 선택
            all_posts_button_selector = "#category0"  # '전체보기' 버튼 선택자
            iframe.wait_for_selector(all_posts_button_selector, timeout=10000)  # 10초 대기
            all_posts_button = iframe.query_selector(all_posts_button_selector)
            if all_posts_button:
                all_posts_button.click()
                time.sleep(5)  # 페이지가 로드될 시간을 주기 위해 대기
                print("'전체보기' 버튼을 클릭했습니다.")
            else:
                print("'전체보기' 버튼을 찾지 못했습니다.")
        except Exception as e:
            print(f"'전체보기' 버튼 클릭에 실패했습니다: {e}")
            raise e

        # 게시글 수집
        current_page = 1
        max_page_reached = False

        while not max_page_reached:
            try:
                # 게시글 제목과 날짜를 포함하는 tr 요소들 접근
                iframe.wait_for_selector("table.blog2_list.blog2_categorylist tbody tr", timeout=10000)  # 10초 대기
                rows = iframe.query_selector_all("table.blog2_list.blog2_categorylist tbody tr")
                if rows:
                    print(f"포스팅을 찾았습니다. 포스팅 수: {len(rows)}")
                    
                    # 각 행에서 제목과 날짜 추출
                    for row in rows:
                        try:
                            title_element = row.query_selector("td.title a.pcol2")
                            date_element = row.query_selector("td.date span.date.pcol2")

                            if title_element and date_element:
                                title = title_element.inner_text().strip()
                                date = date_element.inner_text().strip()

                                # 2024년 작성된 포스트만 추가
                                if title and date and '2024' in date:
                                    data.append([title, date])
                                    print(f"포스트를 추가했습니다: {title} - {date}")
                            else:
                                print("제목이나 날짜 요소를 찾지 못했습니다.")
                        except Exception as e:
                            print(f"행 접근 실패: {e}")
                else:
                    print("게시글을 찾을 수 없습니다.")

            except Exception as e:
                print(f"포스팅 로드에 실패했습니다: {e}")
                break

            # 다음 페이지로 이동
            try:
                # 페이지 번호 버튼 찾기
                pagination = iframe.query_selector("div.blog2_paginate")
                if pagination:
                    # 페이지 번호 버튼을 텍스트 기반으로 찾아서 클릭합니다.
                    next_page_button = pagination.query_selector(f"a.page:has-text('{current_page + 1}')")
                    
                    if next_page_button:
                        next_page_button.click()
                        time.sleep(5)  # 페이지 로드 대기
                        current_page += 1
                        print(f"{current_page} 페이지로 이동합니다.")
                    else:
                        # '다음' 버튼이 존재하는지 확인 후 클릭
                        next_button = pagination.query_selector("a.next.pcol2._goPageTop")
                        if next_button:
                            next_button.click()
                            time.sleep(5)  # 페이지 로드 대기
                            current_page += 1
                            print(f"다음 버튼을 클릭하여 {current_page} 페이지로 이동합니다.")
                        else:
                            print("다음 페이지 버튼을 찾지 못했습니다. 마지막 페이지입니다.")
                            max_page_reached = True
                else:
                    print("페이지네이션 요소를 찾지 못했습니다. 마지막 페이지입니다.")
                    max_page_reached = True

            except Exception as e:
                print(f"페이지 이동 실패: {e}")
                max_page_reached = True

finally:
    try:
        # 브라우저 종료
        if browser:
            browser.close()
    except Exception as e:
        print(f"브라우저 종료 중 오류 발생: {e}")

# 데이터프레임으로 변환 및 엑셀 파일로 저장
if data:
    df = pd.DataFrame(data, columns=["제목", "발행 날짜"])
    save_path = "C:/temp/naver_blog_posts_2024.xlsx"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 디렉토리 생성
    df.to_excel(save_path, index=False)
    print(f"스크래핑 완료 및 엑셀 저장 완료: {save_path}")
else:
    print("스크래핑된 데이터가 없습니다.")
