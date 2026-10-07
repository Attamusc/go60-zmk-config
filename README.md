# Go60 ZMK configuration

Version-controlled firmware configuration for Attamusc's MoErgo Go60. The keymap ports the 34 active positions from the [Toucan configuration](https://github.com/attamusc/zmk-keyboard-toucan) onto the Go60 while retaining MoErgo's Go60 board and dual-Cirque configuration.

Git is the source of truth. ZMK Studio is used to try binding changes, not as a second authoritative editor. See [the Studio workflow](docs/studio.md) before saving live changes.

## Firmware source

- Configuration template: [`moergo-keyboards/go60-zmk-config`](https://github.com/moergo-keyboards/go60-zmk-config), template commit `8ccc8543191a95d6d676032ecb9a834634bda18e`
- MoErgo ZMK fork: [`moergo-sc/zmk`](https://github.com/moergo-sc/zmk)
- Pinned fork revision: `4b2f3b9b718a4508e87111cdec24cda16f3c2726`
- Studio: enabled only for `go60_lh`, the central half
- Studio USB transport: `studio-rpc-usb-uart`, left half only
- Output: one combined `go60.uf2` for both halves

The nanopb module at the pinned revision has Python generator shebangs that do not run inside a Nix sandbox. `config/default.nix` creates a Nix-compatible copy of that module for the Studio-enabled left build only. No firmware fork is kept in this repository.

## Build

### GitHub Actions (verified)

Every push and pull request runs `.github/workflows/build.yml`.

```sh
gh workflow run build.yml --repo Attamusc/go60-zmk-config --ref main
gh run list --repo Attamusc/go60-zmk-config --workflow build.yml --limit 5
gh run download RUN_ID --repo Attamusc/go60-zmk-config --name go60.uf2
```

The downloadable artifact contains `go60.uf2`. The workflow checks out the exact MoErgo ZMK revision listed above; it does not follow `main`.

### Local container build

The template's local build requires Docker:

```sh
./build.sh
```

An explicit revision can still be supplied:

```sh
./build.sh 4b2f3b9b718a4508e87111cdec24cda16f3c2726
```

Docker is not installed on the Fedora development machine used for this port, so the local path is unverified. GitHub Actions is the tested build path.

## Keymap

`config/go60.keymap` contains eight layers: `BASE`, `NAV`, `SYM_RIGHT`, `SYM_LEFT`, `NUM`, `UTIL`, `SYS`, and `MOUSE`.

Every layer supplies all 60 Go60 bindings. BASE uses the ten inner number-row keys for `1`–`0`. The owner's revised thumb arrangement is left T1 GUI/F12, left T2 Shift, left T3 disabled; right T3 `Ctrl+Enter`, right T2 Space/UTIL, and right T1 Tab/Control. On MOUSE, the left thumbs provide right/left/middle clicks (T1/T2/T3), while the right thumbs remain transparent; the number row and `Ctrl+Enter` also remain available. NAV, both symbol layers, NUM, and UTIL pass all six thumbs through. SYS still uses the R_T3 + R_T2 combo (now `Ctrl+Enter` + Space). The remaining 14 positions are `&none` on every layer. The left trackpad scales movement before converting it to scroll events.

For a preview in the MoErgo Go60 Layout Editor, run `python3 scripts/export-layout-editor.py` and import `config/go60-layout-editor.json` after enabling **Settings → Local Backup and Restore**. The export normalizes ZMK aliases (`LCTL` → `LCTRL`, `EQL` → `EQUAL`) for the editor and wraps `&studio_unlock` as a raw Custom binding; the editor does not validate that behavior or enable Studio in its firmware build. This is a derived JSON backup, not a firmware source: editor import, generated firmware parity, and live thumb placement still require verification. Do not replace this repository's keymap with editor-generated firmware without comparing its behaviors and trackpad configuration.

- [Toucan-to-Go60 position map and parity checklist](docs/porting.md)
- [Studio experiment, restore, and recovery procedure](docs/studio.md)
- [Staged build evidence and artifact hashes](docs/build-evidence.md)

## Battery reporting

`config/go60_lh.conf` enables peripheral battery proxying. The pinned Go60 board defaults already enable fetching the right half's battery; the left half exposes it through an additional BLE Battery Service for applications that read both levels. Host Bluetooth menus may still show only the left battery. This setting applies to repository-built firmware, not the Layout Editor JSON preview. Application readings remain unverified until tested with the compiled firmware.

## Flashing

Do not flash either half or reset Bluetooth settings without the keyboard owner's approval. When approved, follow [the recovery-flashing procedure](docs/studio.md#recovery-flashing).

## Current verification status

The unmodified template, pinned template, minimal Studio configuration, and full port all build in GitHub Actions. No Go60 was connected over USB or Bluetooth during this work. Live Studio editing, physical ergonomics, key behavior, trackpads, flashing, reconnect behavior, and restore behavior remain **UNVERIFIED ON HARDWARE**.
