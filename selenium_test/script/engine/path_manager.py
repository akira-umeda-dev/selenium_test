from datetime import datetime
from typing import Optional
from pathlib import Path

class PathManager:
    """
    テキスト、画像に共通するパス生成を担当するクラス。

    Attributes:
        base_dir (Path): 保存先のベースディレクトリ。
    """

    def __init__(self, base_dir: Path):
        """
        Args:
            base_dir (Path): 保存先のベースディレクトリ。
        """
        self.base_dir = base_dir

    def get_path(self, file_name: str, extension: Optional[str]=None,
                 is_add_datetime: bool=False, datetime_format: str="%Y%m%d_%H%M%S") -> Path:
        """
        保存パスを生成する。

        Args:
            file_name (str): ベースとなるファイル名（拡張子なしでも可）。
            extension (Optional[str]): 拡張子（例: 'png', 'txt'）。Noneの場合はfile_nameをそのまま使用。
            is_add_datetime (bool): ファイル名に日時を付加するか否かを判定するフラグ。Default to True.
            datetime_format (str): 日付と時刻のフォーマット。Default to 'YYYYMMDD_HHMMSS'

        Returns:
            Path: 保存先の完全なパス。
        """
        if is_add_datetime:
            timestamp = datetime.now().strftime(datetime_format)
            file_name = f"{timestamp}_{file_name}"

        if extension:
            file_name = f"{file_name}.{extension.lstrip('.')}"

        return self.base_dir / file_name




