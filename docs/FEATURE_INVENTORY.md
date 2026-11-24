# プロパティ一覧（ILCE-7CM2 Ver. 2.01、ファームウェア解析済み）

展開した ILCE-7CM2 Ver. 2.01 の `appFw.so` から、`scripts/bkid_inventory.py` で
バックアッププロパティ（`BKID_APP_*` → `0x02cfXXXX`）の対応を抽出した。
全 **6,450 件**の一覧は [evidence/bkid-inventory-a7cii-201.json](../evidence/bkid-inventory-a7cii-201.json)。

各プロパティには、アップデートファイル同梱の地域プロファイル（12種）における
デフォルト値も含まれている。下表の主要プロパティはすべて12プロファイル共通
（uniform）の値だった。

## 主要プロパティ（本リポジトリの調査対象）

| プロパティ ID | 名前 | デフォルト |
| --- | --- | --- |
| `0x02cf1700` | `BKID_APP_SETTING_MODE_SHUTTER` | `00` |
| `0x02cf1702` | `BKID_APP_SETTING_SHUTTER_ANGLE` | `10` |
| `0x02cf101d` | `BKID_APP_SETTING_LOG_SHOOTING` | `00` |
| `0x02cf19f0` | `BKID_APP_SETTING_STILL_LOG_SHOOTING` | `00` |
| `0x02cf1021` | `BKID_APP_SETTING_EMBED_LUT_FILE` | `00` |
| `0x02cf102d` | `BKID_APP_SETTING_SELECT_LUT` | `01` |
| `0x02cf1030` | `BKID_APP_SETTING_APPLY_LUT` | `00` |
| `0x02cf16a6` | `BKID_APP_CUBE_FILE_OPERATION_DESTINATION` | `00` |
| `0x02cf1983` | `BKID_APP_IMPORT_LUT_HQ_CONVERSION` | `01` |
| `0x02cf1961` | `BKID_APP_SETTING_DE_SQUEEZE_DISP` | `00` |
| `0x02cf1193` | `BKID_APP_EXTERN_DE_SQUEEZE_DISP` | `00` |
| `0x02cf1964` | `BKID_APP_EXTERN_DE_SQUEEZE_LCD_MONITOR` | `01000000` |

シャッター角系（`0x02cf1700` / `0x02cf1702`）については、
`scripts/analyze_feature_properties.py` でもコンストラクタ参照
（`0x2ef5984`、`0x2ef5a34` ほか）を確認済み。

## その他の判明事項

- ユーザー LUT のスロットは `BKID_APP_IS_EXIST_USER_LUT0` 〜 `49` の
  **50 スロット**分が定義されている（`USER_LUT_FILE_ID`、`USER_LUT_ATTR_*` も同様）。
- デスクイーズ表示系のプロパティ（`DE_SQUEEZE_DISP` 等）が ILCE-7CM2 の
  ファームウェア内に存在する。実機メニューで有効化できるかは未検証。
- ここに載っているのは「ファームウェア内に定義とデフォルトが存在する」ことまで。
  実機で読み書きできるか、変更が挙動に反映されるかは [TODO.md](../TODO.md) の
  実機タスクで検証する。

## 実機での読み取り確認（2026-11-24）

実機 ILCE-7CM2（Backup region: CX89700_J1）のサービスシェルで
主要プロパティを読み取り、ファームウェア側の値と一致することを確認した：

| プロパティ | 実機 `bk r` の値 | ファームウェアのデフォルト |
| --- | --- | --- |
| `0x02cf1700` MODE_SHUTTER | `00` | `00` |
| `0x02cf1702` SHUTTER_ANGLE | `10` | `10` |
| `0x02cf101d` LOG_SHOOTING | `00` | `00` |
| `0x02cf102d` SELECT_LUT | `01` | `01` |

BKID の名前→ID 対応（evidence/bkid-inventory-a7cii-201.json）が
実機でも正しいことが裏付けられた。書き換え実験は未実施。

## 実機バックアップとの照合（2026-11-24、PC 上で完結）

`scripts/bkid_inventory.py` に実機バックアップ（`--backup`）と展開済み
アップデート（`--update-root`）を渡して全件を突き合わせた。

- BK4 チェックサムは**有効**。`scripts/bk4.py` は読み込み時に
  `sum(header) + sum(data)` を比較し、不一致なら `checksum mismatch` を投げる。
  6,450 件を完走したので、バックアップは壊れていない。
- バックアップのヘッダは region `CX89700_J1`、バージョン文字列
  `32014_05.2025101101`。後者は展開済み 2.01 の p7 `version.txt` と一致しており、
  **実機のファームウェアが解析対象と同一**であることの独立した裏付けになる。
- バックアップ内のプロパティ総数は 29,176。このうち `appFw.so` の
  name record から名前が引けるのが 6,450 件（＝本一覧の対象）。
- 主要4プロパティの live 値は `00 / 10 / 00 / 01`（`0x02cf1700` /
  `1702` / `101d` / `102d`）で、ファームウェアの既定値と一致。

live 値を含む出力（`/tmp/a7cii-live-check.json`）は、リポジトリ方針どおり
コミットしていない。

## 書き換え実験の結果（2026-11-24）

| プロパティ | 変更 | 結果 |
| --- | --- | --- |
| `0x02cf1700` `MODE_SHUTTER` | `00` → `01` → `00`（所有者が実施、保存済み、**復旧済み**） | **シャッター表示は変化なし**（速度表示のまま）。バッテリーを抜く電源サイクルを経ても同じなので、表示については確定。メニュー項目の増減は未確認のまま。現在の live 値は `00` ＝既定 |

プロパティの読み書き自体は成立しているので、「書けるが挙動に出ない」という
分類になる。メニュー項目の出し分けは `PRM_FEATURE_MANAGER_menu_item` で
製品クラス（`PP`）側に持たれているため、バックアップ値を立てても
メニュー側の判定が先に効く可能性がある。詳細と次の確認手順は
[../TODO.md](../TODO.md) の実験1の節。

## 連番だと思って `base + n` で計算してはいけない

`bkid_inventory.py` は各 BKID の id を、ファームウェア自身の名前レコード
（`id,len,ptr` レイアウト）から**読み出している**。推定ではない。
6,450 件すべてで property_id の重複は無い。

にもかかわらず、`FOO0` と `FOO1` の id を見て step を 1 と決め、
`FOO<n> = base + n` と計算するのは誤り。**系統は途中で飛ぶ。**
ユーザー LUT の50枠がその例で、5系統すべて 0〜15 だけが一続きになっている：

| 系統 | 枠 0〜15 | 枠 16 以降 |
| --- | --- | --- |
| `IS_EXIST_USER_LUT` | `0x02cf105c`〜`0x02cf106b` | `0x02cf141e` から一続きで 49 まで |
| `USER_LUT_FILE_ID` | `0x02cf106c`〜`0x02cf107b` | `0x02cf1440` ほか5ブロックに分散 |
| `USER_LUT_ATTR_INPUT_GAMUT` | `0x02cf107c`〜`0x02cf108b` | `0x02cf16d8` から一続き |
| `USER_LUT_ATTR_OUTPUT_PROCAM` | `0x02cf1450`〜`0x02cf145f` | `0x02cf176a` から一続き |
| `USER_LUT_ATTR_AE_LEVEL_OFFSET` | `0x02cf104c`〜`0x02cf105b` | `0x02cf13a8` ほか4ブロックに分散 |

`IS_EXIST_USER_LUT15` は `0x02cf106b` で、`16` は `0x02cf141e` に飛ぶ。
`base + n` で計算すると `IS_EXIST_USER_LUT16` が `0x02cf106c` になるが、
これは `USER_LUT_FILE_ID0` の id である。

実際にそれで実機を読み、**隣の系統の値を違う名前で読んだ**結果を
「枠16〜49が全部デフォルトと違う」という発見だと誤認した事例がある
（shell-access リポジトリ `docs/LUT.md` に経緯を記録）。
JSON の `property_id` を名前で引くこと。計算しないこと。
