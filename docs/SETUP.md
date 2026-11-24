# セットアップ

## 要件

- Sony ILCE-7CM2（ファームウェア Ver. 2.01 を対象とする）
- データ転送可能な USB ケーブル
- Python 3
- Git
- `libusb` と、USB デバイスへアクセスする権限
- オフライン展開用の公式 Sony `BODYDATA.DAT`（Ver. 2.01）

## このリポジトリを取得

```bash
git clone https://github.com/soralis0912/sony-a7cii-feature-research.git
```

## Sony-PMCA-RE を取得

```bash
git clone https://github.com/ma1co/Sony-PMCA-RE.git
cd Sony-PMCA-RE
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS で `libusb` が無ければ：

```bash
brew install libusb
```

サービスモードの起動（想定コマンド。ILCE-7CM2 実機では未検証）：

```bash
sudo ./venv/bin/python ./pmca-console.py serviceshell
```

## fwtool（A7C II 対応ブランチ）を取得

```bash
git clone --branch a7cII https://github.com/soralis0912/fwtool.py.git
cd fwtool.py
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pycryptodomex pyyaml
```

展開手順と検証済みの値は [FIRMWARE_EXTRACTION.md](FIRMWARE_EXTRACTION.md) を参照。

`Sony-PMCA-RE`、`fwtool.py`、このリポジトリは別々のディレクトリに置く。
アップデートファイル、展開したファームウェア、カメラのバックアップは
コミットしない。

## カメラ側の準備（実機作業時）

1. サービスセッションに足るだけバッテリーを充電する。
2. カメラの USB 設定で **マスストレージ** を選ぶ。
3. カメラを PC に直接接続する。
4. 写真アプリなど、カメラの USB デバイスを占有しうるアプリを閉じる。
5. `serviceshell` を起動する。想定される遷移：

```text
Sony DSC is a camera in mass storage mode
Switching to service mode
Found a camera in service mode
Authenticating
```

USB モード切替中にタイムアウトしたら、サービスモードのデバイスが
現れてから再実行する。

> 注意：上記の実機手順は ILCE-7CM2 ではまだ未検証。
> 検証でき次第、このドキュメントを実測ベースに更新する。
