# assets

`site.css` is linked with a `?v=<hash>` fingerprint so browsers pick up
changes immediately instead of serving a stale copy. Python's dev server
sends no `Cache-Control`, and browsers then cache heuristically without
revalidating — which silently shows old CSS and looks like a layout bug.

After editing `site.css`, re-stamp every page:

```bash
python3 - <<'PY'
import pathlib, re, hashlib
ver = hashlib.sha1(pathlib.Path('assets/site.css').read_bytes()).hexdigest()[:8]
for p in pathlib.Path('.').rglob('*.html'):
    if '.git' in str(p): continue
    s = p.read_text()
    if '/assets/site.css' not in s: continue
    p.write_text(re.sub(r'href="/assets/site\.css(\?v=[a-f0-9]+)?"',
                        f'href="/assets/site.css?v={ver}"', s))
print('stamped', ver)
PY
```

Current fingerprint: `6a8fbb4c`
