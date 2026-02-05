# CLAUDE.md

## Project Overview

MyTranslator is an Alfred workflow for fast English-Chinese translation with word origins and memory aids.

## Key Files

- `translate.py` - Main translation script using Youdao Dict API
- `info.plist` - Alfred workflow configuration
- `icon.png` - Workflow icon

## Architecture

### API Used
- **Youdao Dict API** (`dict.youdao.com/jsonapi_s`) - Free, fast (~0.2s), comprehensive
- **Youdao Official API** (optional) - Requires credentials, higher quality

### Data Fields from Youdao Dict API
| Field | Description |
|-------|-------------|
| `fanyi.tran` | Direct translation |
| `web_trans.web-translation` | Web translations |
| `ce.word.trs` | Chinese-English dictionary |
| `ec.word.trs` | English-Chinese dictionary |
| `etym.etyms.zh` | Etymology (词源词根) |
| `ec.word.wfs` | Word inflections (词形变化) |
| `rel_word.rels` | Word derivatives (派生词) |
| `discriminate.data` | Word discrimination (词义辨析) |
| `individual.idiomatic` | Collocations (常用搭配) |

## Development Notes

### Performance Optimization
- Removed slow APIs (MyMemory ~1.8s, Google ~timeout)
- Single API call to youdao_dict provides all features
- Timeout set to 5s
- Final speed: ~0.3s

### Alfred Integration
- Script Filter with keyword `yd`
- JSON output format with `items` array
- Each item has: `title`, `subtitle`, `arg`, `valid`, `icon`, `mods`

## Commands

```bash
# Test translation
python3 translate.py "happy"

# Create workflow package
zip -r MyTranslator.alfredworkflow info.plist translate.py icon.png
```

## Environment Variables (Optional)
- `youdao_app_key` - Youdao API App Key
- `youdao_app_secret` - Youdao API App Secret
