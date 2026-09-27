# Changelog

## [0.3.0](https://github.com/czimaginginstitute/relion-docker/compare/relion-docker-v0.2.0...relion-docker-v0.3.0) (2026-09-27)


### ✨ Features

* also push relion-zarr-sta to Docker Hub ([efa9cb7](https://github.com/czimaginginstitute/relion-docker/commit/efa9cb7e0cc1ced3ccfc38571e31e710dae5883c))


### 🐞 Bug Fixes

* bundle third-party license notices and pin RELION source commit ([dd9c200](https://github.com/czimaginginstitute/relion-docker/commit/dd9c20008cb044d5997e57b6bc35cd8444e292f1))
* correct CTFFIND license to v1.2/2018 per its actual COPYING file ([cb32b90](https://github.com/czimaginginstitute/relion-docker/commit/cb32b90f31ec322f31e9133767da6d7945246b4e))
* **image:** drop micromamba pkgs cache holding the old setuptools ([#27](https://github.com/czimaginginstitute/relion-docker/issues/27)) ([d747566](https://github.com/czimaginginstitute/relion-docker/commit/d747566d261c329e9793436f18c6c1d425647938))
* **image:** point relion_python_trace_amyloids at the installed script ([#29](https://github.com/czimaginginstitute/relion-docker/issues/29)) ([73a424c](https://github.com/czimaginginstitute/relion-docker/commit/73a424c838712b451af7f23aad052da70a43a467))
* **relion-zarr-sta:** drop build-essential from runtime image ([9f31d99](https://github.com/czimaginginstitute/relion-docker/commit/9f31d992ecf63555d7df3329e36e19c35f0edbb8))
* resolve HIGH image vulns; fix trivy scan, CI cache/disk, dependabot builds, python tools ([#26](https://github.com/czimaginginstitute/relion-docker/issues/26)) ([6879ceb](https://github.com/czimaginginstitute/relion-docker/commit/6879cebb49adfa3c9b0e4b933a7030eecd09bb01))


### 📝 Documentation

* pin exact CTFFIND version/license text and sources in THIRD_PARTY_LICENSES.md ([cdcda52](https://github.com/czimaginginstitute/relion-docker/commit/cdcda527b845e88ad712a874e9785e2e26bb382c))
* rename shims/ to client/, explain wrapper mechanism more clearly, add TOC ([8453b63](https://github.com/czimaginginstitute/relion-docker/commit/8453b63ea4c07e306b544694906c1d22d7cda9dd))
* **security:** note RELION 5.0 torch CVE, recommend 5.1 images ([fdba12d](https://github.com/czimaginginstitute/relion-docker/commit/fdba12d7696ff9f798b4927698a929c17070df10))


### 💅 Styles

* trim comments in security tooling files to essentials ([99c23ce](https://github.com/czimaginginstitute/relion-docker/commit/99c23ce7fcf7d847ea3bfe8e115b93024e26928a))


### 🧹 Miscellaneous Chores

* **security:** add image/code scanning, dependabot, and .dockerignore ([e210fdc](https://github.com/czimaginginstitute/relion-docker/commit/e210fdc4cbd7c61d37256496152aca9e5ea8c034))


### ♻️ Code Refactoring

* rename shims to relion-zarr-sta-client, install py2rely/zarr-particle-tools natively ([ffdf063](https://github.com/czimaginginstitute/relion-docker/commit/ffdf063d2b9b24fd0356fdb9a66d9ebf8cb94a24))


### 🛠️ Build System

* **deps:** bump actions/checkout from 5 to 7 ([#21](https://github.com/czimaginginstitute/relion-docker/issues/21)) ([e4af81a](https://github.com/czimaginginstitute/relion-docker/commit/e4af81a5ac1846baccc125261c2592a08156dadd))
* **deps:** bump aquasecurity/trivy-action ([#23](https://github.com/czimaginginstitute/relion-docker/issues/23)) ([b0052a0](https://github.com/czimaginginstitute/relion-docker/commit/b0052a03dd111e9899ba2a91d0301540fc8f9c78))
* **deps:** bump docker/login-action from 3.7.0 to 4.6.0 ([#24](https://github.com/czimaginginstitute/relion-docker/issues/24)) ([1a95f99](https://github.com/czimaginginstitute/relion-docker/commit/1a95f99b2a95c3e7584a62c1006eeb659c50ebc0))
* **deps:** bump docker/setup-buildx-action from 3.12.0 to 4.4.1 ([#25](https://github.com/czimaginginstitute/relion-docker/issues/25)) ([6176747](https://github.com/czimaginginstitute/relion-docker/commit/6176747e96974bb8ad93affffbc620aeef3d99ef))


### ⚙ Continuous Integration

* add .trivyignore for accepted torch CVE, wire it into the scan ([95e75bf](https://github.com/czimaginginstitute/relion-docker/commit/95e75bf17eab062b0deaec151b49a00684138609))
* drop redundant CodeQL workflow, add ci-pass gate ([39620fc](https://github.com/czimaginginstitute/relion-docker/commit/39620fc36e716eec4fc93e9eea71511b8ca70d2e))
* gate trivy scan on CRITICAL only ([6697dfb](https://github.com/czimaginginstitute/relion-docker/commit/6697dfb0b16c82cd187575db2a4927f7bd2541f4))
* **trivy:** raise scan timeout to 20m ([#31](https://github.com/czimaginginstitute/relion-docker/issues/31)) ([3845f5b](https://github.com/czimaginginstitute/relion-docker/commit/3845f5be23dea6c22ff391378f0b929e6e2b5b82))
* **trivy:** report all severities to code scanning again; gate stays CRITICAL-only ([#30](https://github.com/czimaginginstitute/relion-docker/issues/30)) ([fe86e85](https://github.com/czimaginginstitute/relion-docker/commit/fe86e85e229d8f465f6aa6b627af2623e27ea729))
* weekly cleanup of orphaned GHCR build cache versions ([#28](https://github.com/czimaginginstitute/relion-docker/issues/28)) ([6510e51](https://github.com/czimaginginstitute/relion-docker/commit/6510e51909cd2b532ca7100cad76aa57417dca4a))

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
