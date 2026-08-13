# relion-docker-shims

Generates thin PATH wrapper scripts that route native command invocations
(`mpirun`, `relion_refine_mpi`, `py2rely`, `zarr-particle-*`, etc.) through
`apptainer exec` into a relion-docker image. This lets SLURM job scripts and
tools like [py2rely](https://github.com/chanzuckerberg/py2rely) that expect a
native install work unmodified against the container — no `apptainer exec`
typed anywhere in the calling code.

## Install

```
pip install git+https://github.com/czimaginginstitute/relion-docker.git#subdirectory=shims
```

## Usage

Pull or build a SIF first (e.g. `apptainer pull relion-zarr-sta.sif oras://ghcr.io/czimaginginstitute/relion-zarr-sta-sif:5.0-cuda12.8`), then:

```
relion-docker-shims --sif relion-zarr-sta.sif --out ~/relion-shims/bin
export PATH="$HOME/relion-shims/bin:$PATH"
```

To also point py2rely's `python_load`/`relion_load` at the shim directory
directly (requires `py2rely` on PATH):

```
relion-docker-shims --sif relion-zarr-sta.sif --out ~/relion-shims/bin --wire-py2rely
```

## Options

- `--bind PATH` — bind-mounted into the container at the same path (default: `/data`); set this to whatever shared storage path your data and SIF actually live under.
- `--env-name NAME` — micromamba env name inside the image for env-only CLIs like `py2rely` (default: `relion-zarr-sta`).
