#!/usr/bin/env python3
"""Assemble the publishable site into ./dist.

What gets published is declared in the index.md manifests, never inferred from
the filesystem:
  - index.md             (repo root)   -> the landing page; ## Workspaces lists courses
  - <course>/index.md    (per course)  -> ## Lessons / ## Reference / ## Docs

Each entry is `- [[slug]] — summary`. The slug is a filename stem; CI computes
the href and pulls the link text from the target's <title> (lessons/reference)
or first heading (GLOSSARY/RESOURCES), so the human only writes the summary.

Anything not referenced is not copied — that is the publish gate. After
assembly, every internal href/src in dist must resolve to an existing .html
file in dist, or the build fails (catches both hallucinated and withheld
targets, including cross-course links).
"""
import html.parser
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
TEMPLATES = BUILD / "templates"
DIST = ROOT / "dist"
SITE_CSS = (BUILD / "site.css").read_text(encoding="utf-8")
DOMAIN = "learning-piano.eu.org"

errors = []


def fail(msg):
    errors.append(msg)


def label(course_dir):
    return "(root)" if course_dir == ROOT else course_dir.name


# ---------- parsing ----------

def parse_front_matter(text):
    fm = {}
    body = text
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                for ln in lines[1:i]:
                    if ":" in ln:
                        k, v = ln.split(":", 1)
                        fm[k.strip()] = v.strip()
                return fm, "".join(lines[i + 1:])
    return fm, body


ENTRY_RE = re.compile(r"^\s*-\s*\[\[([^\]]+)\]\]\s*(?:[—–-]\s*(.*))?$")


def parse_manifest(text):
    fm, body = parse_front_matter(text)
    intro_lines, sections, order, current = [], {}, [], None
    for line in body.splitlines():
        head = re.match(r"^##\s+(.*)$", line)
        if head:
            current = head.group(1).strip()
            sections.setdefault(current, [])
            if current not in order:
                order.append(current)
            continue
        if current is None:
            intro_lines.append(line)
            continue
        m = ENTRY_RE.match(line)
        if m:
            sections[current].append((m.group(1).strip(), (m.group(2) or "").strip()))
    return fm, "\n".join(intro_lines).strip(), sections, order


TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)


def html_title(path):
    m = TITLE_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else path.stem


def md_h1(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


# ---------- resolution ----------

def resolve(section, slug, course_dir):
    """Return (href, source_path, kind) or None for an unknown section."""
    if section == "Lessons":
        return f"lessons/{slug}.html", course_dir / "lessons" / f"{slug}.html", "html"
    if section == "Reference":
        return f"reference/{slug}.html", course_dir / "reference" / f"{slug}.html", "html"
    if section == "Docs":
        return f"{slug}.html", course_dir / f"{slug}.md", "doc"
    if section == "Workspaces":
        return f"{slug}/index.html", ROOT / slug / "index.md", "workspace"
    fail(f"{label(course_dir)}/index.md: unknown section '## {section}'")
    return None


def link_text(kind, src):
    if kind == "html":
        return html_title(src)
    if kind == "doc":
        return md_h1(src)
    if kind == "workspace":
        fm, _ = parse_front_matter(src.read_text(encoding="utf-8"))
        return fm.get("title", src.parent.name)
    return src.stem


def display_link_text(section, raw, course_title):
    """Trim a prefix the section/page context already supplies, so overview
    links don't repeat it: 'Reference · X' -> 'X' under ## Reference, and
    '<course title> — Glossary' -> 'Glossary' under ## Docs."""
    if section == "Reference":
        return re.sub(r"^Reference\s*·\s*", "", raw)
    if section == "Docs" and course_title:
        m = re.match(re.escape(course_title) + r"\s*[—–-]\s*(.+)$", raw)
        if m:
            return m.group(1).strip()
    return raw


# ---------- rendering ----------

def pandoc(md_text, template, title, eyebrow=None):
    cmd = ["pandoc", "--from", "markdown", "--to", "html5", "-s",
           "--template", str(TEMPLATES / template), "--metadata", f"title={title}"]
    if eyebrow:
        cmd += ["--metadata", f"eyebrow={eyebrow}"]
    r = subprocess.run(cmd, input=md_text, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"pandoc failed for '{title}':\n{r.stderr}")
    return r.stdout.replace("/*SITE_CSS*/", SITE_CSS)


def build_overview_md(course_dir, intro, sections, order, course_title=None):
    out = []
    if intro:
        out.append(f'<div class="intro">\n\n{intro}\n\n</div>')
    for name in order:
        entries = sections.get(name, [])
        if not entries:
            continue
        out.append(f"## {name}")
        block = []
        for slug, summary in entries:
            resolved = resolve(name, slug, course_dir)
            if resolved is None:
                continue
            href, src, kind = resolved
            if not src.exists():
                fail(f"{label(course_dir)}/index.md '{name}' lists [[{slug}]] "
                     f"but {src.relative_to(ROOT)} does not exist")
                text = slug
            else:
                text = display_link_text(name, link_text(kind, src), course_title)
            block.append(f"[{text}]({href})\n: {summary}")
        out.append("\n\n".join(block))
    return "\n\n".join(out)


def build_course(slug):
    course_dir = ROOT / slug
    idx = course_dir / "index.md"
    if not idx.exists():
        fail(f"global index.md lists workspace [[{slug}]] but {slug}/index.md does not exist")
        return
    fm, intro, sections, order = parse_manifest(idx.read_text(encoding="utf-8"))
    out_dir = DIST / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in order:
        for s, _ in sections.get(name, []):
            resolved = resolve(name, s, course_dir)
            if resolved is None:
                continue
            href, src, kind = resolved
            if kind == "html":
                if not src.exists():
                    fail(f"{slug}/index.md '{name}' lists [[{s}]] but {src.relative_to(ROOT)} missing")
                    continue
                dst = out_dir / href
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            elif kind == "doc":
                if not src.exists():
                    fail(f"{slug}/index.md '{name}' lists [[{s}]] but {src.relative_to(ROOT)} missing")
                    continue
                (out_dir / href).write_text(
                    pandoc(src.read_text(encoding="utf-8"), "document.html", md_h1(src)),
                    encoding="utf-8")
    overview_md = build_overview_md(course_dir, intro, sections, order, fm.get("title", slug))
    (out_dir / "index.html").write_text(
        pandoc(overview_md, "overview.html", fm.get("title", slug), eyebrow="Learning Piano"),
        encoding="utf-8")


# ---------- integrity check ----------

class LinkExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for attr in ("href", "src"):
            if d.get(attr):
                self.links.append(d[attr])


SKIP_RE = re.compile(r"^(https?:|mailto:|tel:|data:|#|//)", re.I)
STRIP_RE = re.compile(r"<script.*?</script>|<style.*?</style>", re.S | re.I)


def link_check():
    for path in sorted(DIST.rglob("*.html")):
        text = STRIP_RE.sub("", path.read_text(encoding="utf-8"))
        p = LinkExtractor()
        p.feed(text)
        for raw in p.links:
            if SKIP_RE.match(raw):
                continue
            link = raw.split("#", 1)[0].split("?", 1)[0]
            if not link:
                continue
            target = (path.parent / link).resolve()
            rel = path.relative_to(DIST)
            if not target.exists():
                fail(f"broken link in {rel}: '{raw}' -> not present in dist")
            elif target.suffix.lower() != ".html":
                fail(f"non-HTML internal link in {rel}: '{raw}'")


# ---------- main ----------

def main():
    if not (ROOT / "index.md").exists():
        sys.exit("No global index.md at repo root — nothing to build.")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    fm, intro, sections, order = parse_manifest((ROOT / "index.md").read_text(encoding="utf-8"))
    (DIST / "index.html").write_text(
        pandoc(build_overview_md(ROOT, intro, sections, order),
               "overview.html", fm.get("title", "Learning Piano")),
        encoding="utf-8")

    for slug, _ in sections.get("Workspaces", []):
        build_course(slug)

    (DIST / ".nojekyll").write_text("")
    (DIST / "CNAME").write_text(DOMAIN + "\n")

    link_check()

    if errors:
        print(f"\nBUILD FAILED — {len(errors)} problem(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    pages = sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*.html"))
    print(f"Assembled {len(pages)} page(s) into {DIST.relative_to(ROOT)}/:")
    for p in pages:
        print(f"  {p}")
    print("Link check passed.")


if __name__ == "__main__":
    main()
