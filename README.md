# Sony A7C II ファームウェア・機能リサーチ

[English version](README_EN.md)

自己責任で利用してください。本リポジトリの利用による損害について、作者は責任を負いません。

Sony **ILCE-7CM2**（A7C II）のファームウェア **Ver. 2.01** を、公式アップデートファイルと
Sony の USB サービスモードを使って調査するための、再現可能なメモとツールの置き場です。

> **状態：準備のみ。** A7C II 実機ではまだ何も検証していません。
> 対象の定義、A7 IV の研究から流用できそうなもの、再導出が必要なもの、検証手順は
> [docs/A7CII_PREP.md](docs/A7CII_PREP.md) を参照してください。

## 参考

このリポジトリは、[leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research)
（Sony A7 IV 6.02 のサービスモード／シャッター角／LUT／ファームウェア研究）を
**雛形として参考に**、新規に作成したものです。fork ではありません。
リポジトリ構成、ドキュメント構成、解析スクリプト、研究手法はその研究に基づきます。
A7 IV の成果はすべて原著者のものです。原典は MIT ライセンスで、その著作権表示は
[LICENSE](LICENSE) にそのまま保持しています。

雛形経由で引き継いだ A7 IV の結果 — バックアッププロパティ ID（`0x02cfXXXX`）、
製品クラス `PRODUCT_MODEL_LS` という結論、サービスモード認証の可否、すべての機能ステータス —
は、どれも A7 IV の結果でしかありません。A7C II では、ILCE-7CM2 のファームウェアから
再導出するか実機で検証するまでは、すべて「未検証」からやり直します。

## 対象

| 項目 | 内容 |
| --- | --- |
| 型番 | ILCE-7CM2（A7C II） |
| ファームウェア | Ver. 2.01（ソニー日本、2025-11-11 公開） |
| アップデートファイル | `BODYDATA.DAT`（約1.1 GB、Sony 公式ダウンロード） |
| SoC | CXD90057（BIONZ XR）、ILCE-7M4 と同一ファミリー |
| FDAT モデル ID | 未定 — unpack した 2.01 のヘッダから読み取る |
| Crypter | 未定 — `CXD90057_k0` / `CXD90057_k8` のどちらか（fwtool の出力で確定） |

## 研究ステータス

| 機能 | 状態 |
| --- | --- |
| ファームウェア展開（fwtool、CXD90057） | 準備済み — ツールは動作可、unpack はこれから |
| サービスモード | ILCE-7CM2 では未検証 |
| 設定バックアップ | 未検証 |
| 復号済みファイルシステムの読み取り | 未検証 |
| 製品クラス | 不明 — ILCE-7CM2 の `appFw.so` から特定する |
| シャッター角／カスタム LUT／デスクイーズ／オープンゲート | 未検証 — A7 IV のプロパティ ID は流用禁止 |

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
docs/       セットアップ、展開、サービスモード、機能別の手順
            （雛形から引き継ぎ。A7 IV の値は docs/A7CII_PREP.md に
             記録してあり、再導出が必要）
scripts/    読み取り専用のバックアップ／ダンプと、オフラインの
            プロパティ解析ツール
evidence/   秘匿情報を除いたプロパティ対応表と検証記録
            （現時点では比較用に雛形の A7 IV 6.02 データ）
```

このリポジトリには、Sony のファームウェア、復号済みバイナリ、カメラのバックアップ、
シリアル番号、復号鍵、抽出したプロプライエタリファイルは意図的に含めていません。
公式アップデートは各自で入手し、生成データはローカルに留めてください。

ここに記載するカメラ側の変更はすべて、再パックしたファームウェアではなく、
永続化されたバックアッププロパティに対するものです。プロパティは1件ずつ検証し、
元のバックアップとそのハッシュはこのリポジトリの外に保管してください。
