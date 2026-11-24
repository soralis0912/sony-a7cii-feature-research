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
- [x] カメラ本体のファームウェア版数の確定
  （Ver. 2.01、2026-11-24 所有者確認。解析対象と一致）

---

# 残タスク一覧（2026-11-24 時点）

完了：サービスモード接続、設定バックアップ取得、主要プロパティの
読み取り照合、製品クラスの確定（`PRODUCT_MODEL_PP`）、地域の確定（J1）、
ファームウェア版数の確定（A）、**Jiritsu 読み取りプローブ（B）**、
BK4 チェックサム検証（D）、CFexpress の訂正（E）。

**残っているのは C（プロパティ変更の実験）だけ。**

## B が通ったことの意味（2026-11-24）

Jiritsu は Senser プロトコルの `0xff00` TestMode 経由で、
`libsencore.so` のディスパッチテーブルを読むと **`0xff00` は
`pFunc_level_A` にしか無い**（レベル B は `0x40`/`0x10`/`0x20`、
レベル C は `0x40` のみ）。
B のプローブが `status 0` で通ったということは、**この機体の認証は
レベル A に到達している**ということになる。

同じコードが `terminal_change_function_is_disabled = (level != 3)` を
設定するので、レベル A なら**サービス USB 端末のゲートが開いている**。
つまり PMCA の `serviceshell` → `shell` で、カメラに何も書き込まずに
root コンソール（通常起動の initrd が回している `ash --login`）に
繋がる見込みが高い。

これは静的解析からの**推論**で、ゲートのバイトを直接見たわけではない。
確かめ方と、その先の手順は派生リポジトリ
[sony-a7cii-shell-access](https://github.com/soralis0912/sony-a7cii-shell-access)
（`scripts/survey_readonly.py`、`docs/FIELD_SESSION.md`）にまとめた。

## A. ファームウェア版数の確認【完了】

- 実機の本体ファームウェアは **Ver. 2.01**（2026-11-24、所有者確認。
  当初 2.03 と報告されたが本人の見間違いと判明）。
  解析対象の 2.01 と一致しており、版数の食い違いはない。

## B. Jiritsu 読み取り専用プローブ（旧セクション4）

> **前提（2026-11-24 判明）**：Jiritsu はサービスプロトコルの
> `0xff00` TestMode 経由で、そのディスパッチテーブルは**レベル A のみ**。
> `survey_readonly.py` でレベル A が出ない機体では、このプローブは通らない。

やり方：

1. カメラを充電し、USB 設定を **マスストレージ** にして PC に直接接続する
   （サービスモード接続テストと同じ状態）。
2. PMCA のディレクトリから、venv の python でプローブを実行する
   （スクリプトは引数なし。固定パス `/usr/share/pmbp/DeviceInfo.xml` を
   読み取り専用で取得する）：

   ```bash
   cd ~/git/a7c2/Sony-PMCA-RE
   ./venv/bin/python ~/git/a7c2/sony-a7cii-feature-research/scripts/a7cii_jiritsu_readonly_probe.py
   ```

3. 期待される出力（成功条件）：
   - `GET_FILE2 inner status: 0x00000000`
   - `Returned file bytes: 517`
   - `SHA256: e44713178fad970870ead845c93abdfcf150c418de11b306da91f2d09d67c1b7`
   - `Matches extracted firmware file: yes`
   - 最後に XML の中身が表示される

   照合先のハッシュは、展開済み 2.01 の同一ファイル
   （`nflasha15_unpacked/share/pmbp/DeviceInfo.xml`、517 バイト）から
   算出した実測値。スクリプト内の期待値とも一致している。
4. 出力をそのまま貼る（記録はこちらで行う）。

- [x] プローブを実行し、status 0 / 517 バイト / ハッシュ一致を確認する
  （2026-11-24 実施：`GET_FILE2 inner status: 0x00000000`、
  SHA-256 `e44713178f…`、Matches extracted firmware file: yes）

## C. プロパティ変更の実験（旧セクション5、1件ずつ）

対象候補は [docs/FEATURE_INVENTORY.md](docs/FEATURE_INVENTORY.md) の表
（シャッター角、Log撮影、LUT、デスクイーズ等）。
**必ず1プロパティずつ** 行い、各実験は「記録 → 書換 → 保存 → 電源断 →
確認 → 復旧」の1サイクルで完結させる。前提：セクション2の
バックアップ取得済みであること。

### 実験1（最初の1件）：シャッター角モード `0x02cf1700` を `00` → `01`

1. serviceshell を起動する：

   ```bash
   cd ~/git/a7c2/Sony-PMCA-RE
   sudo ./venv/bin/python ./pmca-console.py serviceshell
   ```

2. 変更前の値を記録する：

   ```text
   > bk r 02cf1700
   00
   ```

3. 書き換えて、メモリ上で変わったことを確認する：

   ```text
   > bk w 02cf1700 01
   > bk r 02cf1700
   01
   ```

4. 永続化してシェルを抜ける：

   ```text
   > bk s
   > exit
   ```

5. カメラの電源を切り、USB を外し、**バッテリーを10秒抜いて** から
   再装着して電源を入れる。
6. 動画モードでシャッター表示を確認する：
   速度表示（1/xxx）から角度表示（xxx°）に変わっていれば有効化成功。
   変わらなければ「反映されなかった」として記録する（失敗ではない）。
7. **復旧**：再度 serviceshell で `bk w 02cf1700 00` → `bk s` → `exit`、
   手順5の電源サイクルを繰り返し、表示が元に戻ったことと
   `bk r 02cf1700` が `00` であることを確認する。

### 実験2以降の候補（同じサイクルで1件ずつ）

| 順 | プロパティ | 変更 | 期待される確認ポイント |
| --- | --- | --- | --- |
| 2 | `0x02cf101d` LOG_SHOOTING | `00` → `01` | Log撮影メニュー／ピクチャープロファイルの表示 |
| 3 | `0x02cf1961` DE_SQUEEZE_DISP | `00` → `01` | デスクイーズ表示メニューの出現 |
| 4 | `0x02cf1702` SHUTTER_ANGLE | `10` → 別値 | 実験1が有効化できた場合のみ。角度の初期値の変化 |

- [ ] 実験1（MODE_SHUTTER）を実施し、結果と復旧を確認する
- [ ] 実験2以降を1件ずつ実施する

## D. 実機バックアップの BK4 チェックサム検証【完了・2026-11-24】

PC 上で実行し、**成功条件をすべて満たした**。

```bash
python3 scripts/bkid_inventory.py \
  <fwtool.py>/unpacked/firmware.tar_unpacked/0700_part_image/dev/nflasha15_unpacked/lib/appFw.so \
  --backup <PMCA>/a7cii-backup.bin \
  --update-root <fwtool.py>/unpacked/firmware.tar_unpacked \
  --json /tmp/a7cii-live-check.json
```

結果（実行時間 約77秒）：

| 確認項目 | 結果 |
| --- | --- |
| BK4 チェックサム | **有効。** `scripts/bk4.py` は読み込み時に検証し、不一致なら `checksum mismatch` を投げる。エラーなく完走した |
| 出力件数 | **6,450 件**（`/tmp/a7cii-live-check.json`） |
| 主要4プロパティの live 値 | `0x02cf1700`=`00` / `0x02cf1702`=`10` / `0x02cf101d`=`00` / `0x02cf102d`=`01` ＝**期待どおり** |
| 各行の付加情報 | 全件に `live=...` と `profiles=...` が付いた |

あわせて実機バックアップのヘッダから判明したこと：

| 項目 | 値 |
| --- | --- |
| Backup region | `CX89700_J1`（JP 機。`info` の表示と一致） |
| バージョン文字列 | `32014_05.2025101101` — 展開済み 2.01 の p7 `version.txt` と**完全一致** |
| バックアップ内のプロパティ総数 | 29,176（うち `BKID_APP_*` として名前が付くのが 6,450） |

バージョン文字列の一致は、セクション A（実機は Ver. 2.01）の**独立した裏付け**になる。

- [x] 上記を実行し、チェックサム有効と live 値の整合を確認する
- 生成した `/tmp/a7cii-live-check.json` は live 値を含むためコミットしない
  （リポジトリ方針どおり、生成データはローカルに留める）

## E. CFexpress パラメータ【完了・訂正済み】

- feature manager の `support_cfexpress=NONE`（PP）は実仕様と一致する。
  ILCE-7CM2 のスロットは SD（UHS-I/II）専用で CFexpress Type A 非対応。
  当初「実機は対応している」との誤った前提で課題化したが、前提の誤り
  だったため解決済みとする（背景： [docs/PRODUCT_CLASS.md](docs/PRODUCT_CLASS.md)）
