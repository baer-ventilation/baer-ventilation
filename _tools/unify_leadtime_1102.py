import io, os, re, sys

APPLY = "--apply" in sys.argv
PROD = re.compile(r'production|Production|after deposit|Lead time:|branding on an existing model|Standard production orders')
TRANSIT = re.compile(r'transit|sailing|port-to-port|port to port|from Ningbo|Ningbo/Shanghai|sea freight|Sea freight|voyage')
PAT = re.compile(r'20[\u2013\-]30 days')
OLD = '25\u201335 days'

files = []
for r, d, fs in os.walk('.'):
    if any(x in r for x in ['.git', 'node_modules', '_tools', 'assets']):
        continue
    for f in fs:
        if f.endswith('.html'):
            files.append(os.path.join(r, f))

report = []
for p in sorted(files):
    s = io.open(p, encoding='utf-8', newline='', errors='replace').read()
    if not PAT.search(s):
        continue
    for lineno, line in enumerate(s.split('\r\n'), 1):
        if PAT.search(line):
            rule = None
            if '20\u201330 days after deposit' in line or '20-30 days after deposit' in line:
                rule = 'R1 after-deposit'
            elif PROD.search(line) and not TRANSIT.search(line):
                rule = 'R2 production-line'
            report.append((p, lineno, rule, line.strip()[:150]))

print('hits:', len(report))
for p, n, rule, txt in report:
    print(f"[{rule or 'leave'}] {p}:{n}  {txt}")

if not APPLY:
    print('\n(dry run)')
    sys.exit(0)

changed = []
for p in sorted({r[0] for r in report}):
    s = io.open(p, encoding='utf-8', newline='').read()
    out, cnt = [], 0
    for line in s.split('\r\n'):
        if PAT.search(line):
            if '20\u201330 days after deposit' in line or '20-30 days after deposit' in line:
                new = line.replace('20\u201330 days after deposit', '25\u201335 days after deposit')
                new = new.replace('20-30 days after deposit', '25\u201335 days after deposit')
                if new != line:
                    cnt += line.count('after deposit')
                line = new
            elif PROD.search(line) and not TRANSIT.search(line):
                line, k = PAT.subn(OLD, line)
                cnt += k
        out.append(line)
    new = '\r\n'.join(out)
    if new != s:
        io.open(p, 'w', encoding='utf-8', newline='').write(new)
        changed.append((p, cnt))
print('\nfiles changed:', len(changed))
for p, c in changed:
    print('  ', p, c)
