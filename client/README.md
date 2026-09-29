# relion-zarr-sta-client

Makes the `relion-zarr-sta` container's binaries usable as if they were installed natively.
Running the command below generates one small wrapper script per binary (`mpirun`, every
`relion_*` binary in the image, and the zarr-particle-tools job commands, e.g. `relion_refine_mpi`,
`zarr-particle-extract`, etc.), named exactly like the real thing; you put that folder first on
`PATH`. Whatever calls that name, a SLURM job script, py2rely, or you in a shell, can't tell it's
not the real binary; each wrapper runs `apptainer exec --nv [--bind …] /abs/path.sif <binary> "$@"`
(zarr-particle-tools commands via `micromamba run -n relion-zarr-sta`). The actual binary never
has to exist on the host.

It also installs [py2rely](https://github.com/chanzuckerberg/py2rely) and
[zarr-particle-tools](https://github.com/czimaginginstitute/zarr-particle-tools) as real
dependencies, so `py2rely` and `zarr-particle-pipeline` run natively. That's deliberate: they
call `sbatch` to submit jobs, and `sbatch` needs the host's own SLURM setup, which can't run
inside a container. zarr-particle-tools' job commands (extract, reconstruct, ctfrefine, polish,
tomograms, export) are also installed natively but go through the wrappers, so the wrapper folder
must come first on `PATH`.

## Install

Requires Python ≥3.10.

```
pip install git+https://github.com/czimaginginstitute/relion-docker.git#subdirectory=client
```

## Usage

Pull or build a SIF first (e.g. `apptainer pull relion-zarr-sta.sif oras://ghcr.io/czimaginginstitute/relion-zarr-sta-sif:5.0-cuda12.8`), then:

```
relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin --bind /path/to/shared/storage
export PATH="$HOME/relion-shims/bin:$PATH"
```

To also make py2rely's SLURM job scripts use the wrappers, add `--wire-py2rely`. It runs
`py2rely config import`, which **replaces** py2rely's `python_load`/`relion_load` with the
`export PATH=…` line. To keep module/venv lines, re-run `py2rely config add` afterwards and enter
them **together with** the `export PATH=…` line (it replaces each value, it doesn't append).

## Options

- `--sif PATH` (required): the relion-zarr-sta SIF; must exist. Stored as an absolute path
  (symlinks resolved). The client lists its `relion_*` binaries with `apptainer exec`; without
  Apptainer it wraps a default set.
- `--out DIR` (required): directory to write the wrappers to.
- `--bind PATH`: host path bind-mounted into the container at the same path (repeatable; none by default); must exist. Set this to the shared storage your data lives under.
Stored as an absolute path as typed (symlinks aren't resolved); can't contain `,` or `:`.
- `--env-name NAME`: micromamba env name inside the image for zarr-particle-tools' job commands (default: `relion-zarr-sta`).
- `--wire-py2rely`: also point py2rely's `python_load`/`relion_load` at the wrapper directory (see above).
