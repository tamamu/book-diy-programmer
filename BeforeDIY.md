# DIYする前に

## 準備

デスクトップアプリケーションを開発するにあたって、ツールキットというものを利用します。  
これはGUI(グラフィカルユーザーインターフェース)を構築するために必要です。

ここではGTK+3を前提に話を進めていきますが、他のツールキットでも似たような感じで開発出来ると思います。  
例えばQtやFLTK、JavaScriptで書きたいならElectronなんかも選択肢の1つです。  
Windowsの場合はMFCでも良いでしょう(Visual Studio必須ですが)。  
JavaならSwingかJavaFXといったように、言語によっては専用のGUIライブラリがある場合もあります。

さて、それではここから実際の作業に入っていきます。  
Python3は既にインストールされているものとして、まずはGTK+3を利用するために必要なものをインストールします。

\*NIX環境の方はお使いのパッケージマネージャからGTK+3開発用パッケージとPyGObject(PyGI)をインストールしてください。  
以下はUbuntuでの例です。

```bash
$ sudo apt-get install libgtk-3-dev python3-gi
```

macOSの方は以下の作業を行ってください。

```bash
$ brew install gtk+3
$ brew reinstall pygobject3 --with-python3
```

Windowsの方は[PyGObjectのページ](https://wiki.gnome.org/Projects/PyGObject)の**Windows installers with Gtk3 support**というところからインストーラをダウンロードします。  
あとはインストーラの手順に従い、インストールしたいライブラリを選択するところで、「GStreamer」「GTK+」「GTKSourceView」「Webkit2GTK」にチェックを入れてインストールしてください。  
※Windows版のPython3.5には対応していないようなので、既に3.5が入っている方は3.4をインストールし直すか、別のツールキットを利用してください。

GTKSourceViewはテキストエディタ、GStreamerはミュージックプレイヤー、Webkit2GTKはWebブラウザを作る時に使います。

準備が出来ていれば以下のコードでウィンドウが表示されるはずなので、確認してみてください。

```python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
```

正常に動作したでしょうか。