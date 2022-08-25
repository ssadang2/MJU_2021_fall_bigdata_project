from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

#네이버 영화 DB와 IMDB Searching engine/DB를 이용한 영화 데이터 크롤링

browser = webdriver.Chrome('C:/chromedriver.exe')
browser.get('https://movie.naver.com/movie/sdb/browsing/bmovie.naver?nation=US')
browser.implicitly_wait(10)

browser.execute_script('window.open("about:blank", "_blank");')
browser.switch_to.window(browser.window_handles[1])

browser.get('https://www.imdb.com/?ref_=nv_home')
browser.implicitly_wait(10)
browser.switch_to.window(browser.window_handles[0])
# 네이버 영화 페이지와 IMDB 2개의 tab이 필요하기 때문에 2개의 tab을 켜준다.

f = open(r"C:\Users\WIN10\MJU_Study\Bigdata\2021_fall_project\movies_with_naver_and_IMDB.csv", 'w', encoding='UTF-8', newline='')
csvWriter = csv.writer(f)
# 데이터 저장을 위한 csv writer 모듈을 사용한다.

while True:
    try:
        for i in range(1, 21):
            # 한 페이지에 데이터가 20개이므로, 20번 돈다.
            try:
                browser.find_element_by_css_selector('#old_content > ul > li:nth-child({}) > a'.format(i)).click()
                time.sleep(1)
                # 영화를 클릭한다.
            except:
                browser.find_element_by_css_selector('#old_content > ul > li:nth-child({}) > a'.format(i)).send_keys(Keys.ENTER)
                time.sleep(1)
                # 짧은 영화 제목이 브라우저의 크기에 가려져서 css selector 클릭을 못하는 겨우가 생겨서 해당 상황 발생 시 send_keys 메소드로 해결
            try:    
                eng_title = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > strong').text
            except:
                browser.back()
                if i == 20:
                    browser.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
                    time.sleep(1)
                continue
            # 한글 제목 옆에 영어 제목이 없는 경우 IMDB에서 별점 검색을 할 수 없으므로 스킵한다.
            # 그리고 그 데이터가 20번째였다면 다음 페이지로 넘어간다.

            if eng_title.isdigit():
                eng_title = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text + ", " + eng_title
            # 가끔 영어 제목 자체로 수입한 경우, 한글 제목에 영어 제목을 넣고, 영어 제목 칸에 개봉 년도를 넣어 놔서 해당 부분 의도한 대로(영어 제목, 개봉 년도) 수정

            title = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
            # title에 한글 영화 제목을 넣는다
            genre = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a:nth-child(1)').text
            if genre == "미국":
                genre = "장르 정보 없음"
            # genre 칸에 가끔 미국 혹은 미국, 캐나다 이런 식으로 적혀 있는 영화가 있는데 해당 데이터는 장르가 없다고 넣어준다.

            try:
                running_time = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)').text
            except:
                running_time = "상영 시간 정보 없음"
            
            # 상영 시간 정보를 긁어 오고 없으면 상영 시간 정보 없음을 넣어준다.

            try:
                screening_rat = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a').text
            except:
                try:
                    screening_rat = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a:nth-child(1)').text
                except:
                    screening_rat = "상영등급 정보 없음"
                
            # 상영 등급의 위치가 데이터마다 약간 상이하거나 없는 경우가 있으므로, 모든 상황에 대한 분기점을 제공해 준다.

            try:
                director = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a').text
            except:
                browser.back()
                if i == 20:
                    browser.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
                    time.sleep(1)
                continue
            # 감독 이름을 긁어오고 감독이 없다면 해당 data는 스킵한다 혹시 20번째 데이터라면 다음 페이지로 넘어간다.

            browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a').click()
            time.sleep(1)

            try:
                dir_all_movie_num = browser.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst .count > em').text + "개"
            except:
                browser.back()
                browser.back()
                if i == 20:
                    browser.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
                    time.sleep(1)
                continue
            # 감독 연출작 개수를 긁어오고 연출작 개수를 긁어올 수 없다면 해당 데이터는 skip한다 혹시 20번째 데이터라면 다음 페이지로 넘어간다.

            browser.back()

            try:
                browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p > a:nth-child(1)').click()
                time.sleep(1)
                try:
                    actor_all_movie_num = browser.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst .count > em').text + "개"
                    browser.back()
                    browser.back()
                except:
                    actor_all_movie_num = "연기자 없음"
                    browser.back()
                    browser.back()
            except:
                try:
                    browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p > a').click()
                    time.sleep(1)
                    try:
                        actor_all_movie_num = browser.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst .count > em').text + "개"
                        browser.back()
                        browser.back()
                    except:
                        actor_all_movie_num = "연기자 없음"
                        browser.back()
                        browser.back()
                except:
                    actor_all_movie_num = "연기자 없음"
                    browser.back()               
            
            # 연기자가 존재하는 css selector의 위치가 데이터마다 상당히 상이하므로 모든 분기점에 대한 처리를 해주었다

            browser.switch_to.window(browser.window_handles[1])
            # IMDB가 있는 tab으로 넘어간다.

            search = browser.find_element_by_css_selector('#suggestion-search')
            search.click()

            search.send_keys(eng_title)
            search.send_keys(Keys.ENTER)
            # 영화의 영어 제목을 검색한다.

            offset = -100
            for j in range(0, len(eng_title)):
                if eng_title[len(eng_title)-1 - j] == ',':
                    offset = len(eng_title)-1 - j
                    break

            if not (offset == -100):
                eng_title_without_year = eng_title[0 : offset]
            else:
                eng_title_without_year = eng_title

            # eng_title에는 개봉 년도가 있으니 개봉 년도를 제거한다.

            try:
                if not browser.find_element_by_css_selector('#main > div > div.findSection > table > tbody > tr.findResult.odd > td.result_text > a').text.lower() == eng_title_without_year.lower():
                    # 만약 영어 제목과 일치하는 영화가 없다면
                    browser.switch_to.window(browser.window_handles[0])
                    if i == 20:
                        browser.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
                        time.sleep(1)
                    continue
                    # 다시 네이버 영화 tab으로 이동하고 20번째 영화였다면 다음 페이지로 이동한다.
                browser.find_element_by_css_selector('#main > div > div.findSection > table > tbody > tr.findResult.odd > td.result_text > a').click()
                time.sleep(1)
                try:
                    browser.find_element_by_css_selector('#__next > main > div > section.ipc-page-background.ipc-page-background--base.TitlePage__StyledPageBackground-wzlr49-0.dDUGgO > section > div:nth-child(4) > section > section > div.Hero__MediaContentContainer__NoVideo-kvkd64-6.hAJqld > div.Hero__ContentContainer-kvkd64-10.eaUohq > div.Hero__MetaContainer__NoVideo-kvkd64-8.TqBgz > div.RatingBar__RatingContainer-sc-85l9wd-0.hNqCJh.Hero__HideableRatingBar-kvkd64-12.hBqmiS > div > div:nth-child(1) > a').click()
                    time.sleep(1)
                    rating = browser.find_element_by_css_selector('#main > section > div > div.subpage_title_block > div > div.ipl-rating-widget > div.ipl-rating-star > span.ipl-rating-star__rating').text
                    browser.switch_to.window(browser.window_handles[0])
                except:
                    browser.find_element_by_css_selector('#__next > main > div > section.ipc-page-background.ipc-page-background--base.TitlePage__StyledPageBackground-wzlr49-0.dDUGgO > section > div:nth-child(4) > section > section > div.Hero__MediaContentContainer__Video-kvkd64-2.kmTkgc > div.Hero__ContentContainer-kvkd64-10.eaUohq > div.Hero__MetaContainer__Video-kvkd64-4.kNqsIK > div.RatingBar__RatingContainer-sc-85l9wd-0.hNqCJh.Hero__HideableRatingBar-kvkd64-12.hBqmiS > div > div:nth-child(1) > a').click()
                    time.sleep(1)
                    rating = browser.find_element_by_css_selector('#main > section > div > div.subpage_title_block > div > div.ipl-rating-widget > div.ipl-rating-star > span.ipl-rating-star__rating').text
                    browser.switch_to.window(browser.window_handles[0])
                    # IMDB에서 영화 하나를 눌렀을 때, 해당 페이지에 자동 재생되는 예고편이 있느냐 아니면 정적인 이미지밖에 없느냐에 따라 별점의 css selector가 달라진다. 그에 대한 처리를 해주어야 한다.
            except:
                rating = "별점 없음"
                browser.back()
                browser.switch_to.window(browser.window_handles[0])
                if i == 20:
                    browser.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
                    time.sleep(1)
                continue
                # 만약 이 flow까지 왔다면 별점이 아예 없는 data이므로 이 data는 스팁하고 네이버로 이동한다 만약 20번째 데이터라면 다음 페이지로 간다.
            
            print(title, genre, running_time, screening_rat, director, dir_all_movie_num, actor_all_movie_num, rating)
            csvWriter.writerow([title, genre, running_time, screening_rat, director, dir_all_movie_num, actor_all_movie_num, rating])
            # 해당 데이터를 저장한다.

            if i == 20:
                browser.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
                time.sleep(1)
                # 만약 20번째 데이터라면 다음 페이지로 넘어간다.
    except:
        break

f.close()
# csv writter를 종료한다.