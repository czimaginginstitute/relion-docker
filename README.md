# relion-docker

Ready-to-run RELION 5 images (with CUDA support) for Docker and Apptainer/HPC, including
`relion-zarr-sta`, a Subtomogram Averaging (STA) variant for CryoET Data Portal / SLURM
workflows. Images are published to [GitHub Container
Registry](https://github.com/orgs/czimaginginstitute/packages) and [Docker
Hub](https://hub.docker.com/r/jidaniel/relion).

This project is under active development.

## Quickstart: run relion-zarr-sta on your HPC cluster

Most HPC clusters don't provide Docker (no root access); use Apptainer instead.

1. Pull the pre-built SIF:

   ```
   apptainer pull relion-zarr-sta.sif oras://ghcr.io/czimaginginstitute/relion-zarr-sta-sif:5.0-cuda12.8
   ```

2. Install [`relion-zarr-sta-client`](shims/), which brings in py2rely and zarr-particle-tools
   (these run natively; `sbatch` needs the host's own SLURM setup), and wire it up:

   ```
   pip install git+https://github.com/czimaginginstitute/relion-docker.git#subdirectory=shims
   relion-zarr-sta-client --sif relion-zarr-sta.sif --out ~/relion-shims/bin --wire-py2rely
   ```

That's it: RELION and zarr-particle-tools' job commands now transparently run inside the
container when py2rely's SLURM job scripts call them. See [`shims/README.md`](shims/README.md)
for options.

## Running locally with Docker

```
docker pull ghcr.io/czimaginginstitute/relion:5.1-cuda12.8
docker run --gpus all -it --rm -v /path/to/your/data:/work ghcr.io/czimaginginstitute/relion:5.1-cuda12.8 /bin/bash
```

`-v /path/to/your/data:/work` bind-mounts a local directory into the container at `/work`. The
same applies to `relion-zarr-sta`:

```
docker pull ghcr.io/czimaginginstitute/relion-zarr-sta:5.0-cuda12.8.0
```

## Apptainer reference

Apptainer (formerly Singularity — `singularity` accepts the same commands) can pull and convert
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
apptainer exec --nv --bind /path/to/your/data:/work relion_5.1-cuda12.8.sif relion_refine --help
```

For `relion-zarr-sta` on a SLURM cluster, see the
[Quickstart](#quickstart-run-relion-zarr-sta-on-your-hpc-cluster) above for the shim-based
integration.

## Image reference

### relion

This is the base RELION Docker image, which contains RELION with CUDA support and is ready to be run out of the box. It includes all necessary dependencies and is built from an NVIDIA CUDA base image. The Dockerfile sets up the environment for RELION by installing required environments and software packages, including the required conda environment to run RELION, CTFFIND and OpenMPI.

Tags follow `<relion>-cuda<cuda>` and are built for the following combinations:

| RELION | CUDA 12.4 | CUDA 12.8 |
|--------|-----------|-----------|
| 5.0    | `5.0-cuda12.4` | `5.0-cuda12.8` |
| 5.1    | `5.1-cuda12.4` | `5.1-cuda12.8` |

CUDA kernels are compiled for Ampere through Blackwell GPUs. For RELION 5.1, the `cuda12.8` images emit native code for `sm_80/86/89/90/120` and the `cuda12.4` images cover `sm_80/86/89/90` natively (reaching Blackwell via forward-compatible PTX).

RELION 5.0 images are built for a single architecture, `sm_80`, with the rest of the fleet covered by forward-compatible PTX. This is a limitation of RELION 5.0's build system, which uses the older CMake `FindCUDA` and accepts only one `CUDA_ARCH` value; RELION 5.1 switched to `CMAKE_CUDA_ARCHITECTURES`, which takes a list and lets us emit native code for every architecture at once.

For all tags, see https://github.com/czimaginginstitute/relion-docker/pkgs/container/relion.

### relion-zarr-sta

This Docker image is a derived image from the base RELION image, designed for running Subtomogram Averaging (STA) with Zarr/S3-streamed tilt series, including data from the CryoET Data Portal (CDP). It includes the additional Python tools for these STA workflows:
- [py2rely](https://github.com/chanzuckerberg/py2rely): A Pythonic interface for automated RELION workflows for subtomogram averaging on SLURM HPC clusters.
- [zarr-particle-tools](https://github.com/czimaginginstitute/zarr-particle-tools): Subtomogram extraction, reconstruction, CTF refinement, and Bayesian polishing for local files and the CryoET Data Portal.

For all CUDA versions, see https://github.com/czimaginginstitute/relion-docker/pkgs/container/relion-zarr-sta.

## Licensing

relion-docker's own code is licensed under [MIT](LICENSE.md). The built images bundle
third-party software (RELION, CTFFIND, and others) under their own upstream licenses — see
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [opensource@biohub.org](mailto:opensource@biohub.org).

## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@biohub.org](mailto:security@biohub.org).
