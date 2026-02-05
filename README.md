# WordOrigin - Alfred Translation Workflow

Fast translation with word origins, forms, and collocations.

## Features

- **Fast** (~0.3s response time)
- **Word etymology** (词源词根记忆)
- **Word forms** (词形变化: 比较级、过去式等)
- **Word derivatives** (派生词: 名词、副词形式)
- **Collocations** (常用搭配)
- **Word discrimination** (词义辨析)

## Installation

1. Copy this folder to Alfred's workflow directory:
   ```bash
   cp -r WordOrigin ~/Library/Application\ Support/Alfred/Alfred.alfredpreferences/workflows/
   ```

2. Or create `.alfredworkflow` file:
   ```bash
   cd WordOrigin
   zip -r ../WordOrigin.alfredworkflow info.plist translate.py icon.png
   ```
   Then double-click to install.

## Usage

1. Open Alfred (`Cmd + Space`)
2. Type `yd` followed by the text to translate
3. Press `Enter` to copy

### Examples

```
yd happy
→ adj. 快乐的；幸福的...
→ 词源: 来自hap,发生，运气...
→ 比较级: happier | 最高级: happiest
→ adv. happily
→ n. happiness

yd 你好
→ hello; hi; how do you do
```

## Configuration (Optional)

For official Youdao API:

1. Register at [Youdao AI Open Platform](https://ai.youdao.com/)
2. Create application to get App Key and App Secret
3. In Alfred: Workflows → WordOrigin → Configure Workflow
4. Enter your credentials

## Requirements

- macOS with Alfred 4/5 (Powerpack required)
- Python 3

## License

MIT License
