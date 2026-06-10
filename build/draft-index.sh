#!/usr/bin/env bash
# Draft the index.md manifests by summarizing the lessons with `claude`.
#
# Writes <course>/index.md.draft (and ./index.md.draft for the landing page) so
# nothing you've hand-edited is clobbered. Review/edit the drafts, then rename to
# index.md and commit — committing the manifest to master is the publish gate.
#
# Usage:
#   build/draft-index.sh                 # draft all courses + the global landing
#   build/draft-index.sh <course-dir>... # draft only the named course(s)
set -euo pipefail
cd "$(dirname "$0")/.."

command -v claude >/dev/null || { echo "claude CLI not found on PATH" >&2; exit 1; }

courses=(playing-chords-blindly selecting-inversions naming-seventh-chords)

draft_course() {
  local dir="$1"
  [ -d "$dir/lessons" ] || { echo "skip $dir (no lessons/)" >&2; return; }
  echo "Drafting $dir/index.md.draft ..."
  claude -p "Read the lesson and reference HTML files under $dir/lessons and \
$dir/reference, plus $dir/GLOSSARY.md and $dir/RESOURCES.md. Then write a publish \
manifest for this workspace. Output ONLY the file content (no code fences, no \
commentary), in EXACTLY this shape:

---
title: <human-readable workspace title>
---
<one or two sentence intro to the workspace>

## Lessons
- [[<lesson-file-stem>]] — <one-line summary>

## Reference
- [[<reference-file-stem>]] — <one-line summary>

## Docs
- [[GLOSSARY]] — <one-line summary>
- [[RESOURCES]] — <one-line summary>

Rules: a <file-stem> is the filename without .html (e.g. 0001-finding-home-by-feel). \
List lessons and reference cards in numeric order. One short sentence per summary. \
Only include files that currently exist." > "$dir/index.md.draft"
}

draft_global() {
  echo "Drafting index.md.draft (landing) ..."
  claude -p "These workspace directories each have an index.md (or .draft) with a \
title and intro: ${courses[*]}. Write the global landing manifest. Output ONLY the \
file content, in EXACTLY this shape:

---
title: Learning Piano
---
<one or two sentence intro to the whole site>

## Workspaces
- [[<workspace-dir>]] — <one-line summary>

Rules: <workspace-dir> is the directory name (e.g. playing-chords-blindly). Include \
every workspace that has an index.md. One short sentence each." > "index.md.draft"
}

if [ "$#" -gt 0 ]; then
  for d in "$@"; do draft_course "${d%/}"; done
else
  for d in "${courses[@]}"; do draft_course "$d"; done
  draft_global
fi

echo "Done. Review the *.draft files, edit, then rename to index.md and commit."
