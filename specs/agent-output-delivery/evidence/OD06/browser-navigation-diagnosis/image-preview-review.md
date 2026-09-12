# Bitmap preview probe static approval

Independent read-only reviewer `/root/od06_tenant_review`: APPROVE. The optional expectedImageSize is mutually exclusive with expectedText and requires positive integer dimensions. The probe clicks the actual visible preview button, then requires a complete image with the output title as alt and exact natural dimensions. It subsequently retains the actual click-download, SHA256 and exact HTTP200 assertions. Broken/incorrect/text-only previews fail. Web source is unchanged.

Node syntax and diff checks passed. This is static approval only; the bitmap live result remains pending. Baseline is Root3e9f84d plus the bounded image branch recorded in this commit.
