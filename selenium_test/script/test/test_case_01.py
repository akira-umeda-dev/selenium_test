# Python
import time

# Selenium
from selenium import webdriver

# engine（抽象度が高くlibから参照しており、testからは参照しない）

# lib
from script.lib import functions

def main(driver: webdriver.Remote):
    text_report.procedure('手順1.「http://racer.xsrv.jp/portfolio/index.html」を開く')
    functions.open_web_page(driver, report_dir_path=report_dir_path, url='http://racer.xsrv.jp/portfolio/index.html')
    time.sleep(5)

    text_report.expected_result('期待結果1.ページタイトルが「web-pattern1(home) | portfolio」であること')
    functions.confirm_page_title(driver,
                                 report_dir_path=report_dir_path,
                                 text_report=text_report,
                                 expected_result='web-pattern1(home) | portfolio')
    time.sleep(2)

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


