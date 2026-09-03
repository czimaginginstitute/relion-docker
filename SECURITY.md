## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@biohub.org](mailto:security@biohub.org).

## Known image security notes

The RELION 5.0 images bundle PyTorch 2.0.1, which carries CVE-2025-32434 (a `torch.load`
remote-code-execution issue, fixed upstream in 2.6.0). It is only exploitable by loading an
untrusted model checkpoint; RELION uses trusted bundled weights, so the intended workflow is not
exposed. For a build with the fix, use the **5.1** images, which ship PyTorch 2.7.1.
