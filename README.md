# relion-docker

Docker images for [RELION](https://relion.readthedocs.io/en/latest/) (5.0 and 5.1) with CUDA support. Uses GitHub Actions to automate building and pushing of images to GitHub Container Registry at https://github.com/orgs/czimaginginstitute/packages and DockerHub at https://hub.docker.com/r/jidaniel/relion.

## Docker images

### relion

This is the base RELION Docker image, which contains RELION with CUDA support and is ready to be run out of the box. It includes all necessary dependencies and is built from an NVIDIA CUDA base image. The Dockerfile sets up the environment for RELION by installing required environments and software packages, including the required conda environment to run RELION, CTFFIND and OpenMPI.

Tags follow `<relion>-cuda<cuda>` and are built for the following combinations:

| RELION | CUDA 12.4 | CUDA 12.8 |
|--------|-----------|-----------|
| 5.0    | `5.0-cuda12.4` | `5.0-cuda12.8` |
| 5.1    | `5.1-cuda12.4` | `5.1-cuda12.8` |

CUDA kernels are compiled for Ampere through Blackwell GPUs. For RELION 5.1, the `cuda12.8` images emit native code for `sm_80/86/89/90/120` and the `cuda12.4` images cover `sm_80/86/89/90` natively (reaching Blackwell via forward-compatible PTX).

RELION 5.0 images are built for a single architecture, `sm_80`, with the rest of the fleet covered by forward-compatible PTX. This is a limitation of RELION 5.0's build system, which uses the older CMake `FindCUDA` and accepts only one `CUDA_ARCH` value; RELION 5.1 switched to `CMAKE_CUDA_ARCHITECTURES`, which takes a list and lets us emit native code for every architecture at once.

The image can be downloaded via: 

```
docker pull ghcr.io/czimaginginstitute/relion:5.1-cuda12.8
```

For all tags, see https://github.com/czimaginginstitute/relion-docker/pkgs/container/relion.

### cdp-relion-sta

This Docker image is a derived image from the base RELION image, designed for running Subtomogram Averaging (STA) from the CryoET Data Portal (CDP). It includes the additional Python tools for CDP RELION STA workflows:
- [pyrelion](https://github.com/czimaginginstitute/relion-sub-tomogram-pipelines): An interface for automated RELION workflows for subtomogram averaging.
- [octopi](https://github.com/chanzuckerberg/octopi): A deep learning framework to build 3D U-Net models for cryo-ET particle picking.
- [portal-particle-extraction](https://github.com/czimaginginstitute/portal-particle-extraction): A tool for subtomogram extraction and reconstruction from local files and the CryoET Data Portal.

The image can be downloaded via: 

```
docker pull ghcr.io/czimaginginstitute/cryoet-data-portal-relion-sta:5.0-cuda12.8.0
```

For all CUDA versions, see https://github.com/czimaginginstitute/relion-docker/pkgs/container/cryoet-data-portal-relion-sta.

## Mounting Data

When running Docker containers with RELION, it is often necessary to mount local directories to the container so that data can be accessed and processed. You can mount data by using the `-v` option when running the container. This allows you to specify a local directory to mount to a specific directory inside the container.

For example:

```
docker run --gpus all -it --rm -v /path/to/your/data:/work jidaniel/relion:5.0-cuda12.8 /bin/bash
```

In this case, `/path/to/your/data` is a local directory on your host machine, and `/work` is the directory inside the container where the data will be available.

The same approach can be used for mounting data in the `cdp-relion-sta` container.

## Apptainer / Singularity (HPC clusters)

Most HPC clusters don't provide Docker. Apptainer (formerly Singularity) can pull and convert these images directly — note it consumes the built image, not the Dockerfile:

```
apptainer pull docker://ghcr.io/czimaginginstitute/relion:5.1-cuda12.8
```

This produces `relion_5.1-cuda12.8.sif`. Run with GPU access (`--nv`) and your data bind-mounted:

```
apptainer exec --nv --bind /path/to/your/data:/work relion_5.1-cuda12.8.sif relion_refine --help
```

`singularity` accepts the same commands.

## Roadmap
- [ ] Add AreTomo3