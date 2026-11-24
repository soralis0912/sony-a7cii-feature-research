# TODO — 実機が必要な残タスク

ファームウェア解析で埋められる項目は docs/ と evidence/ に反映済み。
ここに残っているのは **ILCE-7CM2 実機と物理操作が必須** のものだけ。
（Muse 側では実施できない。実施したら結果を教えてください／
バックアップファイル自体は公開しないこと。）

## 1. サービスモード接続テスト

- [x] カメラを十分に充電し、USB 設定を **マスストレージ** にする
- [x] PC に直接 USB 接続し、写真アプリ等を閉じる
- [x] Sony-PMCA-RE の `serviceshell` を起動し、`Authenticating` まで進むか確認する
  （手順： [docs/SETUP.md](docs/SETUP.md)、[docs/SERVICE_MODE.md](docs/SERVICE_MODE.md)）
- [x] 結果を記録する（2026-11-24 実施：認証成功。`info` 表示は
  Model: ILCE-7CM2 / Backup region: CX89700_J1。シリアル番号は記録しない）

## 2. 設定バックアップの取得

- [x] `scripts/a7cii_read_backup.py` でバックアップを取得する
  （2026-11-24 実施）
- [x] ファイルサイズと SHA-256 を控える
  （2,390,264 バイト、SHA-256 `27ec1eb1d941aed30f6e0157af68a8d01585ae8d4906c689f3fc64b276d1b916`。
  BK4 チェックサムの検証はプロファイル照合時に実施）
- [x] バックアップファイルはリポジトリ外の安全な場所に保管する（コミット禁止）

## 3. 製品クラスの実機確定

- [ ] `scripts/a7cii_ptp_snapshot.py` で実機のスナップショットを取得する
- [ ] feature manager の実値を
  [evidence/feature-manager-a7cii-201.json](evidence/feature-manager-a7cii-201.json)
  と突き合わせ、ILCE-7CM2 の製品クラスを確定する
  （背景： [docs/PRODUCT_CLASS.md](docs/PRODUCT_CLASS.md)）

## 4. Jiritsu 読み取り専用プローブ

- [ ] `scripts/a7cii_jiritsu_readonly_probe.py` を実行し、
  `/usr/share/pmbp/DeviceInfo.xml` が読めるか確認する
- [ ] 取得したファイルのサイズと SHA-256 を、展開済み 2.01 の同一ファイルと照合する
  （手順： [docs/JIRITSU_DUMP.md](docs/JIRITSU_DUMP.md)）

## 5. プロパティ変更の実験（1件ずつ）

対象候補は [docs/FEATURE_INVENTORY.md](docs/FEATURE_INVENTORY.md) の表。
各実験ごとに：

- [ ] 変更前の値を読み取って記録する
- [ ] 1プロパティだけ書き換え、`bk s` で保存する
- [ ] カメラの電源を切り、USB を外し、バッテリーを10秒抜いてから再装着する
- [ ] メニュー表示・撮影挙動が変わったか実機で確認する
- [ ] 元の値に戻して復旧できることを確認する

## 6. 実機の現行状態の確認

- [ ] カメラ本体のファームウェア版数が Ver. 2.01 であることを本体メニューで確認する
- [x] 地域仕様（JP 機かどうか）を記録する（プロファイル照合に使う）
  （Backup region: CX89700_J1 ＝ JP 機で確定）
