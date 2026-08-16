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
```

Build an image locally:

```bash
docker build -f Dockerfile.relion -t relion:test .
docker build -f extras/Dockerfile.relion-zarr-sta -t relion-zarr-sta:test .
```

On a machine without Docker (e.g. testing the HPC path), convert and run with Apptainer instead:

```bash
apptainer build relion-zarr-sta.sif docker-daemon://relion-zarr-sta:test
apptainer exec --nv relion-zarr-sta.sif relion_refine --version
```

`client/` is a separate Python package — see [`client/README.md`](client/README.md) for its own
development notes.

## Making Changes

1. Create a branch: `git checkout -b your-feature-branch`
2. Make your changes and build the affected image(s) locally to confirm they still build
3. Where practical, test the built image (`docker run` or `apptainer exec`) against a real
   command, not just that the build succeeds
4. Open a pull request against `main`, describing what changed and why, and how you tested it

CI builds every image on pull requests that touch it, and (on merge to `main`) pushes the images
and publishes their SIFs.

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
