#!/usr/bin/env python3
"""Delete unreferenced GHCR container versions.

Roots are tagged versions (sif mode: tags other than <tag>-src-<key>). Everything reachable
from a root (index children, and attestations whose subject is protected) is kept. Fails
closed: any listing/fetch inconsistency aborts without deleting.

  ghcr-prune.py --org ORG --package PKG --mode {cache,image,sif} --min-age-hours N [--delete]
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.github.com"
ACCEPT = ",".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])
SRC_TAG = re.compile(r"-src-[0-9a-f]{12}$")


def request(url, token, method="GET", accept="application/vnd.github+json", auth="Bearer"):
    req = urllib.request.Request(url, method=method, headers={
        "Authorization": f"{auth} {token}", "Accept": accept, "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
        return json.loads(body) if body else None, r.headers


def list_versions(org, pkg, token):
    out, page = [], 1
    while True:
        data, _ = request(f"{API}/orgs/{org}/packages/container/{pkg}/versions?per_page=100&page={page}", token)
        out += data
        if len(data) < 100:
            return out
        page += 1


def registry_token(org, pkg, gh_token):
    basic = base64.b64encode(f"x:{gh_token}".encode()).decode()
    data, _ = request(f"https://ghcr.io/token?scope=repository:{org}/{pkg}:pull", basic, auth="Basic")
    return data["token"]


def manifest(org, pkg, digest, reg_token):
    data, _ = request(f"https://ghcr.io/v2/{org}/{pkg}/manifests/{digest}", reg_token, accept=ACCEPT)
    return data


def is_root(v, mode):
    tags = v["metadata"]["container"]["tags"]
    if mode == "sif":
        return any(not SRC_TAG.search(t) for t in tags)
    return bool(tags)


def plan(org, pkg, mode, min_age, token):
    versions = list_versions(org, pkg, token)
    by_digest = {v["name"]: v for v in versions}
    reg = registry_token(org, pkg, token)
    protected, queue = set(), [v["name"] for v in versions if is_root(v, mode)]
    if not queue:
        raise SystemExit(f"{pkg}: no tagged versions found; refusing to prune")
    manifests = {}

    def fetch(d):
        if d not in manifests:
            manifests[d] = manifest(org, pkg, d, reg)
        return manifests[d]

    def walk():  # protect queued digests and their index children, recursively
        while queue:
            d = queue.pop()
            if d in protected:
                continue
            if d not in by_digest:
                raise SystemExit(f"{pkg}: referenced digest {d} not in version list; aborting")
            protected.add(d)
            queue.extend(c["digest"] for c in (fetch(d).get("manifests") or []))

    walk()
    # referrers (attestations, signatures) whose subject is protected, plus their children
    for d in by_digest:
        fetch(d)
    changed = True
    while changed:
        changed = False
        for d, m in manifests.items():
            if d not in protected and (m.get("subject") or {}).get("digest") in protected:
                queue.append(d)
                walk()
                changed = True

    cutoff = datetime.now(timezone.utc) - timedelta(hours=min_age)
    return [v for v in versions if v["name"] not in protected
            and datetime.fromisoformat(v["created_at"].replace("Z", "+00:00")) < cutoff], len(versions), len(protected)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--org", required=True)
    p.add_argument("--package", required=True)
    p.add_argument("--mode", choices=["cache", "image", "sif"], required=True)
    p.add_argument("--min-age-hours", type=float, required=True)
    p.add_argument("--delete", action="store_true", help="actually delete (default: dry run)")
    a = p.parse_args()
    token = os.environ["GH_TOKEN"]

    cands, total, prot = plan(a.org, a.package, a.mode, a.min_age_hours, token)
    print(f"{a.package}: {total} versions, {prot} protected, {len(cands)} to delete (delete={a.delete})")
    if not a.delete:
        for v in cands:
            print(f"  would delete {v['id']} {v['name'][:19]} {v['created_at']} {v['metadata']['container']['tags']}")
        return

    # re-check right before deleting; drop anything that became protected meanwhile
    recheck, _, _ = plan(a.org, a.package, a.mode, a.min_age_hours, token)
    ids = {v["id"] for v in recheck}
    for v in cands:
        if v["id"] not in ids:
            print(f"  skip {v['id']} (now protected)")
            continue
        try:
            request(f"{API}/orgs/{a.org}/packages/container/{a.package}/versions/{v['id']}", token, method="DELETE")
            print(f"  deleted {v['id']} {v['name'][:19]} {v['created_at']}")
        except urllib.error.HTTPError as e:
            print(f"  failed {v['id']}: {e.code} {e.reason}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
