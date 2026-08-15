# relion-zarr-sta-client

Native client for the `relion-zarr-sta` container. Installs [py2rely](https://github.com/chanzuckerberg/py2rely)
and [zarr-particle-tools](https://github.com/czimaginginstitute/zarr-particle-tools) (orchestration
and job commands run natively; `sbatch` needs the host's own SLURM/identity setup and can't run
inside a container), and generates PATH shims that route RELION's binaries and zarr-particle-tools'
job commands through `apptainer exec` into the container. Job scripts written for a native install
work unmodified, no `apptainer exec` typed anywhere in the calling code.

`py2rely` and `zarr-particle-pipeline` are intentionally not shimmed: they call `sbatch`
themselves, which must run on the real host.

## Install

```
pip install git+https://github.com/czimaginginstitute/relion-docker.git#subdirectory=shims
```

## Usage

Pull or build a SIF first (e.g. `apptainer pull relion-zarr-sta.sif oras://ghcr.io/czimaginginstitute/relion-zarr-sta-sif:5.0-cuda12.8`), then:

```
relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin
export PATH="$HOME/relion-shims/bin:$PATH"
```

To also point py2rely's `python_load`/`relion_load` at the shim directory directly:

```
relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin --wire-py2rely
```

## Options

- `--bind PATH`: bind-mounted into the container at the same path (default: `/data`); set this to whatever shared storage path your data and SIF actually live under.
- `--env-name NAME`: micromamba env name inside the image for zarr-particle-tools' job commands (default: `relion-zarr-sta`).
