from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import logging as logger
import pandas as pd
import random
import time
import os


logger.basicConfig(level=logger.INFO)


# url csv 파일 읽기
def read_csv():

    try:

        logger.info("URL 파일을 불러옵니다.")
        df = pd.read_csv('url.csv', dtype=str)
        # logger.info(df)
        url_lst = df['URL'].tolist()
        logger.info("url 리스트를 불러왔습니다.")

        return url_lst

    except Exception as e:

        logger.error(e)


def crawl_url(url_lst):

    a_lst = []
    b_lst = []
    c_lst = []
    d_lst = []
    e_lst = []
    f_lst = []
    g_lst = []
    h_lst = []
    i_lst = []

    exc_lst = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.set_page_load_timeout(3)
    counter = 1

    for i in range(0, len(url_lst), 1):

        # TimeoutException
        try:
            driver.get(url_lst[i])
            time.sleep(2)

        except Exception as e:

            logger.error(e)
            driver.quit()
            logger.info("드라이버를 다시 로드합니다..")
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            driver.set_page_load_timeout(3)
            driver.get(url_lst[i])

        try:
            # 앱명
            name = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/span')
            name_text = name.text

        except:

            name_text = 'NULL'

        try:
            # 개발자명
            dev_name = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/div/div/a/span')
            dev_name_text = dev_name.text

        except:

            dev_name_text = 'NULL'

        try:
            # 카테고리명
            # cat = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[6]/div/section/div/div[3]/div/div/span')
            cat = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/div/div[3]/div')
            cat_text = cat.text

        except:
            cat_text = 'NULL'

        try:
            # 평점
            star = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[1]/div[1]/div/div')
            star_text = star.text
            star_text = star_text.replace("\n", "")
            star_text = star_text.replace("star", "")

        except:

            star_text = 'NULL'

        try:
            # 평가수
            eval_num = driver.find_element_by_class_name('g1rdde')
            eval_num_text = eval_num.text
            eval_num_text = eval_num_text.replace("리뷰 ", "")
            eval_num_text = eval_num_text.replace("개", "")

        except:

            eval_num_text = 'NULL'

        try:
            # 다운로드
            # down_num = driver.find_element_by_class_name('ClM7O')
            down_num = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[2]/div[1]')
            down_num_text = down_num.text
        except:

            down_num_text = 'NULL'

        try:
            # 업데이트일
            update = driver.find_element_by_class_name('xg1aie')
            update_text = update.text

        except:

            update_text = 'NULL'

        try:
            # 앱정보 클릭 후 얻어내기
            app_info_btn = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[2]/button')
            app_info_btn.click()
            time.sleep(1)

            app_infos = driver.find_elements_by_class_name('reAt0')
            create_text = app_infos[6].text
            ver_text = app_infos[2].text
            # 출시일 app_infos[6]
            # create = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[7]/div[2]')

            # 필요한 Android 버전 app_infos[2]
            # ver = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[5]/div[5]/div[2]')

        except:

            create_text = 'NULL'
            ver_text = 'NULL'

        logger.info("=" * 100)
        logger.info("진행도 : {} / {}".format(counter, len(url_lst)))
        logger.info("=" * 100)
        logger.info("앱명 : {}".format(name_text))
        logger.info("개발자명 : {}".format(dev_name_text))
        logger.info("카테고리명 : {}".format(cat_text))
        logger.info("평점 : {}".format(star_text))
        logger.info("평가수 : {}".format(eval_num_text))
        logger.info("다운로드 : {}".format(down_num_text))
        logger.info("업데이트일 : {}".format(update_text))
        logger.info("출시일 : {}".format(create_text))
        logger.info("버전 : {}".format(ver_text))
        logger.info("=" * 100)

        counter = counter + 1

        a_lst.append(name_text)
        b_lst.append(dev_name_text)
        c_lst.append(cat_text)
        d_lst.append(star_text)
        e_lst.append(eval_num_text)
        f_lst.append(down_num_text)
        g_lst.append(update_text)
        h_lst.append(create_text)
        i_lst.append(ver_text)

        """
        except Exception as e:

            # Timeout
            logger.error(e)
            exc_lst.append(url_lst[i])

            a_lst.append('NULL')
            b_lst.append('NULL')
            c_lst.append('NULL')
            d_lst.append('NULL')
            e_lst.append('NULL')
            f_lst.append('NULL')
            g_lst.append('NULL')
            h_lst.append('NULL')
            i_lst.append('NULL')
        """

    res_dict = {"URL": url_lst, "앱명": a_lst, "개발자명": b_lst, "카테고리명": c_lst, "평점": d_lst, "평가수": e_lst,
                "다운로드": f_lst, "업데이트일": g_lst, "출시일": h_lst, "버전": i_lst}
    exc_dict = {"URL": exc_lst}

    return res_dict, exc_dict


def make_results(res_dict, exc_dict):

    now_time = time.strftime('%Y%m%d%H%M%S')
    df = pd.DataFrame(res_dict)
    exc_df = pd.DataFrame(exc_dict)

    df.to_excel("플레이스토어 결과물_{}".format(now_time) + ".xlsx", sheet_name="Sheet1")
    exc_df.to_excel("재조사 필요리스트_{}".format(now_time) + ".xlsx", sheet_name="Sheet1")

    logger.info("결과물 엑셀 파일들의 생성이 완료되었습니다.")


def main():

    url_lst = read_csv()
    res_dict, exc_dict = crawl_url(url_lst)
    make_results(res_dict, exc_dict)


if __name__ == '__main__':

    main()