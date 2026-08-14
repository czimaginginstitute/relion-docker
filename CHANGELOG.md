# Changelog

## [0.2.0](https://github.com/czimaginginstitute/relion-docker/compare/relion-docker-v0.1.0...relion-docker-v0.2.0) (2026-08-14)


### ✨ Features

* add RELION 5.1 builds and explicit CUDA arch targeting ([ef04fd6](https://github.com/czimaginginstitute/relion-docker/commit/ef04fd6dd7b058841af7a64530655d7cba0053b8))


### 🐞 Bug Fixes

* clean up LICENSE.md for detection, pin third-party Actions to SHAs ([5752558](https://github.com/czimaginginstitute/relion-docker/commit/5752558a6893125fe7e2f5bf392673e54caa0de0))


### 📝 Documentation

* seed CHANGELOG with the 0.1.0 baseline release ([3137b43](https://github.com/czimaginginstitute/relion-docker/commit/3137b4371c13236371b5b33d6c2457d465a75b42))
* update cdp-relion-sta tool list, remove stale known-issues section ([1ffe3a5](https://github.com/czimaginginstitute/relion-docker/commit/1ffe3a5f83e4d09ec7a995d144ae61f3b27f71a1))


### 🧹 Miscellaneous Chores

* reset release-please baseline to 0.0.0 for a clean first release ([13c70c1](https://github.com/czimaginginstitute/relion-docker/commit/13c70c1b95b2d8ad862d7f5b3d37d6c93cd5834a))
* revert release-please baseline to 0.1.0, matching org convention ([1a10661](https://github.com/czimaginginstitute/relion-docker/commit/1a106619a10647bc433d8fb4e84e5e4e14697e89))


### ⚙ Continuous Integration

* drop unneeded private-repo checkouts, build cdp-relion-sta on relevant PRs ([709736a](https://github.com/czimaginginstitute/relion-docker/commit/709736a082758a5a4e67b047e4b852a4470b9a8b))
* fix publish-sif /mnt permission error ([#11](https://github.com/czimaginginstitute/relion-docker/issues/11)) ([f5a44f2](https://github.com/czimaginginstitute/relion-docker/commit/f5a44f235a15732bf488b6cb882d20fd7c0b1e89))
* give publish-sif disk-cleanup headroom, matching build-push ([b02ef12](https://github.com/czimaginginstitute/relion-docker/commit/b02ef124f00cf53149abbd1bc9273a759d9505f5))
* grant pull-requests: read so paths-filter can list PR-changed files ([c05abd5](https://github.com/czimaginginstitute/relion-docker/commit/c05abd5274167bc676a827a33aac0b8d2362c158))
* log in to GHCR on PRs that will attempt the relion-zarr-sta build ([7d86bb7](https://github.com/czimaginginstitute/relion-docker/commit/7d86bb76d7dda8b07ac47f4151114073c9fe9dad))

## Changelog
