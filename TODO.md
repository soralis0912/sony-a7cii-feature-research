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

- [x] `scripts/a7cii_ptp_snapshot.py` で実機のスナップショットを取得する
  （2026-11-24 実施：420 コード、392 ディスクリプタをデコード）
- [x] ILCE-7CM2 の製品クラスを確定する → **`PRODUCT_MODEL_PP` で確定**
  （決め手：実機の Backup region CX89700_J1 がファームウェア内の
  `0110_backup/SYSIPSX-DSLR/PP/` に対応。特性照合でも26クラス中 PP のみ
  全一致。詳細： [docs/PRODUCT_CLASS.md](docs/PRODUCT_CLASS.md)）

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

- [x] 地域仕様（JP 機かどうか）を記録する（プロファイル照合に使う）
  （Backup region: CX89700_J1 ＝ JP 機で確定）
- [ ] カメラ本体のファームウェア版数の確定（下記「残タスク」参照）

---

# 残タスク一覧（2026-11-24 時点）

完了：サービスモード接続、設定バックアップ取得、主要プロパティの
読み取り照合、製品クラスの確定（`PRODUCT_MODEL_PP`）、地域の確定（J1）。
残っているのは以下。

## A. ファームウェア版数の食い違いの解消【最優先】

- 実機の本体表示は **Ver. 2.03**（2026-11-24、所有者確認）。
  一方、本リポジトリの解析対象は **Ver. 2.01**。
- `bk r` の主要4プロパティとプロファイル名（CX89700_J1）は 2.01 側の
  値と一致したが、2.03 で変更されたプロパティが無いとは言えない。
- やること：2.03 の公式アップデートファイルを取得し、fwtool で展開して
  BKID 一覧とプロファイルを 2.01 と差分比較する。差分があれば
  evidence と docs を 2.03 ベースに更新する。

## B. Jiritsu 読み取り専用プローブ（旧セクション4）

- [ ] `scripts/a7cii_jiritsu_readonly_probe.py` を実行し、
  `/usr/share/pmbp/DeviceInfo.xml` が読めるか確認する
- [ ] 取得したファイルのサイズと SHA-256 を、展開済みファームウェアの
  同一ファイルと照合する（手順： [docs/JIRITSU_DUMP.md](docs/JIRITSU_DUMP.md)）

## C. プロパティ変更の実験（旧セクション5、1件ずつ）

対象候補は [docs/FEATURE_INVENTORY.md](docs/FEATURE_INVENTORY.md) の表
（シャッター角、Log撮影、LUT、デスクイーズ等）。各実験ごとに：

- [ ] 変更前の値を読み取って記録する
- [ ] 1プロパティだけ書き換え、`bk s` で保存する
- [ ] カメラの電源を切り、USB を外し、バッテリーを10秒抜いてから再装着する
- [ ] メニュー表示・撮影挙動が変わったか実機で確認する
- [ ] 元の値に戻して復旧できることを確認する

## D. 実機バックアップの BK4 チェックサム検証

- [ ] 取得済みバックアップ（2,390,264 バイト、SHA-256 `27ec1eb1…`）を
  `scripts/bkid_inventory.py --backup` で読み込み、BK4 チェックサムが
  有効なことと、全プロパティが CX89700_J1 プロファイルと整合することを
  確認する（ファイル自体は非公開のまま）

## E. CFexpress パラメータの意味の確定

- [ ] feature manager の `support_cfexpress` が PP で `NONE` なのに
  実機が CFexpress Type A 対応である食い違いについて、
  このパラメータが実際に何を制御するか（第2スロット専用の意味か等）を
  ファームウェア解析で確定する（背景： [docs/PRODUCT_CLASS.md](docs/PRODUCT_CLASS.md)）
