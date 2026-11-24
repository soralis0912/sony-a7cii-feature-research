# ファームウェア展開（ILCE-7CM2 Ver. 2.01・検証済み）

## 公式アップデートファイル

| 項目 | 内容 |
| --- | --- |
| ファイル名 | `BODYDATA.DAT` |
| サイズ | 1,139,929,560 バイト（Sony 公表値と一致） |
| SHA-256 | `eb4943e6099754d64deaef5047942e9bfe258f232d0b7bc39fa23b3cd10e1e31` |
| 入手元 | Sony 公式サポート（ILCE-7CM2、Ver. 2.01、2025-11-11 公開） |

## unpack

[soralis0912/fwtool.py](https://github.com/soralis0912/fwtool.py/tree/a7cII)
の `a7cII` ブランチを使う。依存は `pycryptodomex` と `pyyaml` のみ。

```bash
cd fwtool.py   # branch: a7cII
python fwtool.py unpack -f BODYDATA.DAT -o unpacked
```

2026-11-24 に検証済み。fwtool の報告値：

```text
model:   0x20030014
version: 2.01
region:  0
crypter: CXD90057_k8
```

この結果を受けて、`ILCE-7CM2`（arch `CXD90057`、model `0x20030014`）を
fwtool fork の `devices.yml` に追加済み（`a7cII` ブランチ、commit `dd4def0`）。

なお CXD90057 では fwtool の暗号化（pack）は未実装
（`Encryption not supported`）のため、展開は読み取り専用である。

## 展開後の構成

主な調査対象：

```text
unpacked/firmware.tar_unpacked/0700_part_image/dev/
  nflasha3   (initrd 等)
  nflasha7
  nflasha8
  nflasha15  → nflasha15_unpacked/lib/appFw.so（メインアプリ、約96 MB）
```

展開ツリー全体は約3.9 GB。ファームウェア本体・展開物はこのリポジトリに
含めない（各自で公式アップデートを入手し、ローカルに保持すること）。
