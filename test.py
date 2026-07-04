from lxml import html
import re

with open("generated/updated_resume.html", encoding="utf8") as f:
    root = html.fromstring(f.read())

styles = root.xpath("//style/text()")

css = "\n".join(styles)

w = re.search(r"\.w0\{width:([\d\.]+)px", css)
h = re.search(r"\.h0\{height:([\d\.]+)px", css)

print("HTML Width :", w.group(1))
print("HTML Height:", h.group(1))