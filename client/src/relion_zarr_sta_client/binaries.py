# zarr-particle-tools job commands (run via `micromamba run -n`). py2rely and zarr-particle-pipeline
# stay native: they call sbatch, which needs the host's SLURM setup.
ENV_BINS = [
    "zarr-particle-extract",
    "zarr-particle-reconstruct",
    "zarr-particle-ctfrefine",
    "zarr-particle-polish",
    "zarr-particle-tomograms",
    "zarr-particle-export",
]
