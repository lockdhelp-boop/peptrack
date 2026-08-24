#!/usr/bin/env python3
"""Re-derive sitemap <lastmod> values from git history.

lastmod should reflect when a page's content actually changed, not when the
file was last touched — a CSS fingerprint re-stamp bumps mtime on every page
and would otherwise tell Google the whole site changed. Git commit dates track
real edits, so they are the honest source. Run after committing content
changes, then commit the sitemap.
"""
import re, pathlib, subprocess

sm = pathlib.Path('sitemap.xml')
s = sm.read_text()

def git_date(f):
    r = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', f],
                       capture_output=True, text=True)
    return r.stdout.strip() or None

def path_for(u):
    return u if u.endswith('.html') else ((u + 'index.html') if u else 'index.html')

n = 0
def repl(m):
    global n
    loc, old = m.group(1), m.group(2)
    f = path_for(loc)
    if not pathlib.Path(f).exists():
        return m.group(0)
    new = git_date(f)
    if not new or new == old:
        return m.group(0)
    n += 1
    return m.group(0).replace(f'<lastmod>{old}</lastmod>', f'<lastmod>{new}</lastmod>')

s = re.sub(r'<loc>https://pep-track\.app/([^<]*)</loc>\s*<lastmod>([\d-]+)</lastmod>', repl, s)
sm.write_text(s)
print(f'updated {n} lastmod dates')
