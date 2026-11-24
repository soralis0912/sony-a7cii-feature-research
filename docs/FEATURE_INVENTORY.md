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
