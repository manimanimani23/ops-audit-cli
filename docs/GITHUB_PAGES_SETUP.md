# GitHub Pages Configuration

## Settings Location
Repository → Settings → Pages

## Source
- Branch: `main`
- Folder: `/docs`

## Custom Domain
opsauditcli.manimani.dev

## Enforce HTTPS
☑️ Enabled (recommended)

## Build Status
After pushing CNAME file, GitHub will attempt to verify domain ownership.

## DNS Configuration Required
Add the following records to your DNS provider:

### For apex domain (manimani.dev):
Type: A
Name: @
Value: 
- 185.199.108.153
- 185.199.109.153
- 185.199.110.153
- 185.199.111.153

### For subdomain (opsauditcli.manimani.dev):
Type: CNAME
Name: opsauditcli
Value: manimanimani23.github.io

## Verification
Once DNS propagates (usually 5-60 minutes), visit:
https://opsauditcli.manimani.dev
