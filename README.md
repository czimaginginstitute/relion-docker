# relion-docker

Ready-to-run RELION 5 images (with CUDA support) for Docker and Apptainer/HPC, including
`relion-zarr-sta`, a Subtomogram Averaging (STA) variant for CryoET Data Portal / SLURM
workflows. Images are published to [GitHub Container
Registry](https://github.com/orgs/czimaginginstitute/packages) and Docker Hub
([relion](https://hub.docker.com/r/jidaniel/relion),
[relion-zarr-sta](https://hub.docker.com/r/jidaniel/relion-zarr-sta)).

Requirements: an NVIDIA GPU with compute capability 8.0+ (A100 or newer; V100/T4 and older are
not supported) and a host driver that supports the image's CUDA version (≥570 for `cuda12.8`,
≥550 for `cuda12.4`).

This project is under active development.

## Contents

- [Quickstart: run relion-zarr-sta on your HPC cluster](#quickstart-run-relion-zarr-sta-on-your-hpc-cluster)
- [Running locally with Docker](#running-locally-with-docker)
- [Apptainer reference](#apptainer-reference)
- [Image reference](#image-reference)
- [Licensing](#licensing)

## Quickstart: run relion-zarr-sta on your HPC cluster

Most HPC clusters don't provide Docker (no root access); use Apptainer instead.

1. Pull the pre-built SIF:

   ```
   apptainer pull relion-zarr-sta.sif oras://ghcr.io/czimaginginstitute/relion-zarr-sta-sif:5.0-cuda12.8
   ```

2. Install [`relion-zarr-sta-client`](client/), which brings in py2rely and zarr-particle-tools
   (these run natively; `sbatch` needs the host's own SLURM setup), and wire it up:

   ```
   pip install git+https://github.com/czimaginginstitute/relion-docker.git#subdirectory=client
   relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin \
       --bind /path/to/shared/storage --wire-py2rely
   export PATH="$HOME/relion-shims/bin:$PATH"
   ```

   `--bind` is the storage your data lives on (repeatable). Put the SIF and the wrapper folder on
   storage the compute nodes can see. Requires Python ≥3.10.

RELION and zarr-particle-tools' job commands now run inside the container, both when you call
them and when py2rely's SLURM job scripts do. `--wire-py2rely` **replaces** py2rely's
`python_load`/`relion_load` with the `export PATH` line, dropping any existing module/venv lines
(see [`client/README.md`](client/README.md)).

### What the client actually does

Step 2 above generates a folder of small wrapper scripts: `mpirun`, every `relion_*` binary in
the image, and the zarr-particle-tools job commands (e.g. `relion_refine_mpi`,
`zarr-particle-extract`); you put that folder first on `PATH`. Each wrapper has
the same name as the real binary, so anything that calls that name (a SLURM job script, py2rely,
you typing it in a shell) can't tell the difference; it just runs. Under the hood, the wrapper
runs `apptainer exec --nv [--bind …] /abs/path/relion-zarr-sta.sif <the real binary> "$@"`
(zarr-particle-tools commands via `micromamba run -n relion-zarr-sta`), passing through whatever
arguments it was called with. So the binary itself never has to exist natively on the machine;
the wrapper stands in for it and transparently hands the work to the container.

`py2rely` and `zarr-particle-pipeline` themselves are not wrapped this way, because they call
`sbatch` to submit jobs, and `sbatch` needs the real host's SLURM setup; that can't run inside a
container. So those two run natively (installed by `relion-zarr-sta-client` as real dependencies),
and only reach into the container for the actual RELION/job binaries once a job is running. See
[`client/README.md`](client/README.md) for the full option list.

MPI runs are limited to a single node: `mpirun` runs the container's OpenMPI inside one
`apptainer exec`.

## Running locally with Docker

```
docker pull ghcr.io/czimaginginstitute/relion:5.1-cuda12.8
docker run --gpus all -it --rm -v /path/to/your/data:/work ghcr.io/czimaginginstitute/relion:5.1-cuda12.8 /bin/bash
```

`-v /path/to/your/data:/work` bind-mounts a local directory into the container at `/work`. The
container runs as UID 1000 (`relion`), so the directory must be writable by it (or add
`--user $(id -u):$(id -g) -e HOME=/work`, so model-weight downloads have a writable home). The same applies to `relion-zarr-sta`:

```
docker pull ghcr.io/czimaginginstitute/relion-zarr-sta:5.0-cuda12.8.0
```

## Apptainer reference

Apptainer (formerly Singularity; `singularity` accepts the same commands) can pull and convert
these images directly. Note it consumes the built image, not the Dockerfile:

```
apptainer pull docker://ghcr.io/czimaginginstitute/relion:5.1-cuda12.8
```

Pre-built SIFs are also published directly, under `relion-sif` and `relion-zarr-sta-sif`:

```
apptainer pull oras://ghcr.io/czimaginginstitute/relion-sif:5.1-cuda12.8
apptainer pull oras://ghcr.io/czimaginginstitute/relion-zarr-sta-sif:5.0-cuda12.8
```

Run with GPU access (`--nv`) and your data bind-mounted:

```
apptainer exec --nv --bind /path/to/your/data:/work --pwd /work relion_5.1-cuda12.8.sif relion_refine --help
```

The SIF filename depends on the pull: `docker://` saves `relion_5.1-cuda12.8.sif`, `oras://` saves
`relion-sif_5.1-cuda12.8.sif` (or pass a name as the first argument).

For `relion-zarr-sta` on a SLURM cluster, see the
[Quickstart](#quickstart-run-relion-zarr-sta-on-your-hpc-cluster) above for the client-based
integration.

## Image reference

### relion

The base image: RELION with CUDA, RELION's conda environment, CTFFIND and OpenMPI, on an NVIDIA
CUDA base image. It's a headless build (no `relion` GUI). Model weights for Blush, ModelAngelo,
classranker etc. download on first use, so the first run needs internet access.

Tags follow `<relion>-cuda<X.Y>` (Docker images are also pushed as `-cuda<X.Y.Z>`, e.g.
`5.0-cuda12.4.1`; SIFs use `-cuda<X.Y>` only, plus internal `<tag>-src-<hash>` tags — pull the
plain tag) and are
built for the following combinations:

| RELION | CUDA 12.4 | CUDA 12.8 |
|--------|-----------|-----------|
| 5.0    | `5.0-cuda12.4` | `5.0-cuda12.8` |
| 5.1    | — | `5.1-cuda12.8` |

`relion-zarr-sta` (and its SIF) is built for RELION 5.0 only: `5.0-cuda12.4`, `5.0-cuda12.8`.
Tags not listed here are legacy and are no longer rebuilt or scanned.

Tags are rolling: images rebuild weekly from the upstream `ver5.0`/`ver5.1` branches (for apt
security fixes and upstream changes). The exact RELION commit is in
`/opt/licenses/RELION-SOURCE-COMMIT.txt` and the `org.relion.source.revision` label. A weekly
cleanup deletes superseded digests from GHCR once they're 14+ days old, counted from when they
were built; with weekly rebuilds that's usually about a week after they're replaced. For
long-term reproducibility keep your own copy (`docker save`, or the pulled `.sif`).

RELION 5.1 images emit native code for `sm_80/86/89/90/100/120` (Ampere through Blackwell, incl.
B200/GB200) plus `compute_120` PTX. RELION 5.0 images are built for `sm_80` only, with newer GPUs
covered by PTX JIT: RELION 5.0 uses CMake's older `FindCUDA`, which accepts a single `CUDA_ARCH`.

For all tags, see https://github.com/orgs/czimaginginstitute/packages/container/package/relion.

### relion-zarr-sta

This Docker image is a derived image from the base RELION image, designed for running Subtomogram Averaging (STA) with Zarr/S3-streamed tilt series, including data from the CryoET Data Portal (CDP). It includes the additional Python tools for these STA workflows:
- [py2rely](https://github.com/chanzuckerberg/py2rely): A Pythonic interface for automated RELION workflows for subtomogram averaging on SLURM HPC clusters.
- [zarr-particle-tools](https://github.com/czimaginginstitute/zarr-particle-tools): Subtomogram extraction, reconstruction, CTF refinement, and Bayesian polishing for local files and the CryoET Data Portal.

It starts in `/work` and runs as UID 1000, like `relion`. For all tags, see
https://github.com/orgs/czimaginginstitute/packages/container/package/relion-zarr-sta.

## Licensing

relion-docker's own code is licensed under [MIT](LICENSE.md). The built images bundle
third-party software (RELION, CTFFIND, and others) under their own upstream licenses; see
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [opensource@biohub.org](mailto:opensource@biohub.org).

## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@biohub.org](mailto:security@biohub.org).
