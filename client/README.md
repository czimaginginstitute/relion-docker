# relion-zarr-sta-client

Makes the `relion-zarr-sta` container's binaries usable as if installed natively. It writes one
wrapper script per binary (`mpirun`, every `relion_*` in the image, and zarr-particle-tools' job
commands), each named like the real binary and running it via `apptainer exec` in the SIF. Put
the wrapper folder first on `PATH` and anything that calls those names (you, SLURM job scripts,
py2rely) runs them in the container.

It also installs [py2rely](https://github.com/chanzuckerberg/py2rely) and
[zarr-particle-tools](https://github.com/czimaginginstitute/zarr-particle-tools) natively:
`py2rely` and `zarr-particle-pipeline` call `sbatch`, which needs the host's SLURM.

## Install

Requires Python ≥3.10 and `apptainer` (or `singularity`) on `PATH`, on the login node and the
compute nodes; the wrappers call whichever one the client found.

```
pip install git+https://github.com/czimaginginstitute/relion-docker.git#subdirectory=client
```

## Usage

Pull the SIF first (see the main README's Quickstart), then:

```
relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin --bind /path/to/shared/storage
export PATH="$HOME/relion-shims/bin:$PATH"
```

Add `--wire-py2rely` to make py2rely's SLURM jobs use the wrappers. It **replaces** py2rely's
`python_load`/`relion_load` with the `export PATH=…` line; to keep module/venv lines, re-run
`py2rely config add` and enter them together with that line.

## Options

- `--sif PATH` (required): the relion-zarr-sta SIF.
- `--out DIR` (required): a dedicated directory for the wrappers. Files the client didn't write
  that share a wrapper's name make the run error unless `--force`; stale wrappers are removed.
- `--bind PATH`: host path to mount at the same path inside (repeatable; none by default). Must
  exist; can't contain `,` or `:`.
- `--env-name NAME`: env name for zarr-particle-tools commands (default: `relion-zarr-sta`).
- `--force`: replace existing files or symlinks in `--out` (never a symlink's target or a directory).
- `--wire-py2rely`: see above.

Wrappers ignore the host's `PYTHONPATH` and `~/.local` site-packages.
