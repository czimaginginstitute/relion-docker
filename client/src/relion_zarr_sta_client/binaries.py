# zarr-particle-tools job binaries that live inside the image's micromamba env, need
# `micromamba run -n`. py2rely and zarr-particle-pipeline are deliberately excluded: they call
# `sbatch` themselves, which needs the host's SLURM/identity setup and doesn't work run this way.
ENV_BINS = [
    "zarr-particle-extract",
    "zarr-particle-reconstruct",
    "zarr-particle-ctfrefine",
    "zarr-particle-polish",
    "zarr-particle-tomograms",
    "zarr-particle-export",
]
