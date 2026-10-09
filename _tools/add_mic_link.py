#!/usr/bin/env python3
"""全站 sameAs 增加 MIC 展示厅 + 三个 /verify 页插入可见「官方店铺」链接。

用法:
    python add_mic_link.py          # 干跑
    python add_mic_link.py --apply  # 写入
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIC = "https://www.made-in-china.com/showroom/907205f756d754e7"
TW = '"https://www.tradewheel.com/co/zhejiang-baer-appliance-technology-co-1040399"'

APPLY = "--apply" in sys.argv

# 三个 verify 页的可见插入行（沿用 CTA 段配色 #94A3B8 / 链接色 #E21E26）
VISIBLE = {
    "verify/index.html":
        '    <p style="font-size:13px;margin:14px 0 0;color:#94A3B8;">Official storefront: '
        '<a href="' + MIC + '" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:underline;">'
        'Made-in-China &mdash; Zhejiang Baer Electrical Technology Co., Ltd.</a></p>',
    "ar/verify/index.html":
        '    <p style="font-size:13px;margin:14px 0 0;color:#94A3B8;">المتجر الرسمي: '
        '<a href="' + MIC + '" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:underline;">'
        'Made-in-China &mdash; Zhejiang Baer Electrical Technology Co., Ltd.</a></p>',
    "zh/verify/index.html":
        '    <p style="font-size:13px;margin:14px 0 0;color:#94A3B8;">官方店铺： '
        '<a href="' + MIC + '" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:underline;">'
        'Made-in-China &mdash; 浙江巴尔电器科技有限公司</a></p>',
}

PAT_A = re.compile(re.escape(TW) + r'\]')                       # 内联闭合 ..."]
PAT_B = re.compile(re.escape(TW) + r'(\r?\n([ \t]*)\])')        # 多行闭合 ..."\n  ]


def b_repl(m):
    sep, ind = m.group(1), m.group(2)          # sep = '\n    ]' 或 '\r\n    ]'
    nl = sep[:2] if sep.startswith('\r\n') else sep[0]
    return TW + ',' + nl + ind + '"' + MIC + '"' + nl + ind + ']'


def main():
    changed, tot_a, tot_b, tot_v, skipped = [], 0, 0, 0, []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in ('.git', '_tools', '.workbuddy')]
        for f in fn:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT).replace('\\', '/')
            s = io.open(p, encoding='utf-8', newline='').read()
            if MIC in s:
                skipped.append(rel)
                continue
            n_a = len(PAT_A.findall(s))
            n_b = len(PAT_B.findall(s))
            n_v = 0
            new = s
            new = PAT_B.sub(b_repl, new)
            new = PAT_A.sub(lambda m: TW + ', "' + MIC + '"]', new)
            if rel in VISIBLE:
                anchor = re.compile(r'(^[ \t]*<p class="updated")', re.M)
                if len(anchor.findall(new)) != 1:
                    raise SystemExit(f"FATAL: anchor !=1 in {rel}")
                new = anchor.sub(lambda m: VISIBLE[rel] + '\n' + m.group(0), new, count=1)
                n_v = 1
            if new == s:
                continue
            # JSON-LD 校验
            for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
                import json
                json.loads(blk)
            changed.append((rel, n_a, n_b, n_v))
            tot_a += n_a; tot_b += n_b; tot_v += n_v
            if APPLY:
                io.open(p, 'w', encoding='utf-8', newline='').write(new)

    print(f"{'APPLY' if APPLY else 'DRY '} | 文件 {len(changed)} | sameAs 内联 +{tot_a} | 多行 +{tot_b} | 可见链接 +{tot_v}")
    print(f"已含 MIC 跳过: {len(skipped)} {skipped[:5]}")
    for rel, a, b, v in changed:
        if b or v:
            print(f"  [A{a} B{b} V{v}] {rel}")
    # 幂等复跑应全空
    if not APPLY and tot_a + tot_b + tot_v == 0:
        print("!! 零命中，检查正则")


if __name__ == '__main__':
    main()
