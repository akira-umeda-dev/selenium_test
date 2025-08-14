# Python
import time

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# engine（抽象度が高くlibから参照しており、testからは参照しない）

# lib
from script.lib import functions

def main(driver: webdriver.Remote):
    text_report.procedure('手順1.「http://racer.xsrv.jp/portfolio/index.html」を開く')
    functions.open_web_page(driver, report_dir_path=report_dir_path,
                            url='http://racer.xsrv.jp/portfolio/index.html')
    time.sleep(5)

    text_report.procedure('手順2.「JavaScript」をマウスオーバーする')
    javascript_el = driver.find_element(By.XPATH, '//li[@class="subnavi"][2]')
    ActionChains(driver).move_to_element(javascript_el).perform()

    save = functions.create_save_screenshot(report_dir_path)
    save(driver, image_file_name='JavaScriptマウスオーバー')
    time.sleep(2)

    text_report.procedure('手順3.「カレンダー」をクリックする')
    calender_el = driver.find_element(By.LINK_TEXT, 'カレンダー')
    calender_el.click()
    time.sleep(2)

    text_report.expected_result('期待結果3-1.URLが「http://racer.xsrv.jp/portfolio/javascript/calendar.html」であること')
    functions.confirm_url(driver,
                          report_dir_path=report_dir_path,
                          text_report=text_report,
                          expected_result='http://racer.xsrv.jp/portfolio/javascript/calendar.html')

    text_report.expected_result('期待結果3-2.カレンダーの年月が試験実施年月であること')
    _, year, month, *_, = functions.get_now_datetime(text_report=text_report)
    month = month.lstrip('0')
    functions.confirm_calender_year_and_month_match(driver,
                                                    report_dir_path=report_dir_path,
                                                    text_report=text_report,
                                                    year=year,
                                                    month=month)

##### 実行部 #####
try:
    ### 準備 ###
    report_dir_path = functions.make_result_directory()
    text_report = functions.get_text_report_instance(report_dir_path)
    ### Seleniumドライバー生成 ###
    driver = functions.generate_selenium_driver()
    ### 走行 ###
    main(driver)
    text_report.test_result(result='OK')
except Exception as e:
    text_report.test_result(result='NG')
    text_report.error_details()
finally:
    driver.quit()


