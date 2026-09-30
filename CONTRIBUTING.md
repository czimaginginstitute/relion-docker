# Contributing to relion-docker

Thank you for your interest in contributing to relion-docker!

## Ways to Contribute

- **Report bugs**: Open an issue describing the problem and how to reproduce it
- **Suggest features**: Open an issue describing what you'd like to see (e.g. a new CUDA/RELION
  version combination, an AreTomo3 image)
- **Improve documentation**: Fix typos, clarify instructions, or add examples
- **Fix bugs or add features**: Submit a pull request

## Development Setup

```bash
git clone git@github.com:czimaginginstitute/relion-docker.git
cd relion-docker
git lfs install && git lfs pull   # the vendored CTFFIND tarball is in Git LFS
```

Build locally (CUDA_ARCH as in CI):

```bash
docker build -f Dockerfile.relion --build-arg CUDA_ARCH=80 -t relion:test .
docker build -f Dockerfile.relion --build-arg RELION_REF=ver5.1 \
  --build-arg CUDA_ARCH='80-real;86-real;89-real;90-real;100-real;120-real;120-virtual' -t relion:test-5.1 .
docker build -f extras/Dockerfile.relion-zarr-sta -t relion-zarr-sta:test .
```

The zarr-sta build uses the published `ghcr.io/czimaginginstitute/relion` base; to use yours,
`docker tag relion:test ghcr.io/czimaginginstitute/relion:5.0-cuda12.8.0` first. To test with
Apptainer (same machine as Docker):

```bash
apptainer build relion-zarr-sta.sif docker-daemon://relion-zarr-sta:test
apptainer exec --nv relion-zarr-sta.sif relion_refine --version
```

`client/` is a separate Python package — see [`client/README.md`](client/README.md).

## Making Changes

1. Create a branch: `git checkout -b your-feature-branch`
2. Make your changes and build the affected image(s) locally to confirm they still build
3. Where practical, test the built image (`docker run` or `apptainer exec`) against a real
   command, not just that the build succeeds
4. Open a pull request against `main`, describing what changed and why, and how you tested it

CI builds the images on PRs that change them (zarr-sta against the published relion base). Pushes to `main` (and a weekly rebuild) publish the
images and SIFs, then scan them with Trivy; only `main` publishes.

### Commit / PR title convention

This repo uses [release-please](https://github.com/googleapis/release-please) to generate
CHANGELOG.md from PR titles, so PR titles should follow [Conventional
Commits](https://www.conventionalcommits.org/) (`feat: ...`, `fix: ...`, `docs: ...`, `chore:
...`, `ci: ...`, etc.) — this repo merges via squash, so the PR title becomes the commit message
release-please reads.

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [opensource@biohub.org](mailto:opensource@biohub.org).

## Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@biohub.org](mailto:security@biohub.org). Do not open a public issue.

## License

By contributing to relion-docker, you agree that your contributions will be licensed under the [MIT License](LICENSE.md).
