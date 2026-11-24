# 製品クラス（ILCE-7CM2 Ver. 2.01、ファームウェア解析済み）

## 判明したこと

`scripts/feature_manager_matrix.py` で ILCE-7CM2 Ver. 2.01 の `appFw.so` を解析し、
feature manager の製品マトリクスをデコードした。

- 製品クラス（`PRODUCT_MODEL_*`）は **26 種**定義されている
  （LS、LAX、ALCIN_UUD、ALCIN2、ATOM、CHAPLIN、DOC、DZ、EREN、GL、HARRY、HC、
  LUKE、MT、NE、OS、OT_UUD、POTTER、PP、RS、SA、SP、TAKE_BASIC、TK_UUD、YS、YT）。
- 登録済みパラメータは **39 件**（getter は 122 件）。
  全クラス分の値とラベルは
  [evidence/feature-manager-a7cii-201.json](../evidence/feature-manager-a7cii-201.json)。

## まだ特定できていないこと

**ILCE-7CM2 自身がどのクラスで動作するかは、ファームウェア解析だけでは確定しない。**

- アップデートファイル内（config パーティション含む）に、型番と製品クラスを
  結びつける対応表は存在しなかった。クラス選択は実機側の情報に基づいて
  実行時に行われる見込み。
- 公開仕様（シングルスロット、そのスロットで CFexpress Type A 対応、
  メカシャッターあり）でマトリクスを絞り込む試みも一意に定まらなかった：
  シングルスロットのクラスは全て CFexpress 非対応となっており、
  全条件に一致するクラスが存在しない。パラメータの意味付け自体が
  実機と異なる可能性があるため、推測で結論は出さない。

## 特定方法

実機のサービスモード／PTP スナップショットで feature manager の実値を
取得し、マトリクスと突き合わせれば確定できる。手順は [TODO.md](../TODO.md) の
実機タスクに記載。
