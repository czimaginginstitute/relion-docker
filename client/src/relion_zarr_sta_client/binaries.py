# Binaries on the container's system PATH (RELION + mpirun), called directly.
SYSTEM_BINS = [
    "mpirun",
    "relion_refine",
    "relion_refine_mpi",
    "relion_mask_create",
    "relion_postprocess",
    "relion_tomo_refine_ctf",
    "relion_tomo_align",
    "relion_reconstruct",
    "relion_reconstruct_mpi",
]

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
