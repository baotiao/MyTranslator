#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Youdao Translation Script for Alfred Workflow
Translates Chinese to English using multiple APIs with multiple results
"""

import sys
import json
import hashlib
import time
import uuid
import urllib.request
import urllib.parse
import os


def get_youdao_sign(app_key, app_secret, query, salt, cur_time):
    """Generate Youdao API signature"""
    sign_str = app_key + truncate(query) + salt + cur_time + app_secret
    return hashlib.sha256(sign_str.encode('utf-8')).hexdigest()


def truncate(query):
    """Truncate query for signature"""
    if query is None:
        return None
    size = len(query)
    if size <= 20:
        return query
    return query[:10] + str(size) + query[-10:]


def translate_youdao_official(query, app_key, app_secret):
    """Translate using official Youdao API (requires app_key and app_secret)"""
    url = 'https://openapi.youdao.com/api'
    salt = str(uuid.uuid4())
    cur_time = str(int(time.time()))
    sign = get_youdao_sign(app_key, app_secret, query, salt, cur_time)

    params = {
        'q': query,
        'from': 'zh-CHS',
        'to': 'en',
        'appKey': app_key,
        'salt': salt,
        'sign': sign,
        'signType': 'v3',
        'curtime': cur_time,
    }

    data = urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(url, data=data)

    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode('utf-8'))

    results = []
    if result.get('errorCode') == '0':
        # Get main translations
        translations = result.get('translation', [])
        for t in translations:
            results.append({'text': t, 'source': 'Youdao API'})

        # Get web translations
        web = result.get('web', [])
        for w in web[:3]:
            values = w.get('value', [])
            for v in values[:2]:
                if v and v not in [r['text'] for r in results]:
                    results.append({'text': v, 'source': 'Youdao API (Web)'})

    return results


def translate_youdao_suggest(query):
    """Get multiple translations from Youdao Suggest API"""
    url = 'https://dict.youdao.com/suggest?num=5&ver=3.0&doctype=json&cache=false&le=en'
    params = {'q': query}
    full_url = url + '&' + urllib.parse.urlencode(params)

    req = urllib.request.Request(full_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    results = []
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))

        if result.get('result', {}).get('code') == 200:
            entries = result.get('data', {}).get('entries', [])
            for entry in entries:
                explain = entry.get('explain', '')
                entry_text = entry.get('entry', '')
                if explain:
                    # Format: "entry: explain" or just "explain" if entry matches query
                    if entry_text == query:
                        results.append({'text': explain, 'source': 'Youdao Dict'})
                    else:
                        results.append({'text': f"{entry_text}: {explain}", 'source': 'Youdao Dict'})
    except Exception:
        pass

    return results


def translate_youdao_dict(query):
    """Translate using free Youdao dictionary API with multiple results"""
    url = 'https://dict.youdao.com/jsonapi_s?doctype=json&jsonversion=4'

    params = {
        'q': query,
        'le': 'en',
        'client': 'web',
        'keyfrom': 'webdict',
    }

    full_url = url + '&' + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    results = []
    similar_words = []

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))

        # Try to get fanyi (translation) result
        fanyi = result.get('fanyi', {})
        if fanyi and fanyi.get('tran'):
            results.append({'text': fanyi.get('tran'), 'source': 'Youdao Fanyi', 'type': 'translation'})

        # Try to get web_trans results (multiple)
        web_trans = result.get('web_trans', {})
        if web_trans:
            web_translation = web_trans.get('web-translation', [])
            if web_translation:
                trans_list = web_translation[0].get('trans', [])
                for t in trans_list[:4]:
                    value = t.get('value')
                    if value and value not in [r['text'] for r in results]:
                        results.append({'text': value, 'source': 'Youdao Web', 'type': 'translation'})

        # Try to get ce (Chinese-English) results
        ce = result.get('ce', {})
        if ce:
            word_list = ce.get('word', [])
            for word in word_list:
                trs = word.get('trs', [])
                for tr in trs[:3]:
                    tr_list = tr.get('tr', [])
                    for t in tr_list:
                        text = t.get('l', {}).get('i', [])
                        if text and isinstance(text, list):
                            for item in text[:2]:
                                if item and item not in [r['text'] for r in results]:
                                    results.append({'text': item, 'source': 'Youdao CE', 'type': 'translation'})

        # Try to get ec (English-Chinese) results for reverse lookup
        ec = result.get('ec', {})
        if ec and isinstance(ec, dict):
            word_data = ec.get('word', {})
            # word can be a dict or a list
            word_list = [word_data] if isinstance(word_data, dict) else (word_data if isinstance(word_data, list) else [])
            for word in word_list:
                if not isinstance(word, dict):
                    continue
                trs = word.get('trs', [])
                for tr in trs[:3]:
                    if not isinstance(tr, dict):
                        continue
                    # Try different formats
                    tran = tr.get('tran', '')
                    if tran and tran not in [r['text'] for r in results]:
                        pos = tr.get('pos', '')
                        text = f"{pos} {tran}" if pos else tran
                        results.append({'text': text, 'source': 'Youdao EC', 'type': 'translation'})
                    # Also try the tr list format
                    tr_list = tr.get('tr', [])
                    for t in tr_list:
                        if not isinstance(t, dict):
                            continue
                        l_data = t.get('l', {})
                        if isinstance(l_data, dict):
                            i_list = l_data.get('i', [])
                            if i_list and isinstance(i_list, list):
                                for item in i_list[:2]:
                                    if item and item not in [r['text'] for r in results]:
                                        results.append({'text': item, 'source': 'Youdao EC', 'type': 'translation'})
                            elif i_list and isinstance(i_list, str):
                                if i_list not in [r['text'] for r in results]:
                                    results.append({'text': i_list, 'source': 'Youdao EC', 'type': 'translation'})

        # Get etymology (词源词根记忆)
        etym = result.get('etym', {})
        if etym:
            etyms = etym.get('etyms', {})
            zh_etyms = etyms.get('zh', []) if isinstance(etyms, dict) else []
            for e in zh_etyms[:2]:  # Show up to 2 etymology entries
                value = e.get('value', '')
                desc = e.get('desc', '')
                if value:
                    similar_words.append({
                        'text': value,
                        'source': 'Etymology',
                        'type': 'memory',
                        'subtitle': f"词源: {desc}" if desc else '词根词缀记忆'
                    })

        # Get word inflections (词形变化: 比较级、最高级、过去式等)
        ec = result.get('ec', {})
        if ec and isinstance(ec, dict):
            word_data = ec.get('word', {})
            if isinstance(word_data, dict):
                wfs = word_data.get('wfs', [])
                if wfs:
                    wf_texts = []
                    for wf in wfs:
                        w = wf.get('wf', {})
                        name = w.get('name', '')
                        value = w.get('value', '')
                        if name and value:
                            wf_texts.append(f"{name}: {value}")
                    if wf_texts:
                        similar_words.append({
                            'text': ' | '.join(wf_texts),
                            'source': 'Inflection',
                            'type': 'wordform',
                            'subtitle': '词形变化'
                        })

        # Get word forms (派生词: 名词、副词、形容词等形式)
        rel_word = result.get('rel_word', {})
        if rel_word:
            rels = rel_word.get('rels', [])
            for rel in rels:
                rel_info = rel.get('rel', {})
                pos = rel_info.get('pos', '')
                words = rel_info.get('words', [])
                for w in words[:1]:  # Only first word per POS
                    word_text = w.get('word', '')
                    word_tran = w.get('tran', '')
                    if word_text:
                        similar_words.append({
                            'text': f"{pos} {word_text}",
                            'source': 'WordForm',
                            'type': 'wordform',
                            'subtitle': word_tran
                        })

        # Get word discrimination (词义辨析)
        discriminate = result.get('discriminate', {})
        if discriminate:
            data_list = discriminate.get('data', [])
            for d in data_list[:1]:
                usages = d.get('usages', [])
                for u in usages[:2]:  # Limit to 2
                    hw = u.get('headword', '')
                    usage = u.get('usage', '')
                    if hw and usage and hw.lower() != query.lower():
                        similar_words.append({
                            'text': f"vs {hw}: {usage}",
                            'source': 'Discriminate',
                            'type': 'memory',
                            'subtitle': '词义辨析'
                        })

        # Get collocations (常用搭配)
        individual = result.get('individual', {})
        if individual:
            idiomatic = individual.get('idiomatic', [])
            for item in idiomatic[:3]:
                colloc = item.get('colloc', {})
                en = colloc.get('en', '')
                zh = colloc.get('zh', '')
                if en:
                    similar_words.append({
                        'text': en,
                        'source': 'Collocation',
                        'type': 'collocation',
                        'subtitle': zh if zh else '常用搭配'
                    })

    except Exception:
        pass

    return results, similar_words


def translate_mymemory(query):
    """Translate using MyMemory API with multiple matches"""
    url = 'https://api.mymemory.translated.net/get'

    params = {
        'q': query,
        'langpair': 'zh-CN|en',
    }

    full_url = url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    results = []
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))

        if result.get('responseStatus') == 200:
            # Main translation
            main_text = result.get('responseData', {}).get('translatedText')
            if main_text:
                results.append({'text': main_text, 'source': 'MyMemory'})

            # Additional matches (deduplicated)
            seen = {main_text.lower() if main_text else ''}
            matches = result.get('matches', [])
            for m in matches[:5]:
                trans = m.get('translation', '')
                if trans and trans.lower() not in seen:
                    seen.add(trans.lower())
                    quality = m.get('quality', 0)
                    source = m.get('source', 'MyMemory')
                    results.append({
                        'text': trans,
                        'source': f"MyMemory ({source})" if source != 'MyMemory' else 'MyMemory'
                    })
    except Exception:
        pass

    return results


def translate_google_free(query):
    """Translate using Google Translate (free, may be rate limited)"""
    url = 'https://translate.googleapis.com/translate_a/single'

    params = {
        'client': 'gtx',
        'sl': 'zh-CN',
        'tl': 'en',
        'dt': 't',
        'q': query,
    }

    full_url = url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    results = []
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))

        if result and result[0]:
            translated = ''.join([item[0] for item in result[0] if item[0]])
            if translated:
                results.append({'text': translated, 'source': 'Google'})
    except Exception:
        pass

    return results


def get_all_translations(query):
    """Get translations and similar words from multiple sources"""
    if not query or not query.strip():
        return [], []

    query = query.strip()
    all_results = []
    all_similar = []
    seen_texts = set()
    seen_similar = set()

    # Check for Youdao API credentials from environment
    app_key = os.environ.get('youdao_app_key', '').strip()
    app_secret = os.environ.get('youdao_app_secret', '').strip()

    # Try official Youdao API first if credentials are provided
    if app_key and app_secret:
        try:
            results = translate_youdao_official(query, app_key, app_secret)
            for r in results:
                if r['text'].lower() not in seen_texts:
                    seen_texts.add(r['text'].lower())
                    r['type'] = 'translation'
                    all_results.append(r)
        except Exception:
            pass

    # Try Youdao Suggest API (good for word meanings)
    try:
        results = translate_youdao_suggest(query)
        for r in results:
            if r['text'].lower() not in seen_texts:
                seen_texts.add(r['text'].lower())
                r['type'] = 'translation'
                all_results.append(r)
    except Exception:
        pass

    # Try Youdao Dict API (returns both translations and similar words)
    try:
        results, similar = translate_youdao_dict(query)
        for r in results:
            if r['text'].lower() not in seen_texts:
                seen_texts.add(r['text'].lower())
                all_results.append(r)
        for s in similar:
            if s['text'].lower() not in seen_similar:
                seen_similar.add(s['text'].lower())
                all_similar.append(s)
    except Exception:
        pass

    # Try MyMemory API (good for sentences)
    # For sentences (few results), show MyMemory even if same translation
    try:
        results = translate_mymemory(query)
        for r in results:
            # If we have very few results, show different sources even with same text
            if len(all_results) < 3 or r['text'].lower() not in seen_texts:
                if r['text'].lower() not in seen_texts:
                    seen_texts.add(r['text'].lower())
                r['type'] = 'translation'
                all_results.append(r)
    except Exception:
        pass

    # Filter out results that are same as input query (useless)
    query_lower = query.lower().strip()
    all_results = [r for r in all_results if r['text'].lower().strip() != query_lower]

    return all_results, all_similar


def create_alfred_output(query):
    """Create Alfred JSON output with translations and similar words"""
    items = []

    try:
        translations, similar_words = get_all_translations(query)

        # Add translations first
        if translations:
            for r in translations[:5]:  # Limit translations
                items.append({
                    'title': r['text'],
                    'subtitle': r['source'],
                    'arg': r['text'],
                    'valid': True,
                    'icon': {
                        'path': 'icon.png'
                    },
                    'mods': {
                        'cmd': {
                            'subtitle': 'Press Cmd+Enter to copy original text',
                            'arg': query,
                            'valid': True
                        }
                    }
                })

        # Add similar words / synonyms / phrases / memory aids
        # Sort to prioritize memory aids: memory > collocation > synonym > related > phrase
        if similar_words:
            type_priority = {'memory': 0, 'collocation': 1, 'similar': 2, 'phrase': 3}
            similar_words_sorted = sorted(similar_words,
                key=lambda x: type_priority.get(x.get('type', 'phrase'), 3))

            for s in similar_words_sorted[:10]:  # Limit similar words
                subtitle = s.get('subtitle', '')
                source = s.get('source', 'Similar')
                type_label = s.get('type', 'similar')

                # Determine label based on type
                if type_label == 'phrase':
                    label = 'Phrase'
                    icon_suffix = ''
                elif type_label == 'memory':
                    label = 'Memory'
                    icon_suffix = ''
                elif type_label == 'collocation':
                    label = 'Colloc'
                    icon_suffix = ''
                elif source == 'Synonym':
                    label = 'Synonym'
                    icon_suffix = ''
                elif source == 'Discriminate':
                    label = 'Compare'
                    icon_suffix = ''
                else:
                    label = 'Related'
                    icon_suffix = ''

                display_subtitle = subtitle if subtitle else label

                items.append({
                    'title': s['text'],
                    'subtitle': display_subtitle,
                    'arg': s['text'],
                    'valid': True,
                    'icon': {
                        'path': 'icon.png'
                    },
                    'mods': {
                        'cmd': {
                            'subtitle': 'Press Cmd+Enter to search this word',
                            'arg': s['text'].split(' (')[0],  # Remove POS tag for search
                            'valid': True
                        }
                    }
                })

        if not items:
            items.append({
                'title': 'Translation failed',
                'subtitle': 'Could not translate the text. Please try again.',
                'valid': False,
                'icon': {
                    'path': 'icon.png'
                }
            })
    except Exception as e:
        items.append({
            'title': 'Error occurred',
            'subtitle': str(e),
            'valid': False,
            'icon': {
                'path': 'icon.png'
            }
        })

    return json.dumps({'items': items}, ensure_ascii=False)


def main():
    if len(sys.argv) < 2:
        query = ''
    else:
        query = sys.argv[1]

    output = create_alfred_output(query)
    print(output)


if __name__ == '__main__':
    main()
