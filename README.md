# relion-docker

Ready-to-run RELION 5 images (with CUDA support) for Docker and Apptainer/HPC, including
`relion-zarr-sta`, a Subtomogram Averaging (STA) variant for CryoET Data Portal / SLURM
workflows. Images are published to [GitHub Container
Registry](https://github.com/orgs/czimaginginstitute/packages) and Docker Hub
([relion](https://hub.docker.com/r/jidaniel/relion),
[relion-zarr-sta](https://hub.docker.com/r/jidaniel/relion-zarr-sta)).

Needs an NVIDIA GPU with compute capability 8.0+ (A100 or newer) and a driver ≥570 (`cuda12.8`)
or ≥550 (`cuda12.4`). This project is under active development.

## Contents

- [Quickstart: run relion-zarr-sta on your HPC cluster](#quickstart-run-relion-zarr-sta-on-your-hpc-cluster)
- [Running locally with Docker](#running-locally-with-docker)
- [Apptainer reference](#apptainer-reference)
- [Image reference](#image-reference)
- [Licensing](#licensing)

## Quickstart: run relion-zarr-sta on your HPC cluster

Most HPC clusters don't provide Docker; use Apptainer.

1. Pull the pre-built SIF:

   ```
   apptainer pull relion-zarr-sta.sif oras://ghcr.io/czimaginginstitute/relion-zarr-sta-sif:5.0-cuda12.8
   ```

2. Install [`relion-zarr-sta-client`](client/) (Python ≥3.10) and generate the wrappers:

   ```
   pip install git+https://github.com/czimaginginstitute/relion-docker.git#subdirectory=client
   relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin \
       --bind /path/to/shared/storage --wire-py2rely
   export PATH="$HOME/relion-shims/bin:$PATH"
   ```

RELION and zarr-particle-tools job commands now run inside the container, whether you call them
or py2rely's SLURM jobs do; py2rely and `zarr-particle-pipeline` run natively so `sbatch` works.
Keep the SIF, the wrappers and the client's Python env on storage the compute nodes can see, with
`apptainer` on `PATH` there too. `--wire-py2rely` replaces py2rely's `python_load`/`relion_load` (existing module/venv lines are dropped).
MPI runs are single-node. Details: [`client/README.md`](client/README.md).

## Running locally with Docker

```
docker run --gpus all -it --rm -v /path/to/your/data:/work ghcr.io/czimaginginstitute/relion:5.1-cuda12.8 /bin/bash
```

The container runs as UID 1000, so the mounted directory must be writable by it (or add
`--user $(id -u):$(id -g) -e HOME=/work`). `relion-zarr-sta` works the same way.

## Apptainer reference

Pull the Docker image, or the pre-built SIFs (`relion-sif`, `relion-zarr-sta-sif`):

```
apptainer pull relion.sif oras://ghcr.io/czimaginginstitute/relion-sif:5.1-cuda12.8
# or: apptainer pull relion.sif docker://ghcr.io/czimaginginstitute/relion:5.1-cuda12.8
apptainer exec --nv --bind /path/to/your/data:/work --pwd /work relion.sif relion_refine --help
```

## Image reference

**relion**: RELION with CUDA, its conda environment, CTFFIND and OpenMPI. Headless (no GUI);
model weights (Blush, ModelAngelo, …) download on first use, so the first run needs internet.

**relion-zarr-sta**: `relion` plus [py2rely](https://github.com/chanzuckerberg/py2rely) and
[zarr-particle-tools](https://github.com/czimaginginstitute/zarr-particle-tools), for
subtomogram averaging with Zarr/S3-streamed tilt series, including CryoET Data Portal data.

| Image | CUDA 12.4 | CUDA 12.8 |
|-------|-----------|-----------|
| relion 5.0 | `5.0-cuda12.4` | `5.0-cuda12.8` |
| relion 5.1 | — | `5.1-cuda12.8` |
| relion-zarr-sta (5.0) | `5.0-cuda12.4` | `5.0-cuda12.8` |

- Docker tags also exist as `-cuda<X.Y.Z>`; SIF packages also carry internal `-src-<hash>` tags
  (pull the plain tag). Unlisted tags are legacy and no longer rebuilt or scanned.
- Tags are rebuilt weekly from upstream `ver5.0`/`ver5.1`; the RELION commit is in
  `/opt/licenses/RELION-SOURCE-COMMIT.txt`. Superseded digests are deleted from GHCR 14+ days
  after they were built, so keep your own copy (`docker save`, or the `.sif`) for reproducibility.
- GPUs: 5.1 has native code for `sm_80/86/89/90/100/120`; 5.0 is `sm_80` plus PTX (RELION 5.0
  accepts one arch).

All tags: [relion](https://github.com/orgs/czimaginginstitute/packages/container/package/relion),
[relion-zarr-sta](https://github.com/orgs/czimaginginstitute/packages/container/package/relion-zarr-sta).

## Licensing

relion-docker's own code is licensed under [MIT](LICENSE.md). The built images bundle
third-party software (RELION, CTFFIND, and others) under their own upstream licenses; see
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [opensource@biohub.org](mailto:opensource@biohub.org).

## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@biohub.org](mailto:security@biohub.org).
