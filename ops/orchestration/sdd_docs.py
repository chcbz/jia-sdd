#!/usr/bin/env python3
"""Read-only SDD document navigation checks; not YAML schema or release validation."""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

REQUIRED = ('spec.md', 'design.md', 'tasks.md', 'acceptance.md', 'integration.yaml')
NAV_KEYS = {'current_design', 'current_plan', 'current_acceptance',
            'current_optimization', 'clarifications', 'v1_10_plan', 'previous_design'}
LINK = re.compile(r'(?<!!)\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)')


def without_fences(text):
    lines = []
    fence = None
    for line in text.splitlines():
        mark = re.match(r'^\s*(`{3,}|~{3,})', line)
        if mark:
            token = mark.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append('')
        else:
            lines.append('' if fence else line)
    return '\n'.join(lines)


def check(root, feature=None):
    root = Path(root).resolve()
    errors, exceptions = [], []
    checked = set()
    links = 0
    mapping_path = root / 'docs/sdd-document-map.json'
    mapping = json.loads(mapping_path.read_text())
    removed = mapping['removed']
    for old, new in removed.items():
        if (root / old).exists():
            errors.append('Removed path reappeared: ' + old)
        if not (root / new).exists():
            errors.append('Missing successor: ' + new)
    if feature:
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', feature):
            raise ValueError('Invalid feature ID')
        dirs = [root / 'specs' / feature]
        if not dirs[0].is_dir():
            raise ValueError('Unknown feature: ' + feature)
    else:
        dirs = sorted(p for p in (root / 'specs').iterdir()
                      if p.is_dir() and not p.is_symlink() and p.name != '_template')

    def target_exists(p, target):
        nonlocal links
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            return
        links += 1
        dest = p.parent / unquote(url.path)
        if not dest.exists():
            errors.append('{}: missing target {}'.format(p.relative_to(root), target))

    def markdown(p):
        if p in checked:
            return
        checked.add(p)
        if not p.is_file():
            errors.append('Missing entry: ' + str(p.relative_to(root)))
            return
        text = without_fences(p.read_text())
        for match in LINK.finditer(text):
            target_exists(p, match.group(1))
        # Root-relative / absolute references used by AGENTS and the prototype spec.
        # Bare historical filenames in prose are not current navigation contracts.
        for token in re.findall(r'`([^`\n]+)`', text):
            path = token.split('#')[0]
            relative = path[len(str(root)) + 1:] if path.startswith(str(root) + '/') else path
            if (p.name == 'AGENTS.md' or p.name == 'prototype-spec.md') and re.match(
                    r'^(?:docs/|api/docs/|ops/|specs/|web/prototypes/|\.\./|'
                    + re.escape(str(root)) + r'/)', path):
                if not any(c in path for c in (' ', '*', '<', '>')):
                    if not (p.parent / path).exists() and not (root / path).exists():
                        errors.append('{}: missing inline path {}'.format(p.relative_to(root), path))
            if relative in removed:
                errors.append('{}: deleted reference {} -> {}'.format(
                    p.relative_to(root), path, removed[relative]))

    for folder in dirs:
        role = mapping.get('feature_dispositions', {}).get(folder.name, {}).get('category')
        if role == '历史来源':
            exceptions.append(folder.name + ': source summary, not an implementation feature')
            markdown(folder / 'spec.md')
            continue
        for name in REQUIRED:
            p = folder / name
            if not p.is_file() or not p.stat().st_size:
                errors.append('Missing/empty artifact: ' + str(p.relative_to(root)))
            elif name.endswith('.md'):
                markdown(p)
        manifest = folder / 'integration.yaml'
        if manifest.is_file():
            # Deliberately only the established scalar navigation keys, not a YAML parser.
            # Pins, statuses, frozen evidence and arbitrary nested fields are never rewritten.
            for line in manifest.read_text().splitlines():
                match = re.match(r'^\s*([a-z_0-9]+):\s*(.*?)\s*$', line)
                if not match or match.group(1) not in NAV_KEYS:
                    continue
                value = re.split(r'\s+#', match.group(2), maxsplit=1)[0].strip().strip('\"\'')
                if not value or value in ('null', '~') or value.startswith(('[', '{', '*', '|', '>')):
                    errors.append('{}: unsupported navigation scalar {}'.format(
                        manifest.relative_to(root), match.group(1)))
                else:
                    target_exists(manifest, value)
        for name in ('README.md',):
            if (folder / name).is_file():
                markdown(folder / name)
        # The UI specification deliberately keeps its current detail in optimization/.
        if (folder / 'optimization/README.md').is_file():
            for p in sorted((folder / 'optimization').glob('*.md')):
                if p.name in ('README.md', 'spec.md', 'detailed-design.md', 'tasks.md', 'acceptance.md'):
                    markdown(p)
    if not feature:
        for name in ('AGENTS.md', 'api/AGENTS.md', 'web/AGENTS.md',
                     'docs/codex-project-map.md', 'docs/sdd-workflow.md',
                     'docs/knowledge-base/README.md', 'specs/README.md', 'specs/INDEX.md',
                     'web/prototypes/juyiting/specs/prototype-spec.md'):
            markdown(root / name)
    return {'scope': 'current document entries and scalar navigation only; not YAML schema, '
                     'historical snapshot links, source tests, candidate matching or release acceptance',
            'features_checked': len(dirs), 'markdown_files_checked': len(checked),
            'local_targets_checked': links, 'exceptions': exceptions, 'errors': sorted(set(errors)),
            'result': 'FAIL' if errors else 'DOCUMENT_NAVIGATION_PASS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('feature', nargs='?')
    args = parser.parse_args()
    try:
        result = check(Path(__file__).resolve().parents[2], args.feature)
    except (ValueError, OSError, KeyError) as error:
        print('Document check error: {}'.format(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    sys.exit(main())
