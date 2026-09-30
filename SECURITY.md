## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@biohub.org](mailto:security@biohub.org).

## Known image security notes

The RELION 5.0 and relion-zarr-sta images bundle PyTorch 2.0.1 (pinned upstream), which has
CVE-2025-32434 (`torch.load` RCE, needs an untrusted checkpoint; RELION only loads its own
weights) and CVE-2024-31580/31583 (mobile interpreter, unused). The 5.1 `relion` image ships
PyTorch 2.7.1. `.trivyignore.yaml` lists these plus two findings in pip's own vendored copies.

Images are scanned with Trivy after every main build; fixable findings are reported to code
scanning, and a fixable CRITICAL fails the scan.
