from selenium import webdriver
import time
import csv

# 네이버 영화 DB를 이용한 영화 데이터 크롤링
browser = webdriver.Chrome('C:/chromedriver.exe')
browser.get('https://www.naver.com/')
browser.implicitly_wait(10)
# 웹 드라이버와 chrome을 연결하고 네이버 브라우저를 열고 꼬이지 않도록 잠시 대기시킨다.

browser.find_element_by_css_selector('#NM_FAVORITE > div.group_nav > a').click()
time.sleep(1)

browser.find_element_by_css_selector('#gnb > div.ly_service > div.group_service.NM_FAVORITE_ALL_LY > dl:nth-child(3) > dd:nth-child(3) > a').click()
time.sleep(1)

browser.find_element_by_css_selector('#scrollbar > div.scrollbar-box > div > div > ul > li:nth-child(3) > a').click()
time.sleep(1)

browser.find_element_by_css_selector('#old_content > div.tab_type_6 > ul > li:nth-child(3) > a > img').click()
time.sleep(1)

#네이버 영화 평점순으로 접속한다. 여기엔 약 2천개의 영화가 있다.

movies = browser.find_elements_by_css_selector('#old_content > table > tbody > tr ')

movie_cnt = 0

for movie in movies:
    try:
        title = movie.find_element_by_css_selector("td.title > div > a").text
    except:
        movie_cnt += 1
        continue
    else:
        movie_cnt += 1

# loop를 위해 page에 있는 movie data의 개수를 세는 작업이다.
# movie datas들이 table안에 있는데 table 안에는 movie_data 말고도 html의 <hr>태그와 같은 분리줄이 같이 섞여 들어온다 따라서 그 분리줄 포함 모든 moives 개수를 세어야 원활한 크롤링이 가능하다.
 
checker = 2
# 모든 row를 돌며 값을 증가시키고 마지막 row면 다음 페이지로 넘어가기 위한 checker 변수이다.

f = open(r"C:\Users\WIN10\MJU_Study\Bigdata\2021_fall_project\movies_with_naver.csv", 'w', encoding='UTF-8', newline='')
csvWriter = csv.writer(f)
# 데이터 저장을 위한 csv writer 모듈을 사용한다.

while True:
    try:
        while checker < movie_cnt + 1:
            try:
                browser.find_element_by_css_selector('#old_content > table > tbody > tr:nth-child({}) > td.title > div > a'.format(checker)).click()
                # table 안에 있는 영화 하나를 클릭한다.
            except:
                checker += 1
                # css selector를 찾지 못해서 예외가 발생하면 해당 row는 영화가 아니라 분리줄이라는 뜻으로 checker 값만 올리고 다시 loop로 돌아간다.
                continue

            try:
                browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
                # 영화 제목이 있는지 확인한다.
            except:
                browser.back()
                checker += 1
                continue
                # 없다면 수집할 수 없는 data이므로 browser를 뒤로 보내고 checker의 값을 올리고 loop로 돌아간다.

            title = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
            genre = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a:nth-child(1)').text
            running_time = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)').text
            # 영화 제목, 장르, 상영 시간을 알맞게 긁어 온다.
            try:
                screening_rat = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a').text
            except:
                try:
                    screening_rat = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a:nth-child(1)').text
                except:
                    screening_rat = "상영등급 정보 없음"
            # 영화 상영등급의 위치가 다르고 아예 상영 등급이 없는 데이터도 있으므로, 상황별 분기점을 만들어 준다.
                    
            director = browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a').text

            browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a').click()

            dir_all_movie_num = browser.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst .count > em').text + "개"

            # 감독의 이름과 감독의 연출작의 개수를 긁어 온다.

            browser.back()

            try:
                browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p > a:nth-child(1)').click()
                actor_all_movie_num = browser.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst .count > em').text + "개"
                browser.back()
                browser.back()
            except:
                try:
                    browser.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p > a').click()
                    actor_all_movie_num = browser.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst .count > em').text + "개"
                    browser.back()
                    browser.back()
                except:
                    actor_all_movie_num = "연기자 없음"
                    browser.back()
                    browser.back()
            # 주연의 출연작 개수의 css selector 위치가 데이터마다 다르고 아예 주연의 정보가 없는 데이터도 있으므로, 상황별 분기점을 만들어 준다.

            try:
                rating = browser.find_element_by_css_selector('#old_content > table > tbody > tr:nth-child({}) > td.point'.format(checker)).text
            except:
                continue
            # 평점을 받고 예외 발생 시 loop로 continue.
            # 로직 상 여기서 예외가 발생할 이유가 없지만 특이하게 8번 페이지에서 9번 페이지 넘어가는 부분에서 try except 처리를 해주지 예외가 발생한다.
            # 하지만 크롤링을 8번 페이지부터 시작하면 9번 페이지로 잘 넘어가 진다.
            # 크롤러는 특정 사이트에 종속적이기 때문에 원활한 크롤링을 위해 그냥 try except 해주자
        
            checker += 1
            print(title, genre, running_time, screening_rat, director, dir_all_movie_num, actor_all_movie_num, rating)
            csvWriter.writerow([title, genre, running_time, screening_rat, director, dir_all_movie_num, actor_all_movie_num, rating])
            # checker 값을 늘리고 긁어 온 data를 csv에 저장한다.
            
        checker = 2
        browser.find_element_by_css_selector("#old_content > div.pagenavigation > table > tbody > tr > td.next > a").click()
        time.sleep(1)
        # for loop이 끝나면 한 page를 모두 긁었다 뜻이므로, checker = 2로 초기화시키고 다음 페이지로 넘어간다.

    except:
        break
        
f.close()
# csvwritter를 닫느다.

