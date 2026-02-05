# MyTranslator

Fast Alfred workflow for English-Chinese translation with word origins and memory aids.

<img src="https://img.shields.io/badge/Alfred-4%2F5-purple" alt="Alfred 4/5"> <img src="https://img.shields.io/badge/Speed-0.3s-green" alt="Speed 0.3s"> <img src="https://img.shields.io/badge/License-MIT-blue" alt="MIT License">

## Features

| Feature | Description |
|---------|-------------|
| **Fast** | ~0.3s response time |
| **Etymology** | 词源词根记忆 (word roots) |
| **Inflections** | 词形变化 (comparative, tenses) |
| **Derivatives** | 派生词 (noun, adverb forms) |
| **Collocations** | 常用搭配 |
| **Discrimination** | 词义辨析 (word comparison) |

## Demo

```
yd happy
├── adj. 快乐的；幸福的；满意的...
├── 词源: 来自hap,发生，运气，机会。即运气好的，引申词义高兴的。
├── vs glad: 高兴,只能做表语
├── be happy to do sth. (很高兴做某事)
├── 比较级: happier | 最高级: happiest
├── adv. happily (快乐地)
└── n. happiness (幸福)
```

## Installation

### Method 1: Download Release
1. Download `MyTranslator.alfredworkflow` from [Releases](https://github.com/baotiao/MyTranslator/releases)
2. Double-click to install

### Method 2: Manual Install
```bash
git clone https://github.com/baotiao/MyTranslator.git
cd MyTranslator
zip -r MyTranslator.alfredworkflow info.plist translate.py icon.png
# Double-click MyTranslator.alfredworkflow to install
```

## Usage

1. Open Alfred (`Cmd + Space`)
2. Type `yd` + space + word/phrase
3. Press `Enter` to copy result

| Input | Output |
|-------|--------|
| `yd happy` | Translation + word origins + forms |
| `yd 你好` | hello; hi; how do you do |
| `yd remember` | Translation + etymology + verb forms |

## Configuration (Optional)

For higher quality translations with official Youdao API:

1. Register at [Youdao AI Open Platform](https://ai.youdao.com/)
2. Create a text translation application
3. In Alfred: Workflows → MyTranslator → Configure Workflow
4. Enter your App Key and App Secret

> Without credentials, the workflow uses free Youdao Dictionary API which works great for most cases.

## Requirements

- macOS
- Alfred 4 or 5 (Powerpack license required for workflows)
- Python 3 (pre-installed on macOS)

## License

MIT License

## Author

[baotiao](https://github.com/baotiao)
