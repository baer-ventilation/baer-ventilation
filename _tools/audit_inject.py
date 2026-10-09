# -*- coding: utf-8 -*-
"""
逆操作审计：证明 97 个页脚注入文件「除底部隐私行追加的 verify 链接外，零附带改动」。
做法：从 git HEAD blob 读原文件 → 在 HEAD 的 footer 底部行上执行同一注入 → 与工作区逐字节比对（归一化换行）。
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOTTOM = re.compile(r'<p style="margin:14px 0 0;font-size:12px;opacity:\.85;">(.*?)</p>', re.S)
BOTTOM2 = re.compile(r'<p style="margin:14px 0 0;font-size:12px;">(.*?)</p>', re.S)
FOOT = re.compile(r'<footer[\s\S]*?</footer>', re.I)
LINK = {'EN': ('/verify/', 'Verify Our Company'),
        'AR': ('/ar/verify/', 'تحقّق من شركتنا'),
        'ZH': ('/zh/verify/', '公司资质核验')}


def lang_of(rel):
    if rel.startswith('ar/') or rel.startswith('ar__'):
        return 'AR'
    if rel.startswith('zh/') or rel.startswith('zh__'):
        return 'ZH'
    return 'EN'


def inject(s, href, label, rx):
    fm = FOOT.search(s)
    if not fm:
        return s
    foot = fm.group(0)
    m = rx.search(foot)
    if not m:
        return s
    style = m.group(0)[len('<p style="'):m.group(0).index('">')]
    new_p = '<p style="%s">%s &middot; <a href="%s" style="color:inherit;text-decoration:underline;">%s</a></p>' % (
        style, m.group(1), href, label)
    new_foot = foot[:m.start()] + new_p + foot[m.end():]
    return s[:fm.start()] + new_foot + s[fm.end():]


def norm(t):
    return t.replace('\r\n', '\n')


def main():
    # 变更文件 = git status 中的 .html
    out = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True).stdout
    paths = []
    for line in out.splitlines():
        st, p = line[:2], line[3:].strip().strip('"')
        if p.endswith('.html') and st.strip() in ('M', 'MM', 'M '):
            paths.append(p)
    ok = bad = 0
    for rel in sorted(paths):
        head = subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:' + rel],
                              capture_output=True).stdout.decode('utf-8', 'surrogateescape')
        work = io.open(os.path.join(ROOT, rel), encoding='utf-8', newline='').read()
        href, label = LINK[lang_of(rel)]
        for rx in (BOTTOM, BOTTOM2):
            recon = inject(head, href, label, rx)
            if recon != head:
                break
        if norm(recon) == norm(work):
            ok += 1
        else:
            bad += 1
            print("MISMATCH:", rel)
    print(f"\n逆操作审计：匹配 {ok} / 不匹配 {bad}  （共 {len(paths)} 个变更 HTML）")
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
