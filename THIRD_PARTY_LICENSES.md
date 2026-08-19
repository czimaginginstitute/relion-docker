# Third-Party Licenses

relion-docker's own code (Dockerfiles, CI configuration, `client/`) is MIT-licensed (see
[LICENSE.md](LICENSE.md)). The images this repository builds bundle third-party software under
its own upstream license, listed below.

This file is bundled inside the images themselves at `/opt/licenses/THIRD_PARTY_LICENSES.md`,
alongside RELION's own license text (`/opt/licenses/RELION-LICENSE`) and the exact upstream
RELION commit that was compiled in (`/opt/licenses/RELION-SOURCE-COMMIT.txt`, also recorded as
the `org.relion.source.revision` image label). Each apt package additionally carries its own
`/usr/share/doc/<pkg>/copyright`, each Python package its `*.dist-info/` license, and the
NVIDIA CUDA base image its EULA at `/NGC-DL-CONTAINER-LICENSE`.

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

Note: no LICENSE file ships inside the vendored binary tarball itself (it contains only
`bin/ctffind` and a plotting script) — the above is reproduced from the sources cited, not from
a file included in the tarball.

## Other bundled software (conda/pip/apt packages)

Both images also install a conda/pip environment (PyTorch, CTFFIND's runtime dependencies,
py2rely, zarr-particle-tools, etc.) and apt packages. Each keeps its own upstream license and
ships its own license text inside the image — apt packages at `/usr/share/doc/<pkg>/copyright`,
Python packages in their `*.dist-info/` directory. `relion-zarr-sta` adds py2rely and
zarr-particle-tools, both MIT-licensed.

## Corresponding source for GPL/AGPL components

The images redistribute the following software in binary form under the GPL or AGPL. The
complete corresponding source for each is identified below; in addition, **we hereby offer, for
any recipient of these images and for a period of three years, to provide the complete
corresponding source for these components on request at opensource@biohub.org.**

- **RELION** and its bundled companion tools (relion-blush, relion-classranker, DynaMight,
  topaz, model-angelo) — GPL-2.0-or-later / per each tool's upstream license. Built from source
  from the [3dem GitHub organization](https://github.com/3dem); the exact RELION commit is
  recorded at `/opt/licenses/RELION-SOURCE-COMMIT.txt`.
- **FFTW3** (GPL-2.0-or-later) and **Ghostscript** (AGPL-3.0) — installed unmodified from the
  Ubuntu 22.04 archive; corresponding source is available from Ubuntu (e.g. `apt-get source
  <pkg>`). Ghostscript is invoked only as a local command-line tool and is never exposed to
  users over a network, so the AGPL §13 (remote-network-interaction) source requirement does
  not apply; the ordinary source requirement for binary distribution is covered by this offer.
- **PyQt5** (GPL-3.0) — installed unmodified via pip; corresponding source is the upstream
  sdist on PyPI / from Riverbank Computing.

`libgomp` is licensed GPL-3.0 **with the GCC Runtime Library Exception**, which permits
distribution alongside compiled programs without a corresponding-source obligation for the
runtime library, so it is not covered by the offer above.
