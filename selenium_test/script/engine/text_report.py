# Python
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# engine
from script.engine.path_manager import PathManager 

class TextReport:
    """
    テキスト形式の試験レポートを管理・出力するユーティリティクラス。

    指定されたディレクトリに対して、レポートファイル（.txt）を作成・追記する機能を提供する。
    主にテスト結果やエラーの記録に使用される。

    Attributes:
        path_manager (Path): パス生成を司るインスタンス。
        text_report_name (str): レポートファイル名（ディレクトリ名に拡張子'.txt'を付与して生成）。
    """
    def __init__(self, path: Path, is_add_datetime: bool=True):
        """
        TextReport インスタンスを初期化する。

        Args:
            path_manager (Path): レポートファイルを保存するディレクトリのパス。
            text_report_name (str): レポートファイル名。
            
        """
        self.path_manager = PathManager(path)
        self.text_report_name = path.name # ファイル名はディレクトリ名を流用する
        self.text_report_path = self.path_manager.get_path(
            file_name=self.text_report_name, extension='txt', is_add_datetime=False)

    def make_text_report(self):
        """
        レポート用ディレクトリと空のテキストファイルを作成する。

        ディレクトリが存在しない場合は作成し、ファイルが存在しない場合は空ファイルを作成する。
        """
        self.path_manager.base_dir.mkdir(parents=True, exist_ok=True)
        self.text_report_path.touch()

    def add_line_on_text_report(self, line: str, is_terminal: bool=True):
        """
        テキストレポートに1行追記する。ファイルが存在しない場合は新規作成する。
        この関数は直接コールせず、この関数をラップしている以下の関数をコールすること。
         - def procedure
         - def expected_result
         - def comment
         - def test_result
         - def error_details

        Args:
            line (str): 書き込む文字列（改行なしでもOK）。
            is_terminal (bool): ターミナル出力判定フラグ。 Default to True.
        """
        now = datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')

        if not self.text_report_path.is_file():
            self.make_text_report()
        
        with self.text_report_path.open(mode='a', encoding='utf-8') as f:
            f.write(f'{now}  {line}\n')
        
        if is_terminal: print(f'{now}  {line}')

    def procedure(self, line: str, is_terminal: bool=True):
        """
        試験手順を記入する関数。
        可読性を考慮し、add_line_on_text_report関数をラップしただけの関数。
        テキストレポートに試験手順を追記する。

        Args:
            line (str): 書き込む文字列（改行なしでもOK）。
            is_terminal (bool): ターミナル出力判定フラグ。 Default to True.
        """
        self.add_line_on_text_report(line, is_terminal)

    def expected_result(self, line: str, is_terminal: bool=True):
        """
        期待結果を記入する関数。
        可読性を考慮し、add_line_on_text_report関数をラップしただけの関数。
        テキストレポートに期待結果を追記する。

        Args:
            line (str): 書き込む文字列（改行なしでもOK）
            is_terminal (bool): ターミナル出力判定フラグ。 Default to True.
        """
        self.add_line_on_text_report(line, is_terminal)

    def comment(self, line: str, is_terminal: bool=True):
        """
        任意のコメントを記入する関数。
        可読性を考慮し、add_line_on_text_report関数をラップしただけの関数。
        テキストレポートに期待結果を追記する。

        Args:
            line (str): 書き込む文字列（改行なしでもOK）
            is_terminal (bool): ターミナル出力判定フラグ。 Default to True.
        """
        self.add_line_on_text_report(line, is_terminal)

    def test_result(self, result: str='OK', is_terminal: bool=True):
        """
        試験結果を記入する関数。
        可読性を考慮し、add_line_on_text_report関数をラップした関数。
        テキストレポートに試験結果を追記する。

        Args:
            result (str): 書き込む文字列（改行なしでもOK）。 Default to 'OK'.
            is_terminal (bool): ターミナル出力判定フラグ。 Default to True.
        """
        self.add_line_on_text_report(f'試験結果_{result}', is_terminal)

    def error_details(self, line: str='', is_terminal: bool=True):
        """
        エラーを記入する関数。
        可読性を考慮し、add_line_on_text_report関数の引数をラップした関数。
        テキストレポートにエラー内容を追記する。

        Args:
            line (str): 書き込む文字列（改行なしでもOK）。
            is_terminal (bool): ターミナル出力判定フラグ。 Default to True.
        """
        if line == '': line = f'エラー内容:\n{traceback.format_exc()}'
        self.add_line_on_text_report(line, is_terminal)
    
        