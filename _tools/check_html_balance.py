# -*- coding: utf-8 -*-
"""报告标签平衡校验（stack-based, 处理 void 元素）"""
import io, sys
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Chk(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at {self.getpos()}"); return
        if self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            # 找最近的匹配
            names = [t for t, _ in self.stack]
            if tag in names:
                idx = len(names) - 1 - names[::-1].index(tag)
                for t, pos in self.stack[idx+1:]:
                    self.errors.append(f"unclosed <{t}> opened at {pos}, closed implicitly by </{tag}> at {self.getpos()}")
                del self.stack[idx:]
            else:
                self.errors.append(f"unmatched </{tag}> at {self.getpos()}")

p = sys.argv[1] if len(sys.argv) > 1 else 'report.html'
s = io.open(p, encoding='utf-8', newline='').read()
c = Chk(); c.feed(s)
for t, pos in c.stack:
    c.errors.append(f"unclosed <{t}> opened at {pos}")
print("行数:", s.count('\n') + 1, "字符:", len(s), "字节:", len(s.encode('utf-8')))
print("标签错误:", len(c.errors))
for e in c.errors[:40]:
    print("  -", e)
print("关键锚点:", [a for a in ['id="s11"','id="s12"','id="s13"'] if a in s])
