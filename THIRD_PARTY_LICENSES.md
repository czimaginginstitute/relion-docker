# Third-Party Licenses

relion-docker's own code (Dockerfiles, CI configuration, `shims/`) is MIT-licensed (see
[LICENSE.md](LICENSE.md)). The images this repository builds bundle third-party software under
its own upstream license, listed below.

## RELION

RELION is licensed under [GPL-2.0-or-later](https://github.com/3dem/relion/blob/master/LICENSE).
`Dockerfile.relion` builds it from source at the pinned `RELION_REF` build argument, from the
upstream repository at https://github.com/3dem/relion — the corresponding source for any built
image is the source at that same ref.

## CTFFIND

CTFFIND version 4.1.14 (vendored as a prebuilt binary at
`extras/ctffind-4.1.14-linux64.tar.gz`, SHA256-pinned in `Dockerfile.relion`). CTFFIND4's own
page states: "This software is licensed under the terms of the [Janelia Research Campus Software
Copyright 1.1](http://license.janelia.org/license/)." —
https://grigoriefflab.umassmed.edu/ctf_estimation_ctffind_ctftilt. That URL redirects to
https://www.janelia.org/node/47808, Janelia's current license page, which describes the same
license as a 3-clause BSD license copyright Howard Hughes Medical Institute (HHMI). The exact
text below is reproduced from a published copy of this license (originally titled "The Janelia
Farm Research Campus Software Copyright 1.1"):
https://github.com/JaneliaSciComp/omnivore/blob/master/LICENSE.md.

```
The Janelia Farm Research Campus Software Copyright 1.1
=========================================================

Copyright (c) Howard Hughes Medical Institute, All rights reserved.

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
py2rely, zarr-particle-tools, etc.) and apt packages. Each keeps its own upstream license; see the
respective package's own repository/registry entry for details.
