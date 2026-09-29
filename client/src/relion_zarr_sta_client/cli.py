from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from .binaries import ENV_BINS, SYSTEM_BINS

SHIM_TEMPLATE = """#!/bin/bash
exec apptainer exec --nv {binds}{sif} {invocation} "$@"
"""


def _write_shim(outdir: Path, name: str, sif: Path, binds: list[str], invocation: list[str]) -> None:
    path = outdir / name
    bind_args = "".join(f"--bind {shlex.quote(f'{b}:{b}')} " for b in binds)
    path.write_text(
        SHIM_TEMPLATE.format(
            binds=bind_args, sif=shlex.quote(str(sif)), invocation=shlex.join(invocation)
        )
    )
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def generate_shims(sif: Path, outdir: Path, binds: list[str], env_name: str) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    for name in SYSTEM_BINS:
        _write_shim(outdir, name, sif, binds, [name])
    for name in ENV_BINS:
        _write_shim(outdir, name, sif, binds, ["micromamba", "run", "-n", env_name, name])
    return len(SYSTEM_BINS) + len(ENV_BINS)


def wire_py2rely(outdir: Path) -> None:
    if shutil.which("py2rely") is None:
        print(
            "error: --wire-py2rely requires the `py2rely` CLI to be on PATH "
            "(it's a dependency of this package -- check your install)",
            file=sys.stderr,
        )
        raise SystemExit(1)

    path_line = f'export PATH={shlex.quote(str(outdir))}:"$PATH"'
    config = {"python_load": path_line, "relion_load": path_line}

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        tmp_path = f.name

    try:
        subprocess.run(["py2rely", "config", "import", tmp_path], check=True)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="relion-zarr-sta-client",
        description=(
            "Native client for relion-zarr-sta. Installs py2rely and zarr-particle-tools "
            "(py2rely and zarr-particle-pipeline run natively -- sbatch needs the host's SLURM "
            "setup) and generates PATH shims that route RELION and zarr-particle-tools job "
            "binaries through `apptainer exec` into the container, so job scripts written for "
            "a native install work unmodified."
        ),
    )
    parser.add_argument("--sif", required=True, help="path to the .sif image")
    parser.add_argument(
        "--out", required=True, help="output directory for shim scripts (add this to PATH)"
    )
    parser.add_argument(
        "--bind",
        action="append",
        default=[],
        help="host path to bind into the container at the same path (repeatable); "
        "e.g. the shared storage your data lives under",
    )
    parser.add_argument(
        "--env-name",
        default="relion-zarr-sta",
        help="micromamba env name inside the image for env-only CLIs (default: %(default)s)",
    )
    parser.add_argument(
        "--wire-py2rely",
        action="store_true",
        help="also point py2rely's python_load/relion_load at the generated shim "
        "directory via `py2rely config import`",
    )
    args = parser.parse_args()

    sif = Path(args.sif).expanduser().resolve()
    if not sif.is_file():
        parser.error(f"--sif {args.sif}: no such file")
    # absolute but not symlink-resolved, so job scripts can use the path as typed
    binds = [os.path.abspath(os.path.expanduser(b)) for b in args.bind]
    missing = [b for b in binds if not Path(b).exists()]
    if missing:
        parser.error(f"--bind path(s) not found: {', '.join(missing)}")
    bad = [b for b in binds if "," in b or ":" in b]
    if bad:
        parser.error(f"--bind paths can't contain ',' or ':': {', '.join(bad)}")

    outdir = Path(args.out).expanduser().resolve()
    count = generate_shims(sif, outdir, binds, args.env_name)
    print(f"Generated {count} shims in {outdir}")

    if args.wire_py2rely:
        wire_py2rely(outdir)
        print("Wired py2rely's python_load/relion_load to the shim directory")
    else:
        print(f"Add to PATH (or set py2rely's python_load/relion_load to): export PATH={shlex.quote(str(outdir))}:\"$PATH\"")


if __name__ == "__main__":
    main()
