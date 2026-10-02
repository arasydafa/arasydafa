"""Refresh the Medium section of README.md from the author's RSS feed.

Cleans what the generic blog action got wrong: strips Medium tracking
params, normalizes em dashes, one post per line with a date.
"""
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://medium.com/feed/@arasydafa"
README = "README.md"
START = "<!-- BLOG-POST-LIST:START -->"
END = "<!-- BLOG-POST-LIST:END -->"
MAX_POSTS = 3


def main() -> None:
    req = urllib.request.Request(FEED, headers={"User-Agent": "portfolio-readme-bot"})
    with urllib.request.urlopen(req, timeout=30) as res:
        xml = res.read()
    items = ET.fromstring(xml).find("channel").findall("item")[:MAX_POSTS]

    lines = []
    for item in items:
        title = (item.findtext("title") or "").strip().replace("—", "-")
        link = (item.findtext("link") or "").split("?")[0].strip()
        date = parsedate_to_datetime(item.findtext("pubDate")).strftime("%b %-d, %Y")
        lines.append(f"- [{title}]({link}) · {date}")

    block = "\n".join(lines) + "\n"
    text = open(README, encoding="utf-8").read()
    updated = re.sub(
        f"{re.escape(START)}.*?{re.escape(END)}",
        f"{START}\n{block}{END}",
        text,
        flags=re.S,
    )
    if updated != text:
        open(README, "w", encoding="utf-8").write(updated)
        print("README updated")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
