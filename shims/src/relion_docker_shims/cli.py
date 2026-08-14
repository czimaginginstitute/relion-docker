import argparse
import json
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from .binaries import ENV_BINS, SYSTEM_BINS

SHIM_TEMPLATE = """#!/bin/bash
exec apptainer exec --nv --bind "{bind}:{bind}" "{sif}" {invocation} "$@"
"""


def _write_shim(outdir: Path, name: str, sif: str, bind: str, invocation: str) -> None:
    path = outdir / name
    path.write_text(SHIM_TEMPLATE.format(bind=bind, sif=sif, invocation=invocation))
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def generate_shims(sif: str, outdir: Path, bind: str, env_name: str) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    for name in SYSTEM_BINS:
        _write_shim(outdir, name, sif, bind, name)
    for name in ENV_BINS:
        _write_shim(outdir, name, sif, bind, f"micromamba run -n {env_name} {name}")
    return len(SYSTEM_BINS) + len(ENV_BINS)


def wire_py2rely(outdir: Path) -> None:
    if shutil.which("py2rely") is None:
        print(
            "error: --wire-py2rely requires the `py2rely` CLI to be on PATH "
            "(pip install py2rely first)",
            file=sys.stderr,
        )
        raise SystemExit(1)

    path_line = f'export PATH="{outdir}:$PATH"'
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
        prog="relion-docker-shims",
        description=(
            "Generate PATH shims that transparently route native command invocations "
            "(mpirun, relion_*, py2rely, zarr-particle-*) through `apptainer exec` into "
            "a relion-docker image, so SLURM job scripts written for a native install "
            "work unmodified against the container."
        ),
    )
    parser.add_argument("--sif", required=True, help="path to the .sif image")
    parser.add_argument(
        "--out", required=True, help="output directory for shim scripts (add this to PATH)"
    )
    parser.add_argument(
        "--bind",
        default="/data",
        help="bind path passed to apptainer exec, mounted at the same path inside the "
        "container (default: %(default)s) -- set this to whatever shared storage path "
        "your data and SIF actually live under",
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

    outdir = Path(args.out).expanduser().resolve()
    count = generate_shims(args.sif, outdir, args.bind, args.env_name)
    print(f"Generated {count} shims in {outdir}")

    if args.wire_py2rely:
        wire_py2rely(outdir)
        print("Wired py2rely's python_load/relion_load to the shim directory")
    else:
        print(f'To use with py2rely, set python_load/relion_load to: export PATH="{outdir}:$PATH"')


if __name__ == "__main__":
    main()
