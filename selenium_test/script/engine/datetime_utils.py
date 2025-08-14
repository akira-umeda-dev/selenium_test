# Python
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# engine
from script.engine.text_report import TextReport 

class DatetimeUtils:
    """
    日付時刻をを管理するユーティリティクラス。

    Attributes:
        results_dir_path (Path): スクリーンショット画像を保存するディレクトリのパス。
    """

    def __init__(self):
        """
        DatetimeUtil インスタンスを初期化する。
        """
        pass

    @classmethod
    def get_now_datetime(cls, text_report: TextReport, is_comment: bool=True) -> tuple[str, str, str, str, str, str, str]:
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

        now = datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')
        year, month, date = now.split(' ')[0].split('-')
        hour, minute, second = now.split(' ')[1].split(':')
        if is_comment: text_report.comment(f'現在の日付時刻: {now}')
        return now, year, month, date, hour, minute, second
