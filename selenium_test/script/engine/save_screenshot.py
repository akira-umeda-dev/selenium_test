# Python
import traceback
from datetime import datetime
from typing import Optional
from pathlib import Path
from zoneinfo import ZoneInfo

# Selenium
from selenium import webdriver

# engine
from script.engine.path_manager import PathManager 
from script.engine.text_report import TextReport 
from script.engine.datetime_utils import DatetimeUtils 

class SaveScreenshot:
    """
    スクリーンショットを保存するクラス。

    Attributes:
        path_manager (PathManager): パス生成に使用するインスタンス。
    """

    def __init__(self, path_manager: PathManager):
        """
        Args:
            path (Path): スクリーンショットを保存するディレクトリ。
        """
        self.path_manager = path_manager

    def save(self, driver: webdriver.Remote, screenshot_name: str='',
             extension: Optional[str]='png', is_add_datetime: bool=True,
             datetime_format: str = "%Y%m%d_%H%M%S"):
        """
        スクリーンショット画像を指定パスに保存する。

        Args:
            driver (webdriver.Remote): webdriver.Remoteインスタンス。
            screenshot_name (str): スクリーンショットファイル名。
            extension (Optional[str]): 拡張子（例: 'png', 'txt'）。Noneの場合はfile_nameをそのまま使用。Default to '.png'
            is_add_datetime (bool): ファイル名に日時を付加するか否かを判定するフラグ。Default to True.
            datetime_format (str): 日付と時刻のフォーマット。Default to 'YYYYMMDD_HHMMSS'
        """
        path = self.path_manager.get_path(screenshot_name, extension, is_add_datetime, datetime_format)
        driver.save_screenshot(str(path))

def create_save_screenshot(report_dir_path: Path):
    """
    スクリーンショット画像を保存する関数を生成するファクトリ関数。
    内部でPathManagerとSaveImageのインスタンスを生成し、画像を保存する関数を返す。
    返却された関数を変数で受取り実行することで、

    Args:
        report_dir_path (Path): スクリーンショットを保存するディレクトリ。

    Returns:
        Callable[webdriver.Remote, str]: スクリーンショット画像を保存する関数。
    """
    path_manager = PathManager(report_dir_path)
    save_image = SaveScreenshot(path_manager)

    def save(driver: webdriver.Remote, screenshot_name: str='',
             extension: Optional[str]='png', is_add_datetime: bool=True,
             datetime_format: str = "%Y%m%d_%H%M%S"):
        """
        スクリーンショットを保存する関数。

        Args:
            driver (webdriver.Remote): webdriver.Remoteインスタンス。
            screenshot_name (str): 保存する画像ファイル名。
            extension (Optional[str]): 拡張子（例: 'png', 'txt'）。Noneの場合はfile_nameをそのまま使用。Default to '.png'
            is_add_datetime (bool): ファイル名に日時を付加するか否かを判定するフラグ。Default to True.
            datetime_format (str): 日付と時刻のフォーマット。Default to 'YYYYMMDD_HHMMSS'
        """
        save_image.save(driver, screenshot_name, extension, is_add_datetime, datetime_format)

    return save
