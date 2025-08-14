# Python
import inspect
import re
from typing import Optional
from pathlib import Path

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# engine
from script.engine.datetime_utils import DatetimeUtils
from script.engine.path_manager import PathManager
from script.engine.report_directory import ReportDirectory
from script.engine.save_screenshot import SaveScreenshot
from script.engine.text_report import TextReport

def get_caller_script_path(layer: int=2) -> Path:
    """
    呼び出し元のスクリプトファイルのパスを取得する。

    Args:
        layer (int): 呼び出し元の階層。 Default to 2.
        基本的にこのファイル内の関数からコールするため、呼び出し元スクリプトからはdepth=2となる

    Returns:
        Path: 呼び出し元のファイルパス（例: script/test_case_01.py）
    """
    return Path(inspect.stack()[layer].filename).resolve()

def make_result_directory() -> Path:
    """
    test_case に対応する新しい結果ディレクトリを作成する。

    既存のディレクトリがあれば最大の連番に +1 した名前で作成する。
    既存のディレクトリない場合は 'test_case_**_1' として作成する。

    Returns:
        Path: 作成された新しい結果ディレクトリのパス。
    """
    caller_script_path = get_caller_script_path()
    report_dir_obj = ReportDirectory(caller_script_path)
    return report_dir_obj.make_result_directory()

def get_text_report_instance(report_dir_path: Path) -> TextReport:
    """
    TextReportインスタンスを取得する。

    Args:
        report_dir_path (Path): 結果ディレクトリのパス。

    Returns:
        TextReport: TextReportインスタンス。
    """
    return TextReport(report_dir_path)

def generate_selenium_driver() -> webdriver.Remote:
    """
    Selenium Web Driverを生成する。

    Returns:
        driver (webdriver.Remote): webdriver.Remoteインスタンス。
    """
    selenium_url = 'http://selenium:4444/wd/hub'
    options = Options()
    # ヘッドレスモードの場合はブラウザを起動せずに実施する
    # options.add_argument('--headless')
    # chromeのSandBox機能無効化
    options.add_argument('--no-sandbox')
    # chromeが共有メモリを使わないようにする（仮想環境のクラッシュ予防）
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(command_executor=selenium_url, options=options)
    driver.maximize_window()
    return driver

def get_now_datetime(text_report: TextReport, is_comment: bool=True) -> tuple[str, str, str, str, str, str, str]:
    """
    現在の年月日時刻を取得する。

    Args:
        text_report (TextReport): TextReportインスタンス。
        is_comment (bool): 「現在の日付時刻」コメント出力判定フラグ. Default to True.

    Returns:
        tuple[str, str, str, str, str, str, str]: 以下の7つの文字列を含むタプル。
            - now: 'YYYY-MM-DD HH:MM:SS' 形式の現在時刻
            - year: 年（例: '2025'）
            - month: 月（例: '08'）
            - day: 日（例: '11'）
            - hour: 時（例: '18'）
            - minute: 分（例: '59'）
            - second: 秒（例: '00'）
    """
    return DatetimeUtils.get_now_datetime(text_report=text_report, is_comment=is_comment)

def create_save_screenshot(path: Path):
    """
    スクリーンショット画像を保存する関数を生成するファクトリ関数。
    内部でPathManagerとSaveImageのインスタンスを生成し、画像を保存する関数を返す。
    返却された関数を変数で受取り実行することで、

    Args:
        base_dir (Path): スクリーンショット画像を保存するベースディレクトリ。

    Returns:
        save (Callable[webdriver.Remote, str]): スクリーンショット画像を保存する関数。
    """
    path_manager = PathManager(path)
    save_screenshot = SaveScreenshot(path_manager)

    def save(driver: webdriver.Remote, image_file_name: str='',
             extension: Optional[str]='.png', is_add_datetime: bool=True,
             datetime_format: str = "%Y%m%d_%H%M%S"):
        """
        スクリーンショット画像を保存する関数。

        Args:
            driver (webdriver.Remote): webdriver.Remoteインスタンス。
            image_file_name (str): 保存する画像ファイル名。
            extension (Optional[str]): 拡張子（例: 'png', 'txt'）。Noneの場合はfile_nameをそのまま使用。Default to '.png'
            is_add_datetime (bool): ファイル名に日時を付加するか否かを判定するフラグ。
            datetime_format (str): 日付と時刻のフォーマット。Default to 'YYYYMMDD_HHMMSS'
        """
        save_screenshot.save(driver, image_file_name, extension, is_add_datetime, datetime_format)

    return save

def open_web_page(driver: webdriver.Remote, report_dir_path: Path, url: str):
    """
    Webページを開く。

    Args:
        driver (webdriver.Remote): webdriver.Remoteインスタンス。
        text_report (TextReport): TextReportインスタンス。
        url (str): 遷移先URL。
    """
    driver.get(url)
    save = create_save_screenshot(report_dir_path)
    save(driver, image_file_name=url)

def confirm_page_title(driver: webdriver.Remote, report_dir_path: Path,
                       text_report: TextReport, expected_result: str):
    """
    Webページのページタイトルを確認する。

    Args:
        driver (webdriver.Remote): webdriver.Remoteインスタンス。
        report_dir_path (Path): 結果レポート格納用フォルダのパス。
        text_report (TextReport): TextReportインスタンス。
        expected_result (str): 期待結果となるページタイトル。
    """
    # driver.save_screenshot(f'{str(report_dir_path)}/{driver.title}.png')
    save = create_save_screenshot(report_dir_path)
    save(driver, image_file_name=driver.title)
    if driver.title == expected_result:
        text_report.comment(f'ページタイトルが「{expected_result}」であることを確認_OK')
    else:
        raise Exception(f'ページタイトルが「{driver.title}」であり「{expected_result}」ではない_NG')

def confirm_url(driver: webdriver.Remote, report_dir_path: Path,
                text_report: TextReport, expected_result: str):
    """
    WebページのURLを確認する。

    Args:
        driver (webdriver.Remote): webdriver.Remoteインスタンス。
        report_dir_path (Path): 結果レポート格納用フォルダのパス。
        text_report (TextReport): TextReportインスタンス。
        expected_result (str): 期待結果となる遷移先URL。
    """
    save = create_save_screenshot(report_dir_path)
    save(driver, image_file_name=driver.current_url)
    if driver.current_url == expected_result:
        text_report.comment(f'URLが「{expected_result}」であることを確認_OK')
    else:
        raise Exception(f'URLが「{driver.current_url}」であり「{expected_result}」ではない_NG')
    
def get_calender_year_and_month(driver: webdriver.Remote, report_dir_path: Path,
                                text_report: TextReport) -> tuple[str, str]:
    """
    カレンダーの年月を取得する。

    Args:
        driver (webdriver.Remote): webdriver.Remoteインスタンス。
        report_dir_path (Path): 結果レポート格納用フォルダのパス。
        text_report (TextReport): TextReportインスタンス。

    Returns:
        tuple[str, str]: 以下の2つの文字列を含むタプル。
            - year: 年（例: '2025'）
            - month: 月（例: '8'）
    """
    displayed_calender_el = driver.find_element(By.TAG_NAME, 'caption')
    year, month = re.findall(r'\d+', displayed_calender_el.text)
    
    save = create_save_screenshot(report_dir_path)
    save(driver, image_file_name=displayed_calender_el.text)
    text_report.comment(f'表示中のカレンダー: {displayed_calender_el.text}')
    return year, month

def confirm_calender_year_and_month_match(driver: webdriver.Remote,
                                          report_dir_path: Path,
                                          text_report: TextReport,
                                          year: str,
                                          month: str):
    """
    カレンダーの年月が試験項目で指定された年月に一致することを確認する。
    
    Args:
        driver (webdriver.Remote): webdriver.Remoteインスタンス。
        report_dir_path (Path): 結果レポート格納用フォルダのパス。
        text_report (TextReport): TextReportインスタンス。
        year: 年（例: '2025'）
        month: 月（例: '8'）
    """
    text_report.comment(f'{year}年{month}月のカレンダーが表示されていることを確認する')
    calender_year, calender_month = get_calender_year_and_month(driver, report_dir_path, text_report)
    if year == calender_year and month == calender_month:
        text_report.comment(f'{year}年{month}月のカレンダーが表示されていることを確認_OK')
    else:
        raise Exception(f'{year}年{month}月のカレンダーが表示されていない_NG')