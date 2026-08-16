# relion-zarr-sta-client

Makes the `relion-zarr-sta` container's binaries usable as if they were installed natively.
Running the command below generates one small wrapper script per binary (`relion_refine_mpi`,
`zarr-particle-extract`, etc.), named exactly like the real thing, and put on `PATH`. Whatever
calls that name, a SLURM job script, py2rely, or you in a shell, can't tell it's not the real
binary; each wrapper just runs `apptainer exec relion-zarr-sta.sif <binary> "$@"` and hands off
whatever arguments it was given. The actual binary never has to exist on the host.

It also installs [py2rely](https://github.com/chanzuckerberg/py2rely) and
[zarr-particle-tools](https://github.com/czimaginginstitute/zarr-particle-tools) as real
dependencies, so they run natively rather than through a wrapper. That's deliberate: `py2rely`
and `zarr-particle-pipeline` call `sbatch` to submit jobs, and `sbatch` needs the host's own
SLURM setup, which can't run inside a container. Once a submitted job is actually running, its
RELION and job-binary calls go through the wrappers into the container as usual.

## Install

```
pip install git+https://github.com/czimaginginstitute/relion-docker.git#subdirectory=client
```

## Usage

Pull or build a SIF first (e.g. `apptainer pull relion-zarr-sta.sif oras://ghcr.io/czimaginginstitute/relion-zarr-sta-sif:5.0-cuda12.8`), then:

```
relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin
export PATH="$HOME/relion-shims/bin:$PATH"
```

To also point py2rely's `python_load`/`relion_load` at the wrapper directory directly:

```
relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin --wire-py2rely
```

## Options

- `--bind PATH`: bind-mounted into the container at the same path (default: `/data`); set this to whatever shared storage path your data and SIF actually live under.
- `--env-name NAME`: micromamba env name inside the image for zarr-particle-tools' job commands (default: `relion-zarr-sta`).
