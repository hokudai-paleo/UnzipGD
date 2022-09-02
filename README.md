# UnzipGD

- 大量のzipファイルを自動で解凍処理するアプリです．
- google driveから大量のファイルをダウンロードする場合，強制的に複数のzipファイルに分割されてしまいます．これらのzipファイルを一つ一つ手動で解凍するのはとても大変です．このアプリはこの問題を解決するために作られました．

- This app extracts multiple .zip files at once.
- When downloading a large number of files from google drive, they are forced to be split into multiple zip files. This is useful for unzipping these zip files.

## 使い方(非Githubユーザー向け)
- Codeボタンをクリックし，Download Zipボタンをクリックして，アプリをダウンロードします．
- ファイルを解凍し，v3.1フォルダ>distフォルダ>UnzipGD31.exeをクリックするとアプリが起動します．

## How to use(for non-Github users)
- Click "Code"> Click "Download Zip", then the app will be donwloaded.
- Extracts the .zip, click v3.1>dist>UnzipGD31.exe to start the app.

## 使い方(Githubユーザー向け)
- 実行ファイルはv3.1>dist>UnzipGD31.exeです．
- ご自身でソースから実行ファイルを作る場合は`pyinstaller main.py --onefile`で作れます．
  - PyQtやpyinstallerなどの必要なライブラリを予めインストールしてください．

## How to use(Github users)
- The execution file is v3.1>dist>UnzipGD31.exe.
- Build from the source by `pyinstaller main.py --onefile`.
  - You need to install PyQt, pyinstaller and other libraries required.
