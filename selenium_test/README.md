selenium-test
PythonによるSelenium自動テスト環境（Docker + WSL2）を構築・運用

本リポジトリは就職活動用ポートフォリオです。
著作権は作者に帰属し、無断での改変・再配布・商用利用を禁止します。

■環境要件

Windows Subsystem for Linux 2 (WSL2)
Docker & Docker Compose
Python 3.x（コンテナ内で使用）
Chromeブラウザ（noVNCアクセス用）
■前提条件

DockerおよびDocker Composeがインストールされていること。
GitやVSCodeは不要（コマンドラインのみで操作可能）
■ディレクトリ構造（下記参照）

directory_tree.txt script/ 以下は抽象度に応じて engine（高）、lib（中）、test（低）に分離されています。
■使用方法（VSCode不要）

1. プロジェクトのルートディレクトリに移動します  
   ※ `/path/to/` は各自の環境に応じて読み替えてください  
   ※ プロジェクトフォルダ名は共通で `selenium-test` です  
   ```bash
   cd /path/to/selenium-test
   ```

2. コンテナをバックグラウンドで起動・ビルドします（初回は数分かかります）

   ```bash
   docker-compose up --build -d
   ```

3. 起動したコンテナを確認します

   ```bash
   docker ps
   ```

4. 「selenium_test-python」という名前のコンテナに入ります

   ```bash
   docker exec -it selenium_test-python /bin/bash
   ```

5. コンテナ内の作業ディレクトリに移動します

   ```bash
   cd /selenium_test/script
   ```

6. ホスト側の Chrome ブラウザで以下にアクセスします

   ```
   http://localhost:7900/?autoconnect=1&resize=scale&password=secret
   ```

7. noVNC画面で「接続」をクリックし、パスワード「secret」を入力します

8. コンテナ内でスクリプトを実行します

   ```bash
   python test_case_01.py
   python test_case_02.py
   ```