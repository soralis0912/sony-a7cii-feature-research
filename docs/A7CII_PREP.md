# ILCE-7CM2 調査計画と進捗

このリポジトリの対象は **ILCE-7CM2（A7C II）ファームウェア Ver. 2.01 のみ**。
ここには ILCE-7CM2 自体のファームウェアと実機から得た値だけを記録する。
他機種の値は持ち込まない。

## 対象

| 項目 | 内容 |
| --- | --- |
| 型番 | ILCE-7CM2（A7C II） |
| ファームウェア | Ver. 2.01（Sony、2025-11-11） |
| アップデートファイル | `BODYDATA.DAT`、1,139,929,560 バイト、SHA-256 `eb4943e6099754d64deaef5047942e9bfe258f232d0b7bc39fa23b3cd10e1e31` |
| SoC | CXD90057（BIONZ XR） |
| FDAT モデル ID | `0x20030014`（unpack で確認済み） |
| Crypter | `CXD90057_k8`（unpack で確認済み） |

## 進捗

1. **完了（2026-11-24）— ファームウェア展開。**
   公式 Ver. 2.01 `BODYDATA.DAT` を fwtool `a7cII` ブランチで unpack 成功。
   model / version / region / crypter を記録し、`ILCE-7CM2` を fwtool fork の
   `devices.yml` に追加した。詳細は [FIRMWARE_EXTRACTION.md](FIRMWARE_EXTRACTION.md)。
   パーティション構成（`nflasha3/7/8/15`、`nflasha15_unpacked/lib/appFw.so`）も確認済み。

2. **解析済み（2026-11-24）— 製品クラスの候補抽出。**
   feature manager のマトリクス（26クラス／39パラメータ）をデコードした。
   ただし ILCE-7CM2 自身のクラスはファームウェアだけでは確定しない
   （詳細： [PRODUCT_CLASS.md](PRODUCT_CLASS.md)）。確定は実機タスク
   （[TODO.md](../TODO.md)）で行う。

3. **実機待ち — サービスモードの読み取り専用テスト。**
   PMCA で接続し、認証の可否を確認する。設定バックアップを取得し、
   チェックサムが有効であることを検証する（`scripts/a7cii_read_backup.py`）。

4. **完了（2026-11-24）— プロパティ一覧の構築。**
   ILCE-7CM2 の `appFw.so` から `0x02cfXXXX` の対応表（全6,450件）と
   地域プロファイルのデフォルト値を抽出し、`evidence/` に置いた。
   主要プロパティの抜粋は [FEATURE_INVENTORY.md](FEATURE_INVENTORY.md)。
   実機バックアップとの突き合わせは実機タスク側で残っている。

5. **実機待ち — 機能実験。**
   シャッター角、カスタム LUT、デスクイーズ等の候補（ID は
   FEATURE_INVENTORY に特定済み）を、1プロパティずつ、
   バックアップと復旧手順を確保したうえで検証する。
   実機が必須の残作業は [TODO.md](../TODO.md) に集約した。

## ルール

- 記録する値はすべて ILCE-7CM2 の 2.01 ファームウェアまたは実機由来に限る。
- ファームウェア本体、復号済みバイナリ、カメラのバックアップ、シリアル番号、
  復号鍵はこのリポジトリに置かない。
- カメラ側の変更は永続化バックアッププロパティに対してのみ行い、
  1件ずつ検証する。
