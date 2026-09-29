#!/usr/bin/env bash
# SIF publish helper (GHCR registry API; needs GH_TOKEN with packages read/write).
#   key <repo> <tag>            -> 12-char hash of the amd64 layers + runtime config (stable across cached rebuilds)
#   current <sif_repo> <tag> <key> -> exit 0 if <tag> and <tag>-src-<key> point at the same SIF
#   mark <sif_repo> <tag> <key>    -> add tag <tag>-src-<key> to the SIF currently at <tag>
# repos are "owner/name" on ghcr.io
set -euo pipefail
mode=$1 repo=$2 tag=$3 key=${4:-}
accept='application/vnd.oci.image.index.v1+json,application/vnd.docker.distribution.manifest.list.v2+json,application/vnd.oci.image.manifest.v1+json,application/vnd.docker.distribution.manifest.v2+json'
token=$(curl -fsS -u "x:${GH_TOKEN}" "https://ghcr.io/token?scope=repository:${repo}:pull,push" | jq -r .token)
api() { curl -fsS -H "Authorization: Bearer $token" -H "Accept: $accept" "$@"; }
digest() { api -I "https://ghcr.io/v2/${repo}/manifests/$1" 2>/dev/null | tr -d '\r' | awk -F': ' 'tolower($1)=="docker-content-digest"{print $2}'; }

case $mode in
  key)
    m=$(api "https://ghcr.io/v2/${repo}/manifests/${tag}")
    if jq -e '.manifests' >/dev/null <<<"$m"; then
      d=$(jq -r '[.manifests[] | select(.platform.architecture=="amd64")][0].digest' <<<"$m")
      m=$(api "https://ghcr.io/v2/${repo}/manifests/${d}")
    fi
    cfg=$(api "https://ghcr.io/v2/${repo}/blobs/$(jq -r .config.digest <<<"$m")" -L)
    { jq -r '.layers[].digest' <<<"$m"
      jq -cS '.config | {Env, User, WorkingDir, Entrypoint, Cmd}' <<<"$cfg"; } | sha256sum | cut -c1-12 ;;
  current)
    a=$(digest "$tag" || true); b=$(digest "${tag}-src-${key}" || true)
    [ -n "$a" ] && [ "$a" = "$b" ] ;;
  mark)
    ct=$(api -I "https://ghcr.io/v2/${repo}/manifests/${tag}" | tr -d '\r' | awk -F': ' 'tolower($1)=="content-type"{print $2}')
    api "https://ghcr.io/v2/${repo}/manifests/${tag}" \
      | curl -fsS -X PUT -H "Authorization: Bearer $token" -H "Content-Type: $ct" --data-binary @- \
          "https://ghcr.io/v2/${repo}/manifests/${tag}-src-${key}" ;;
  *) echo "unknown mode $mode" >&2; exit 2 ;;
esac
