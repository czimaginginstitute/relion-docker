# Third-Party Licenses

relion-docker's own code (Dockerfiles, CI configuration, `client/`) is MIT-licensed (see
[LICENSE.md](LICENSE.md)). The images this repository builds bundle third-party software under
its own upstream license, listed below.

License texts inside the images:

| What | Where |
|---|---|
| this file, RELION's license (`RELION-LICENSE`), built RELION commit | `/opt/licenses/` |
| apt packages | `/usr/share/doc/<pkg>/copyright` |
| conda packages | `/opt/licenses/conda/` (relion-zarr-sta's env: `/opt/licenses/conda-zarr-sta/`) |
| pip packages | each `*.dist-info/` |
| micromamba (BSD-3-Clause) | `/opt/licenses/MICROMAMBA-LICENSE` |
| NVIDIA CUDA base image EULA | `/NGC-DL-CONTAINER-LICENSE` |

## RELION

RELION is licensed under [GPL-2.0-or-later](https://github.com/3dem/relion/blob/master/LICENSE).
`Dockerfile.relion` builds it from source at the `RELION_REF` build argument, from the upstream
repository at https://github.com/3dem/relion. The complete corresponding source for any built
image is that repository at the exact commit recorded inside the image at
`/opt/licenses/RELION-SOURCE-COMMIT.txt` (and in the `org.relion.source.revision` image label).
See "Corresponding source for GPL/AGPL components" below.

## CTFFIND

CTFFIND version 4.1.14 (vendored as a prebuilt binary at
`extras/ctffind-4.1.14-linux64.tar.gz`, SHA256-pinned in `Dockerfile.relion`). The text below is
copied verbatim from the `COPYING` file shipped in CTFFIND's own source distribution for this
version, obtained directly from the
[Grigorieff Lab](https://grigoriefflab.umassmed.edu/ctf_estimation_ctffind_ctftilt).

```
The Janelia Research Campus Software License 1.2

Copyright (c) 2018, Howard Hughes Medical Institute, All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions
and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or other materials provided
with the distribution.
Neither the name of the Howard Hughes Medical Institute nor the names of its contributors may
be used to endorse or promote products derived from this software without specific prior
written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED WARRANTIES OF MERCHANTABILITY,
NON-INFRINGEMENT, OR FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; REASONABLE ROYALTIES; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

The tarball contains only `bin/ctffind` and a plotting script (no LICENSE file); the text above
is from the sources cited. The binary is upstream's unmodified, statically linked build and
includes Intel MKL (Intel Simplified Software License) and OpenMP runtime libiomp5 (Intel license), wxWidgets (wxWindows Library Licence), glibc
(LGPL-2.1+), libstdc++ (GPL-3.0 with the GCC Runtime Library Exception), and libtiff, libjpeg and
zlib (permissive).

## Other bundled software (conda/pip/apt packages)

The images also contain apt packages and conda/pip environments (PyTorch, NumPy, napari, …;
relion-zarr-sta adds py2rely and zarr-particle-tools, both MIT), each under its own license (see
the table above). micromamba statically bundles libsolv, libarchive, libcurl, OpenSSL, krb5 and others
(BSD/MIT/Apache-2.0).

## Corresponding source for GPL/AGPL components

The images redistribute the following software in binary form under the GPL or AGPL. The
complete corresponding source for each is identified below; in addition, **we hereby offer, for
any recipient of these images and for a period of three years, to provide the complete
corresponding source for these components on request at opensource@biohub.org.**

- **RELION** (GPL-2.0-or-later): [3dem/relion](https://github.com/3dem/relion) at the commit in
  `/opt/licenses/RELION-SOURCE-COMMIT.txt`.
- **relion-classranker** and **topaz** (GPL-3.0), installed from upstream git; the commit is in
  each `<pkg>.dist-info/direct_url.json`.
- **Ubuntu 22.04 packages**, incl. FFTW3 (GPL-2.0+), Ghostscript (AGPL-3.0) and GPL base-system
  packages (bash, coreutils, …), unmodified; source via `apt-get source <pkg>`. Ghostscript runs only as a local
  command, never over a network, so AGPL §13 doesn't apply.
- **PyQt5** (GPL-3.0) and its Qt 5 libraries via `PyQt5-Qt5` (LGPL-3.0), unmodified from PyPI;
  source: PyPI sdists (Riverbank Computing, Qt Project).
- **glibc** (LGPL-2.1+), statically linked into `ctffind` (above); source from GNU.
- 5.1 only: `opencv-python` bundles Qt 5 and FFmpeg (LGPL); see its `LICENSE-3RD-PARTY.txt`.
- **conda-forge GPL packages** (e.g. `readline`, binutils' `ld_impl_linux-64`, GPL-3.0), unmodified; source
  via each conda-forge feedstock.

`libgomp` (GPL-3.0 with the GCC Runtime Library Exception) has no corresponding-source
obligation and isn't covered by the offer.
