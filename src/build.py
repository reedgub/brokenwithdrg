"""Builds public/index.html from src/template.html.

Run from the repo root: python3 src/build.py
Inlines the logo paths (one colour, currentColor) and wraps the page in a full document.
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT = os.path.join(ROOT, 'src'), os.path.join(ROOT, 'public')

def path(f):
    p = re.search(r'<path[^>]*/>', open(os.path.join(SRC, 'brand', f)).read()).group(0)
    p = re.sub(r'\d+\.\d{3,}', lambda m: ('%.2f' % float(m.group(0))).rstrip('0').rstrip('.'), p)
    return re.sub(r'fill="[^"]*"', 'fill="currentColor"', p)

h = open(os.path.join(SRC, 'template.html')).read()
h = h.replace('<!--LOCKUP-->', path('BROKEN_Primary_Lockup_Bone.svg')).replace('<!--ICON-->', path('BROKEN_Icon_Bone.svg'))

head_extra = '''
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0B0B0B">
<link rel="canonical" href="https://www.brokenwithdrg.com/">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.brokenwithdrg.com/">
<meta property="og:title" content="BROKEN with Dr. G">
<meta property="og:description" content="Everybody breaks. Different sports. Same scars. A YouTube series, coming soon.">
<meta property="og:image" content="https://www.brokenwithdrg.com/og-image_1200x630.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://www.brokenwithdrg.com/og-image_1200x630.png">
<style>html,body{margin:0}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>
'''
title_end = h.index('</title>') + len('</title>')
body_start = h.index('<svg width="0"')
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n' + h[:title_end] + head_extra +
       h[title_end:body_start].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '') +
       '</head>\n<body>\n' + h[body_start:] + '\n</body>\n</html>\n')
doc = '\n'.join(l.strip() for l in doc.split('\n') if l.strip()) + '\n'

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w').write(doc)
for f in ['favicon.ico', 'favicon-32x32.png', 'apple-touch-icon.png', 'og-image_1200x630.png']:
    shutil.copy(os.path.join(SRC, 'brand', f), OUT)
print('built public/index.html', len(doc))
