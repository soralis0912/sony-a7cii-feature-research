# Sony A7C II ファームウェア・機能リサーチ

[English version](README_EN.md)

自己責任で利用してください。本リポジトリの利用による損害について、作者は責任を負いません。

Sony **ILCE-7CM2**（A7C II）のファームウェア **Ver. 2.01** を、公式アップデートファイルと
Sony の USB サービスモードを使って調査するための、再現可能なメモとツールの置き場です。

> **状態：ファームウェア展開まで検証済み。** 実機（サービスモード等）は未検証。
> 対象の定義と調査計画・進捗は [docs/A7CII_PREP.md](docs/A7CII_PREP.md) を参照。

## 参考

このリポジトリは、[leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research)
（Sony A7 IV 6.02 のサービスモード／シャッター角／LUT／ファームウェア研究）を
**雛形として参考に**、新規に作成したものです。fork ではありません。
リポジトリ構成、ドキュメント構成、解析スクリプト、研究手法はその研究に基づきます。
A7 IV の成果はすべて原著者のものです。原典は MIT ライセンスで、その著作権表示は
[LICENSE](LICENSE) にそのまま保持しています。

なお、このリポジトリに記録する値はすべて ILCE-7CM2 のファームウェア／実機由来に
限ります。雛形に含まれていた他機種の成果ドキュメントは削除し、内容は順次
ILCE-7CM2 のものに置き換えています。

## 対象

| 項目 | 内容 |
| --- | --- |
| 型番 | ILCE-7CM2（A7C II） |
| ファームウェア | Ver. 2.01（ソニー日本、2025-11-11 公開） |
| アップデートファイル | `BODYDATA.DAT`（約1.1 GB、Sony 公式ダウンロード） |
| SoC | CXD90057（BIONZ XR） |
| FDAT モデル ID | `0x20030014`（2.01 の unpack で確認済み） |
| Crypter | `CXD90057_k8`（2.01 の unpack で確認済み） |

## 研究ステータス

| 機能 | 状態 |
| --- | --- |
| ファームウェア展開（fwtool、CXD90057） | **確認済み** — 公式 2.01 `BODYDATA.DAT` の unpack 成功（model `0x20030014`、crypter `CXD90057_k8`） |
| サービスモード | ILCE-7CM2 では未検証 |
| 設定バックアップ | 未検証 |
| 復号済みファイルシステムの読み取り | 未検証 |
| 製品クラス | 解析済み — 26クラスのマトリクスをデコード。実機のクラス確定は実機待ち（docs/PRODUCT_CLASS.md） |
| シャッター角／カスタム LUT／デスクイーズ | プロパティ ID は ILCE-7CM2 のファームウェアから特定済み（docs/FEATURE_INVENTORY.md）。実機での変更検証は未実施 |

## 上流・関連プロジェクト

- [leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research):
  本リポジトリの雛形・参考元（A7 IV の研究）。
- [ma1co/Sony-PMCA-RE](https://github.com/ma1co/Sony-PMCA-RE):
  USB サービスモードの通信とバックアップシェル。
- [soralis0912/fwtool.py](https://github.com/soralis0912/fwtool.py/tree/a7cII)
  の `a7cII` ブランチ: CXD90057 対応の Sony ファームウェア展開ツール。
  DavidBuchanan314 の fwtool.py `a7iv` ブランチからの fork。
- [ma1co/fwtool.py PR #52](https://github.com/ma1co/fwtool.py/pull/52):
  上流の CXD90057 展開作業。ILCE-7CM2 が動作確認済みリストに入っている。

## リポジトリ構成

```
docs/       セットアップ、展開（検証済み）、サービスモード、
            ライブファイルシステム読み取りの手順と、調査計画
scripts/    読み取り専用のバックアップ／ダンプと、オフラインの
            プロパティ解析ツール（a7cii_* に改名済み）
evidence/   秘匿情報を除いたプロパティ対応表と検証記録
            （ILCE-7CM2 のデータが得られ次第追加）
```

このリポジトリには、Sony のファームウェア、復号済みバイナリ、カメラのバックアップ、
シリアル番号、復号鍵、抽出したプロプライエタリファイルは意図的に含めていません。
公式アップデートは各自で入手し、生成データはローカルに留めてください。

ここに記載するカメラ側の変更はすべて、再パックしたファームウェアではなく、
永続化されたバックアッププロパティに対するものです。プロパティは1件ずつ検証し、
元のバックアップとそのハッシュはこのリポジトリの外に保管してください。
