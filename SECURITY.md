## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@biohub.org](mailto:security@biohub.org).

## Known image security notes

The RELION 5.0 images **and all relion-zarr-sta images** (built on RELION 5.0) bundle PyTorch
2.0.1, which carries CVE-2025-32434 (a `torch.load` remote-code-execution issue, fixed upstream in
2.6.0). It is only exploitable by loading an untrusted model checkpoint; RELION only loads its own
upstream model weights, which are downloaded on first use (not bundled; Blush, ModelAngelo,
classranker etc. need internet on first run), so the intended workflow is not exposed. It also
carries CVE-2024-31580 and CVE-2024-31583 (fixed in 2.2.0), which are in the mobile/lite
interpreter that RELION does not use. The 5.1 `relion` image ships PyTorch 2.7.1; there is no
5.1 relion-zarr-sta build yet.

`.trivyignore.yaml` also suppresses GHSA-6v7p-g79w-8964 (msgpack) and CVE-2025-47273 (setuptools),
both in pip's own vendored copies, which aren't used at runtime.

Images are scanned with Trivy after every main build (and on demand): fixable findings of every
severity are reported to code scanning (unfixed ones are left out), and a fixable, non-ignored
CRITICAL finding fails the scan.
