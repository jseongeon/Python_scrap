import pandas as pd
from playwright.sync_api import sync_playwright
import time
import re
import os

# 엑셀 파일로 저장할 데이터 리스트
data = []

# Playwright 사용하여 네이버 블로그 스크래핑
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 디버깅을 위해 headless=False로 설정
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    # 페이지 열기
    page = context.new_page()
    blog_url = "https://blog.naver.com/urimpatent"  # 블로그 URL
    page.goto(blog_url)
    print("블로그 페이지에 접속했습니다.")

    # iframe 로드 대기 및 접근
    try:
        page.wait_for_selector("iframe#mainFrame", timeout=20000)  # 대기 시간을 20초로 증가
        iframe = page.frame(name="mainFrame")  # iframe의 이름을 사용하여 접근
        print("iframe에 접근했습니다.")
    except Exception as e:
        print(f"iframe 로드에 실패했습니다: {e}")
        browser.close()
        exit()

    # '특허정보창고' 카테고리로 이동
    try:
        category_elements = iframe.query_selector_all("a")
        for category in category_elements:
            category_text = category.inner_text().strip()

            if category_text == "특허정보창고":
                category.click()
                time.sleep(5)  # 페이지 로드 대기
                print(f"특허정보창고 카테고리로 이동했습니다.")
                break
        else:
            raise Exception("특허정보창고 카테고리를 찾을 수 없습니다.")
    except Exception as e:
        print(f"카테고리 이동에 실패했습니다: {e}")
        browser.close()
        exit()

    # 페이지 반복적으로 이동하며 게시글 수집 (페이지 번호 클릭 방식)
    current_page = 1  # 현재 페이지 번호 추적

    while True:
        # 포스팅 목록 스크래핑
        try:
            posts = iframe.query_selector_all(".blog2_list.blog2_categorylist tbody tr")  # 게시글 목록이 포함된 tbody의 tr
            print(f"포스팅을 찾았습니다. 포스팅 수: {len(posts)}")

            # 모든 포스트에서 제목과 날짜 추출
            for post in posts:
                try:
                    # 제목 요소와 날짜 요소 찾기
                    title_element = post.query_selector(".title a")  # 제목이 포함된 요소 접근
                    date_element = post.query_selector(".date")  # 날짜 요소 접근
                    
                    if title_element:
                        title = title_element.inner_text().strip()
                    else:
                        title = None

                    if date_element:
                        date = date_element.inner_text().strip()
                    else:
                        date = None

                    # 결과 출력 및 데이터 수집 여부 확인
                    if title and date:
                        if '2024' in date:
                            data.append([title, date])
                            print(f"포스트를 추가했습니다: {title} - {date}")
                    else:
                        print("제목이나 날짜 요소를 찾지 못했습니다.")
                except Exception as e:
                    print(f"포스트 접근 실패: {e}")
        except Exception as e:
            print(f"포스팅 로드에 실패했습니다: {e}")
            browser.close()
            exit()

        # 다음 페이지로 이동 (페이지 번호 클릭)
        try:
            pagination = iframe.locator("div.blog2_paginate")
            if pagination:
                # 다음 페이지 번호 버튼 찾기
                next_page_button = pagination.locator(f"a.page:has-text('{current_page + 1}')")
                
                if next_page_button.count() > 0:
                    next_page_button.click()
                    time.sleep(5)  # 페이지 로드 대기
                    current_page += 1  # 페이지 번호 증가
                    print(f"{current_page} 페이지로 이동합니다.")
                else:
                    print("다음 페이지를 찾지 못했습니다. 마지막 페이지입니다.")
                    break
            else:
                print("페이지네이션 요소를 찾지 못했습니다.")
                break
        except Exception as e:
            print(f"페이지 이동 실패: {e}")
            break

    # 브라우저 종료
    browser.close()

# 데이터프레임으로 변환 및 엑셀 파일로 저장
if data:
    df = pd.DataFrame(data, columns=["제목", "발행 날짜"])
    save_path = "C:/temp/naver_blog_posts_2024.xlsx"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 디렉토리 생성
    df.to_excel(save_path, index=False)
    print(f"스크래핑 완료 및 엑셀 저장 완료: {save_path}")
else:
    print("스크래핑된 데이터가 없습니다.")
