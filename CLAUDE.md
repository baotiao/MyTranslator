# CLAUDE.md

## Project Overview

MyTranslator is an Alfred workflow for fast English-Chinese translation with word origins and memory aids.

**GitHub:** https://github.com/baotiao/MyTranslator

## Key Files

| File | Description |
|------|-------------|
| `translate.py` | Main translation script |
| `info.plist` | Alfred workflow configuration |
| `icon.svg` | Workflow icon |

## Architecture

### API Used
- **Youdao Dict API** (`https://dict.youdao.com/jsonapi_s?doctype=json&jsonversion=4`)
  - Free, no authentication required
  - Fast (~0.2s)
  - Comprehensive data (translations + etymology + word forms)

- **Youdao Official API** (optional, requires credentials)
  - URL: `https://openapi.youdao.com/api`
  - Requires `youdao_app_key` and `youdao_app_secret` environment variables
  - Higher quality translations

### Data Fields from Youdao Dict API

```python
result.get('fanyi', {}).get('tran')           # 直接翻译
result.get('web_trans', {}).get('web-translation')  # 网络翻译
result.get('ce', {}).get('word', [])          # 汉英词典
result.get('ec', {}).get('word', {})          # 英汉词典
result.get('etym', {}).get('etyms', {}).get('zh', [])  # 词源词根
result.get('ec', {}).get('word', {}).get('wfs', [])    # 词形变化
result.get('rel_word', {}).get('rels', [])    # 派生词
result.get('discriminate', {}).get('data', [])  # 词义辨析
result.get('individual', {}).get('idiomatic', [])  # 常用搭配
```

### Alfred JSON Output Format

```python
{
    "items": [
        {
            "title": "翻译结果",
            "subtitle": "来源",
            "arg": "复制内容",
            "valid": True,
            "icon": {"path": "icon.png"},
            "mods": {
                "cmd": {
                    "subtitle": "按住Cmd的提示",
                    "arg": "Cmd+Enter的内容",
                    "valid": True
                }
            }
        }
    ]
}
```

## Performance Optimization History

| Version | Speed | Changes |
|---------|-------|---------|
| Initial | ~10s | Multiple APIs (Google, MyMemory, Youdao) |
| v2 | ~3-5s | Removed Google (timeout issues) |
| v3 | ~1.5s | Parallel API calls with ThreadPoolExecutor |
| v4 (current) | ~0.3s | Single API (youdao_dict only) |

### Key Optimizations
1. **Removed slow APIs**: MyMemory (~1.8s), Google (timeout)
2. **Single API call**: youdao_dict provides all features needed
3. **Reduced timeout**: 10s → 5s
4. **No threading needed**: Single fast API call

## Development Commands

```bash
# Test translation
python3 translate.py "happy"
python3 translate.py "你好"

# Create workflow package
zip -r MyTranslator.alfredworkflow info.plist translate.py icon.svg

# Create GitHub release
gh release create v1.0.0 MyTranslator.alfredworkflow --title "MyTranslator v1.0.0"
```

## Environment Variables (Optional)

```bash
export youdao_app_key="your_app_key"
export youdao_app_secret="your_app_secret"
```

## Lessons Learned

### 1. API Selection
- Not all APIs are equal in speed and quality
- Always benchmark individual APIs before combining
- One comprehensive API is better than multiple slow APIs

### 2. Alfred Workflow Structure
- `info.plist`: XML configuration with workflow objects and connections
- Script Filter: Input type that runs a script and displays results
- Each item needs unique content, avoid duplicate UIDs

### 3. Youdao API Data Structure Gotchas
- `ec.word` can be dict or list - handle both cases
- `l.i` can be string or list - check type before processing
- Always use `.get()` with defaults to avoid KeyError

### 4. GitHub CLI (gh) Installation on Linux

```bash
# For RHEL/CentOS/Alibaba Cloud Linux
curl -sL https://github.com/cli/cli/releases/latest/download/gh_*_linux_amd64.tar.gz | tar xz
mv gh_*/bin/gh ~/.local/bin/

# Login
gh auth login

# Create release
gh release create v1.0.0 file.zip --title "Title" --notes "Notes"
```

## Project History

1. Initial implementation with multiple APIs
2. Added multiple translation results
3. Added similar words (later removed)
4. Added memory aids: etymology, word discrimination, collocations
5. Added word forms: inflections, derivatives
6. Performance optimization: parallel → single fast API
7. Renamed: YouDaoAlfred → WordBridge → WordOrigin → MyTranslator
8. Published to GitHub with release
