# Documentation Roadmap

## Content Gaps

### Missing Image Documentation
- [ ] **Uptime Kuma** (`uptime-kuma`)
    - [ ] Create `docs/images/uptime-kuma.md`
    - [ ] Add to `mkdocs.yml` navigation under "Utilities"
    - [ ] Add to `docs/images/index.md`
- [ ] **Immich** (`immich`)
    - [ ] Verify status of `immich-server` and `immich-ml` images (currently missing from repo root).
    - [ ] Create `docs/images/immich.md` covering the stack once ready.
    - [ ] Create `docs/images/immich-postgres.md` (or include in main Immich doc).

### Guide Improvements
- [ ] **Troubleshooting Guide**: Add common issues and fixes (e.g. permission denied, networking issues).
- [ ] **Migration Guide**: Specific steps for migrating from Linux/Docker to FreeBSD/Podman.

## Technical Improvements

- [ ] **Automated Doc Generation**: Script to sync `README.md` from image repos to `docs/images/<name>.md`.
    - This would prevent documentation drift.
- [ ] **Broken Link Checker**: Add CI step to check for broken links.
- [ ] **Search Optimization**: Add keywords/tags to pages for better search results.

## Design/UX

- [ ] **Image Badges**: Add "Official Image", "Community Image" or "Beta" badges if applicable.
- [ ] **Copy-Paste Annotations**: Ensure all complex `podman run` commands with annotations have easy copy buttons (already standard, but verify).
