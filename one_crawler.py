from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import logging as logger
import pandas as pd
import random
import time
import os

logger.basicConfig(level=logger.INFO)


# URL 목록 xlsx 파일 읽어오기
def read_xlsx():

    logger.info("엑셀 파일을 불러옵니다.")
    df = pd.read_excel('URL_one.xlsx')
    url_lst = df['URL'].tolist()

    return url_lst


def crawl_url(url_lst):

    global update_text
    global cat_text
    global create_text
    global down_text

    a_lst = []
    b_lst = []
    c_lst = []
    d_lst = []
    e_lst = []
    f_lst = []
    g_lst = []
    h_lst = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.set_page_load_timeout(3)
    counter = 1

    for i in range(0, len(url_lst), 1):

        try:
            driver.get(url_lst[i])
            time.sleep(2)

        except:
            driver.refresh()
            driver.get(url_lst[i])
            time.sleep(2)

        try:
            # 앱명
            name = driver.find_element_by_class_name('detailapptop-co-title')
            name_text = name.text
        except:
            name_text = 'NULL'

        try:
            # 개발자명
            dev_name = driver.find_element_by_class_name('detailapptop-co-seller')
            dev_name_text = dev_name.text
        except:
            dev_name_text = 'NULL'

        try:

            dc_info = driver.find_elements_by_class_name('detailcomment-cell')
            star = dc_info[0].find_element_by_tag_name('strong')
            star_text = star.text

            eval_num = dc_info[0].find_element_by_tag_name('span')
            eval_num_text = eval_num.text

        except:
            star_text = 'NULL'
            eval_num_text = 'NULL'

        try:
            detail_btn = driver.find_element_by_id('btn_gameDetailMore')
            detail_btn.click()
            time.sleep(1)
        except:

            update_text = 'NULL'
            cat_text = 'NULL'
            create_text = 'NULL'
            down_text = 'NULL'

        try:

            detail_info = driver.find_elements_by_class_name('cboth')

            try:
                # 장르
                cat = detail_info[1].find_element_by_tag_name('span')
                cat_text = cat.text

            except:
                cat_text = 'NULL'

            try:
                # 다운로드 수
                down = detail_info[3].find_element_by_tag_name('span')
                down_text = down.text
            except:
                down_text = 'NULL'

            try:
                # 출시일
                create = detail_info[4].find_element_by_tag_name('span')
                create_text = create.text
            except:
                create_text = 'NULL'

            try:
                # 업데이트일
                update = driver.find_element_by_class_name('detaildescriptionclamp-date')
                update_text = update.text

            except:
                update_text = 'NULL'

        except:

            update_text = 'NULL'
            cat_text = 'NULL'
            create_text = 'NULL'
            down_text = 'NULL'

        logger.info("=" * 100)
        logger.info("진행도 : {} / {}".format(counter, len(url_lst)))
        logger.info("=" * 100)
        logger.info("앱명 : {}".format(name_text))
        logger.info("개발자명 : {}".format(dev_name_text))
        logger.info("카테고리명 : {}".format(cat_text))
        logger.info("평점 : {}".format(star_text))
        logger.info("평가수 : {}".format(eval_num_text))
        logger.info("다운로드 : {}".format(down_text))
        logger.info("업데이트일 : {}".format(update_text))
        logger.info("출시일 : {}".format(create_text))
        # logger.info("버전 : {}".format(ver_text))
        logger.info("=" * 100)

        a_lst.append(name_text)
        b_lst.append(dev_name_text)
        c_lst.append(cat_text)
        d_lst.append(star_text)
        e_lst.append(eval_num_text)
        f_lst.append(down_text)
        g_lst.append(update_text)
        h_lst.append(create_text)

        counter = counter + 1

    res_dict = {"URL": url_lst, "앱명": a_lst, "개발자명": b_lst, "카테고리명": c_lst, "평점": d_lst,
                "평가수": e_lst, "다운로드": f_lst, "업데이트일": g_lst, "출시일": h_lst}

    return res_dict


def make_results(res_dict):

    now_time = time.strftime('%Y%m%d%H%M%S')
    res_df = pd.DataFrame(res_dict)
    res_df.to_excel("원스토어_결과물_{}".format(now_time) + ".xlsx", sheet_name='Sheet1')
    logger.info("엑셀파일 생성이 완료되었습니다.")

def main():

    url_lst = read_xlsx()
    res_dict = crawl_url(url_lst)
    make_results(res_dict)

    return


if __name__ == '__main__':

    main()