#!/usr/bin/env python3
"""Check archived JUnit reports and source snapshots against a Git candidate.

This read-only check establishes evidence correspondence, not test coverage or
release acceptance. Tests must already have run and their limits remain applicable.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import xml.etree.ElementTree as ET


def relative_path(value):
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("Evidence paths must be relative and stay within their root")
    return str(path)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("observations", nargs="+", type=Path)
    args = parser.parse_args()
    candidate = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{args.candidate}^{{commit}}"],
        cwd=args.repo, text=True).strip()
    failures = []
    groups = []
    for observation in args.observations:
        data = json.loads(observation.read_text())
        totals = dict.fromkeys(("tests", "failures", "errors", "skipped"), 0)
        reports = data.get("reports", [])
        sources = data.get("source_sha256", {})
        if not reports or not sources:
            failures.append(f"{observation}: reports or source snapshots missing")
        for report in reports:
            path = observation.parent / relative_path(report["file"])
            raw = path.read_bytes()
            suite = ET.fromstring(raw)
            if digest(raw) != report["sha256"] or suite.attrib != report["suite"]:
                failures.append(f"{path}: report differs from observation")
            for key in totals:
                totals[key] += int(suite.get(key, "0"))
        if totals["tests"] <= 0 or any(totals[k] for k in ("failures", "errors", "skipped")):
            failures.append(f"{observation}: batch is empty, failed, or skipped")
        if "totals" in data and data["totals"] != totals:
            failures.append(f"{observation}: recorded totals differ from reports")
        for name, expected in sources.items():
            name = relative_path(name)
            result = subprocess.run(
                ["git", "show", f"{candidate}:{name}"], cwd=args.repo,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
            if result.returncode or digest(result.stdout) != expected:
                failures.append(f"{name}: archived source differs from candidate")
        groups.append({"observation": str(observation), "totals": totals,
                       "source_snapshots": len(sources)})
    print(json.dumps({"candidate": candidate, "groups": groups,
                      "correspondence_valid": not failures, "failures": failures,
                      "limit": "Source/report association only; no coverage or release verdict."},
                     ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, ET.ParseError,
            subprocess.CalledProcessError) as error:
        print(f"Evidence check failed: {type(error).__name__}", file=sys.stderr)
        sys.exit(2)
