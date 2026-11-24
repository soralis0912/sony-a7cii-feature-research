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
加えて、B が開けた Jiritsu 経路の読み取り範囲を広げる作業が新しく生えた（下記）。

## B が通ったことの意味（2026-11-24、訂正済み）

**訂正**：いちど「Jiritsu は `0xff00` TestMode 経由なので、通った＝
サービス権限レベル A」と書いたが、これは誤り。
`scripts/a7cii_jiritsu_readonly_probe.py` が使っているのは
`_sendAdjustControlPacket`、すなわち **PFUNC `0x40` AdjustControl** で、
これは `libsencore.so` の3つのディスパッチテーブル（A / B / C）**すべて**に
入っている。したがって B が通ったことから権限レベルは分からない。

IDA で確認した `AdjustControlFunc` の中身は、受け取ったカテゴリ／コマンドを
`SubsystemCommunicationCommand::TransactionStart` でサブシステムへ転送する形。
Jiritsu はそのサブシステムの1つで、カテゴリ **`0x1001`**。
`TestMode`（`0xff00`）は別経路（`HostCommunicationCommand`）で、
こちらは確かにレベル A のテーブルにしか無い。

### 実際に分かったこと（こちらのほうが価値がある）

B が通った＝**この機体で Jiritsu のカテゴリ `0x1001` が通る**。
同じカテゴリに**書き込み系コマンドも定義されている**（下表）。
つまり、権限レベル A を取らなくても、ファイルの読み書きが届く可能性がある。

全18コマンドを `libsencore.so` の定義表から抽出した
（`scripts/jiritsu_commands.py`、
[evidence/jiritsu-commands-a7cii-201.json](evidence/jiritsu-commands-a7cii-201.json)）。
コマンド／カテゴリはレコード内の u32 から直接読んだもので、順序からの推測ではない。
うち `0x400f` と `0x4011` は B の実測で裏が取れている。

| コマンド | 名前 | 性質 |
| --- | --- | --- |
| `0x4001` | MODE | 状態変更 |
| `0x4002` | MOUNT | 状態変更 |
| `0x4003` | FORMAT | **破壊的** |
| `0x4004` | START | 状態変更 |
| `0x4005` | DEBUG | 状態変更 |
| `0x4006` | FIRMUP | **破壊的** |
| `0x4007` | SET_FILE | **書き込み** |
| `0x4008` | GET_FILE | 読み取り |
| `0x4009` | FILE_DELETE | **破壊的** |
| `0x400a` | GET_FILELIST | 読み取り |
| `0x400b` | GET_FILE_HASH | 読み取り |
| `0x400c` | COMPARE_MEDIA | 状態変更 |
| `0x400d` | GET_VERSION | 読み取り |
| `0x400e` | FACTORY | 状態変更 |
| `0x400f` | SET_FILE_PATH | 読み取り（パス選択。**実測済み**） |
| `0x4010` | SET_FILE2 | **書き込み** |
| `0x4011` | GET_FILE2 | 読み取り（**実測済み**） |
| `0x4012` | FILE_DELETE2 | **破壊的** |

カテゴリはすべて `0x1001`、コマンドは `0x4001`〜`0x4012` の連番。

### 次に意味があること

1. **読み取りの範囲を広げる**（破壊性ゼロ）。`SET_FILE_PATH` + `GET_FILE2` は
   `../../` でルートへ抜けられるので、`/etc/ssh/sshd_config`、
   `/etc/nsswitch.conf`、`/etc/passwd`、`/setting/ulogio.bin` を読める見込み。
   これらはアップデートパッケージに入っていない（nflasha10 / nflasha2）ので、
   **読めれば静的解析では埋まらない穴が埋まる**。
2. `GET_FILELIST`（`0x400a`）と `GET_FILE_HASH`（`0x400b`）も読み取り専用。
3. **書き込みは `/tmp_wbshd` など揮発領域から**。`SET_FILE` / `SET_FILE2` の
   引数形式は未確認で、`FORMAT` / `FIRMUP` / `FILE_DELETE` が同じ番号帯に
   並んでいるので、コマンド番号の打ち間違いは危険。

手順は派生リポジトリ
[sony-a7cii-shell-access](https://github.com/soralis0912/sony-a7cii-shell-access)
の `docs/FIELD_SESSION.md` に反映する。

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

### 実験1の結果（2026-11-24、所有者が実施）

**書き換えは成立、挙動には反映されなかった。**

| 項目 | 内容 |
| --- | --- |
| 実施 | 所有者。`bk w 02cf1700 01` → `bk s` |
| 現在の live 値 | **`01`**（復旧していない。2026-11-24 21:51 の読み取りで確認） |
| `0x02cf1702 SHUTTER_ANGLE` | `10`（既定のまま） |
| 動画モードのシャッター表示 | **変化なし**（`1/50` などの速度表示のまま） |
| メニュー項目が増えたか | **未確認** |
| 電源サイクルでバッテリーを抜いたか | **踏んだ（所有者確認）** |

結論：**バッテリーを抜く電源サイクルを経ても、このプロパティ単独では
シャッター角表示にならない。** 表示については確定。
残る未確認はメニュー項目の有無だけ。

- [ ] 動画モードのメニュー（露出周り）に項目が増えていないか見る（10秒）
- [ ] 変わっていなければ `0x02cf1700` を `00` に戻して閉じる
      （`bk w 02cf1700 00` → `bk s` → 電源サイクル → `bk r` で `00` を確認）。
      効かない値を残しておくと、次の読み取りで既定との差分が紛れる

### 考えられる理由：メニューは製品クラスごとに別テーブル

feature manager の **`PRM_FEATURE_MANAGER_menu_item`**（getter `0x1797d44`、
テーブル `0x370ce60`）を全26クラス分展開すると、**クラスごとに 0〜25 の
別々の値**が割り当てられていて、**A7C II（`PP`）は 9**。
`camera_parameters` も PP = 9 で同様にクラスごとに別値。

つまりメニュー項目の集合は「クラス9用のメニュー定義」で決まる。
バックアッププロパティを立てても、**その定義に項目が無ければメニューには
出ない**という構造で、今回の結果と整合する。

### 追った結果（2026-11-24、PC のみ）：テーブルではなくコード内比較だった

- [x] getter（`0x1797d44`）の実体を確認した。3命令で、
      **`.data 0x5bc35b0` のクラス番号**を読み、`0x370ce60` の配列を
      4バイト単位で引くだけ：

      ```asm
      adrp x0, 0x5bc3000 ; ldrsw x1, [x0, #0x5b0]   ; 現在のクラス番号
      adrp x0, 0x370c000 ; add  x0, x0, #0xe60      ; menu_item のテーブル
      ldr  w0, [x0, x1, lsl #2] ; ret
      ```

      同じ形の getter が隣に並んでおり（`camera_parameters` は
      `0x370e110`、他も同様）、feature manager は
      **「クラス番号で引く4バイト配列」が PRM ごとに1本**という作り。

- [x] 呼び出し側を `.text`（`0x1660680`〜、34MB）全域から機械的に拾った。
      **menu_item の getter を呼ぶ箇所は 116 件**。その直後は
      ほぼ `cmp w0, #定数` で、**メニュー定義テーブルを引いてはいない**。
      つまり分岐は**コード中に直接書かれた「クラス番号との比較」**。

      比較している定数の分布（116件）：

      | 定数 | 件数 | | 定数 | 件数 |
      | --- | --- | --- | --- | --- |
      | 1 | 4 | | 11 | 6 |
      | 2 | 7 | | 19 | 7 |
      | 3 | 2 | | 20 | 8 |
      | 4 | 2 | | 21 | 3 |
      | 5 | 5 | | 23 | 2 |
      | 6 | 3 | | 24 | 10 |
      | 8 | 1 | | 25 | 8 |
      | **9（PP）** | **11** | | 比較なし | 26 |
      | 10 | 11 | | | |

      **PP（9）を名指しする箇所は11件**：`0x181a7a0`、`0x1c312f8`、
      `0x219fc20`、`0x3024a98`、`0x305f648`、`0x3060008`、`0x3060b60`、
      `0x3439888`、`0x34ebd50`、`0x34ebd94`、`0x357b354`。

### 何が言えるか

1. **「クラス9用のメニュー定義」という単一のテーブルは無い。**
   機能ごとに `if (menu_item() == <クラス>)` が散らばっている。
2. したがって PP で出ない項目を出すには、**その比較を書き換える**か
   `.data 0x5bc35b0` のクラス番号自体を変えることになる。前者は
   `appFw.so` のコード改変、後者は全機能のクラスが変わる乱暴な手で、
   調整値まわりに波及するので勧められない。
3. **実験1の結果と整合する。** バックアップ値を立てても、
   コード側の比較が PP を通さなければメニューには出ない。
4. よって `DE_SQUEEZE_DISP` 等についても、**プロパティ単独で開く見込みは薄い**。
   試す価値はあるが（1件あたり電源サイクル1回）、期待値は低い。

### ここから先に必要なもの

どの経路でも **`appFw.so` に触れること**が前提になる。
`/usr` は読み取り専用マウントなので、実行中のプロセスメモリか
フラッシュへの書き込みが要る。つまり**先にシェルを取るのが筋**で、
サービス権限レベル A（2026-11-24 に確認）の USB 端末が最も安全な入口。
手順は派生リポジトリ
[sony-a7cii-shell-access](https://github.com/soralis0912/sony-a7cii-shell-access)
の `docs/FIELD_SESSION.md`。

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
