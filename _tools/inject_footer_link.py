# -*- coding: utf-8 -*-
"""
全站页脚注入 /verify/ 入口链接。
- 命中「底部隐私行」<p style="margin:14px 0 0;font-size:12px;opacity:.85;">…</p> 的 99 个文件，
  在行尾追加 ` &middot; <a href="{verify}" style="…">label</a>`。
- privacy/index.html 的行样式略有不同（无 opacity），单独规则处理。
- 幂等：<p> 内已含 '/verify/' 则跳过（3 个新建 verify 页自带链接）。
- 严格限定在 <footer> 内：只替换 footer 内出现的该 <p>（位置校验）。
用法：python inject_footer_link.py [--apply]
"""
import io, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOTTOM = re.compile(r'<p style="margin:14px 0 0;font-size:12px;opacity:\.85;">(.*?)</p>', re.S)
BOTTOM2 = re.compile(r'<p style="margin:14px 0 0;font-size:12px;">(.*?)</p>', re.S)
FOOT = re.compile(r'<footer[\s\S]*?</footer>', re.I)

LINK = {
    'EN': ('/verify/', 'Verify Our Company'),
    'AR': ('/ar/verify/', 'تحقّق من شركتنا'),
    'ZH': ('/zh/verify/', '公司资质核验'),
}


def lang_of(p):
    q = os.path.relpath(p, ROOT).replace('\\', '/')
    if q.startswith('ar/') or q.startswith('ar__'):
        return 'AR'
    if q.startswith('zh/') or q.startswith('zh__'):
        return 'ZH'
    return 'EN'


def collect():
    files = []
    for dp, dn, fn in os.walk(ROOT):
        if '.git' in dp or os.sep + '_tools' in dp:
            continue
        for f in fn:
            if f.endswith('.html'):
                files.append(os.path.join(dp, f))
    files.sort()
    return files


def apply_to_text(s, href, label, rx):
    """在 footer 内对底部隐私行追加 verify 链接；返回 (new_s, changed, reason)"""
    fm = FOOT.search(s)
    if not fm:
        return s, False, 'no-footer'
    foot = fm.group(0)
    m = rx.search(foot)
    if not m:
        return s, False, 'no-bottomline'
    inner = m.group(1)
    if '/verify/' in inner or 'verify/' in inner and 'href="/verify' in inner:
        return s, False, 'already'
    if '/verify/' in ' '.join(re.findall(r'href="([^"]*)"', inner)):
        return s, False, 'already'
    new_p = '<p style="%s">%s &middot; <a href="%s" style="color:inherit;text-decoration:underline;">%s</a></p>' % (
        m.group(0)[len('<p style="'):m.group(0).index('">')], inner, href, label)
    new_foot = foot[:m.start()] + new_p + foot[m.end():]
    return s[:fm.start()] + new_foot + s[fm.end():], True, 'ok'


def main():
    apply = '--apply' in sys.argv
    files = collect()
    stat = collections.Counter()
    changed_files = []
    for p in files:
        s = io.open(p, encoding='utf-8', newline='').read()
        lg = lang_of(p)
        href, label = LINK[lg]
        # privacy 特例
        rx = BOTTOM2 if p.replace('\\', '/').endswith('privacy/index.html') else BOTTOM
        new_s, changed, reason = apply_to_text(s, href, label, rx)
        # 兜底：privacy 若 BOTTOM2 不中，试 BOTTOM
        if not changed and reason == 'no-bottomline':
            rx = BOTTOM
            new_s, changed, reason = apply_to_text(s, href, label, rx)
        stat[(lg, reason)] += 1
        if changed:
            changed_files.append((p, lg))
            if apply:
                io.open(p, 'w', encoding='utf-8', newline='').write(new_s)
    print("=== 注入结果统计 (lang, reason) ===")
    for k, v in sorted(stat.items()):
        print(f"  {k}: {v}")
    print(f"\n改动文件数: {len(changed_files)}")
    for p, lg in changed_files:
        print(f"  [{lg}] {os.path.relpath(p, ROOT)}")
    print("\nAPPLIED" if apply else "\nDRY-RUN（加 --apply 写入）")


if __name__ == '__main__':
    main()
