# Youdao Translate Alfred Workflow

A simple Alfred workflow for translating Chinese to English using Youdao API.

## Features

- Fast Chinese to English translation
- Supports official Youdao API (with credentials)
- Falls back to free Youdao Dictionary and Google Translate
- Copy translation result with one click

## Installation

### Method 1: Direct Installation

1. Copy this folder to Alfred's workflow directory:
   ```bash
   cp -r YouDaoAlfred ~/Library/Application\ Support/Alfred/Alfred.alfredpreferences/workflows/
   ```

2. Create the icon (on macOS):
   ```bash
   cd ~/Library/Application\ Support/Alfred/Alfred.alfredpreferences/workflows/YouDaoAlfred
   # Convert SVG to PNG using built-in tools or use any 512x512 PNG as icon.png
   ```

### Method 2: Create .alfredworkflow file

1. In the workflow folder, create a zip file:
   ```bash
   cd YouDaoAlfred
   zip -r ../YoudaoTranslate.alfredworkflow info.plist translate.py icon.png
   ```

2. Double-click the `.alfredworkflow` file to install

## Usage

1. Open Alfred (default: `Cmd + Space`)
2. Type `yd` followed by the Chinese text you want to translate
3. Press `Enter` to copy the translation to clipboard

### Examples

```
yd 你好世界
→ Hello World

yd 这是一个测试
→ This is a test
```

## Configuration (Optional)

For better translation quality, you can configure official Youdao API credentials:

1. Register at [Youdao AI Open Platform](https://ai.youdao.com/)
2. Create a text translation application to get App Key and App Secret
3. In Alfred, go to Workflows → Youdao Translate → Configure Workflow
4. Enter your App Key and App Secret

Without credentials, the workflow will use free translation services which may have rate limits.

## Icon

The workflow includes an `icon.svg` file. To convert it to PNG on macOS:

```bash
# Using qlmanage (built-in)
qlmanage -t -s 512 -o . icon.svg && mv icon.svg.png icon.png

# Or using sips with an existing PNG
# Just download any 512x512 translation icon and name it icon.png
```

Or simply download a translation icon from the internet and save it as `icon.png`.

## Requirements

- macOS with Alfred 4 or 5 (Powerpack license required for workflows)
- Python 3 (pre-installed on modern macOS)

## File Structure

```
YouDaoAlfred/
├── info.plist      # Alfred workflow configuration
├── translate.py    # Main translation script
├── icon.svg        # Vector icon (needs conversion to PNG)
├── icon.png        # Workflow icon (create from SVG)
└── README.md       # This file
```

## Troubleshooting

**Translation not working:**
- Check your internet connection
- Try again (free APIs may have rate limits)
- Configure official Youdao API for reliable service

**Alfred not showing the workflow:**
- Make sure you have Alfred Powerpack license
- Check that Python 3 is available: `python3 --version`

## License

MIT License
