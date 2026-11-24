# 製品クラス（ILCE-7CM2 Ver. 2.01）

## 結論：ILCE-7CM2 は `PRODUCT_MODEL_PP`

**ILCE-7CM2 は製品クラス `PRODUCT_MODEL_PP` で動作する**（2026-11-24、実機で確定）。

### 根拠1：バックアッププロファイルの格納先（決定的）

アップデートファイル内の地域プロファイルは
`0110_backup/SYSIPSX-DSLR/PP/` の下にだけ格納されており、
実機のサービスモード `info` が示した Backup region は **`CX89700_J1`**、
すなわち `PP/CX89700_J1.bin` そのものだった。
プロファイルの格納フォルダ名が製品クラス名であることは、
A7 IV の研究（`SYSIPSX-DSLR/LS` → `PRODUCT_MODEL_LS`）で実証済みの対応関係。

### 根拠2：ハードウェア特性との一致（26クラス中 PP のみ全一致）

| パラメータ | PP の値 | A7C II の実仕様 |
| --- | --- | --- |
| `imager_model` | IMX710 | A7 IV と同じ 33MP センサー |
| `num_of_media_slot` | SINGLE | シングルスロット |
| `mecha_shutter` | AVAILABLE | メカシャッターあり |
| `shutter_curtain` | AVAILABLE | 先幕あり |
| `shoot_mode_switch` | モードダイヤル＋レバー | モードダイヤルあり |
| `product_concept` | OTHER | Cinema Line ではない |

次点の DZ / SP は imager が異なり、LS（A7 IV）はスロット数が異なる。

### 残る注意点：CFexpress の表記

`support_cfexpress` は PP では `NONE` だが、実際の A7C II のスロットは
CFexpress Type A に対応する。この食い違いはシングルスロットの全クラスに
共通するため、クラス判定の反証にはならない（このパラメータの意味付けが
小売仕様と異なる可能性が高い）。意味の確定は今後の課題。

## マトリクスについて

`scripts/feature_manager_matrix.py` で ILCE-7CM2 Ver. 2.01 の `appFw.so` を解析し、
feature manager の製品マトリクスをデコードした。

- 製品クラス（`PRODUCT_MODEL_*`）は **26 種**定義されている
  （LS、LAX、ALCIN_UUD、ALCIN2、ATOM、CHAPLIN、DOC、DZ、EREN、GL、HARRY、HC、
  LUKE、MT、NE、OS、OT_UUD、POTTER、PP、RS、SA、SP、TAKE_BASIC、TK_UUD、YS、YT）。
- 登録済みパラメータは **39 件**（getter は 122 件）。
  全クラス分の値とラベルは
  [evidence/feature-manager-a7cii-201.json](../evidence/feature-manager-a7cii-201.json)。

確定までの経緯：当初は「アップデートファイル内に型番とクラスを結ぶ対応表が
無いため、ファームウェアだけでは確定しない」としていたが、プロファイルの
格納フォルダという形の対応が存在し、実機の Backup region と一致したため
確定に至った。PTP スナップショット（2026-11-24 取得、392 ディスクリプタ
デコード済み）は補助資料として保持する。
