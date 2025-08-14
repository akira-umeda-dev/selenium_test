# Python
import re
from pathlib import Path

class ReportDirectory:
    """
    テストスクリプトのパスをもとに、対応する結果ディレクトリを取り扱うクラス。

    指定されたスクリプトファイルのパスに基づいて、
    'results' ディレクトリ内にテスト結果を保存するための結果ディレクトリを作成する。
    結果ディレクトリ名にはスクリプト名と連番を付与し、既存の結果ディレクトリ名と重複しないようにする。

    Attributes:
        results_dir_path (Path): 'results'ディレクトリのパス。
        test_case (str): 実行スクリプト名（拡張子なし）を元にした識別子。
    """
    def __init__(self, script_path: Path):
        """
        Directory クラスの初期化。

        Args:
            script_path (Path): 実行スクリプトのファイルパス。
        """
        self.results_dir_path = script_path.parent / 'results'
        self.test_case = script_path.stem # 正規表現パターンとして使用
    
    def confirm_existance_of_directory(self) -> bool:
        """
        'results' ディレクトリ内に、現在の test_case に対応する結果ディレクトリが存在するか確認する。

        Returns:
            bool: 対応する結果ディレクトリが存在すれば True、存在しなければ False。
        """
        for subdir in self.results_dir_path.iterdir():
            if subdir.is_dir() and re.search(self.test_case, f'{subdir.name}'):
                return True
        return False
    
    def get_directory_max_num(self) -> int:
        """
        'results' ディレクトリ内の test_case に対応する結果ディレクトリの末尾に付与される連番を比較し、
        最大値を取得する。

        Returns:
            int: 結果ディレクトリの末尾に付与される連番の最大値（整数値）。
        """
        num_list = []
        for subdir in self.results_dir_path.iterdir():
            # 実施中のテストケースフォルダーを抽出（全テストケースの結果がresults配下に格納されるため）
            if self.test_case in subdir.name:
                num_list.append(int(subdir.name.split('_')[-1]))
        return max(num_list)

    def make_result_directory(self) -> Path:
        """
        test_case に対応する新しい結果ディレクトリを作成する。

        既存のディレクトリがあれば最大の連番に +1 した名前で作成し、
        なければ 'test_case_1' として作成する。

        Returns:
            Path: 作成された新しい結果ディレクトリのパス。
        """
        num = 0
        if self.confirm_existance_of_directory():
            num = self.get_directory_max_num()
        new_dir = self.results_dir_path / f'{self.test_case}_{num + 1}'
        new_dir.mkdir(exist_ok=True)
        return new_dir