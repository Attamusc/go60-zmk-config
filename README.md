# Go60 ZMK configuration

Version-controlled firmware configuration for Attamusc's MoErgo Go60. The keymap ports the 34 active positions from the [Toucan configuration](https://github.com/attamusc/zmk-keyboard-toucan) onto the Go60 while retaining MoErgo's Go60 board and dual-Cirque configuration.

The MoErgo Layout Editor is used to edit and preview layouts; keep the repository keymap and its JSON export in sync. ZMK Studio is not enabled.

## Firmware source

- Configuration template: [`moergo-keyboards/go60-zmk-config`](https://github.com/moergo-keyboards/go60-zmk-config), template commit `8ccc8543191a95d6d676032ecb9a834634bda18e`
- MoErgo ZMK fork: [`moergo-sc/zmk`](https://github.com/moergo-sc/zmk)
- Pinned fork revision: `4b2f3b9b718a4508e87111cdec24cda16f3c2726`
- Output: one combined `go60.uf2` for both halves

Both halves use the Go60 board defaults for split communication. No firmware fork is kept in this repository.

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

For a preview in the MoErgo Go60 Layout Editor, run `python3 scripts/export-layout-editor.py` and import `config/go60-layout-editor.json` after enabling **Settings → Local Backup and Restore**. The export normalizes ZMK aliases (`LCTL` → `LCTRL`, `EQL` → `EQUAL`) for the editor. This is a derived JSON backup, not a firmware source: editor import, generated firmware parity, and live thumb placement still require verification. Do not replace this repository's keymap with editor-generated firmware without comparing its behaviors and trackpad configuration.

- [Toucan-to-Go60 position map and parity checklist](docs/porting.md)
- [Staged build evidence and artifact hashes](docs/build-evidence.md)

## Battery reporting

`config/go60_lh.conf` enables peripheral battery proxying. The pinned Go60 board defaults already enable fetching the right half's battery; the left half exposes it through an additional BLE Battery Service for applications that read both levels. Host Bluetooth menus may still show only the left battery. This setting applies to repository-built firmware, not the Layout Editor JSON preview. Application readings remain unverified until tested with the compiled firmware.

## Flashing

Do not flash either half or reset Bluetooth settings without the keyboard owner's approval.

When approved:

1. Download `go60.uf2` from the successful GitHub Actions run. The same combined file contains firmware for both halves.
2. Flash the **right half first**, then the left half.
3. To enter the right bootloader if the running keymap is unusable, power the half off, connect USB, hold physical `T3 + C3R3` (Alt + K on the stock right layout), and power it on.
4. Copy `go60.uf2` to `GO60RHBOOT`. The volume disappearing, sometimes with a host copy error at the end, normally indicates the bootloader rebooted.
5. Enter the left bootloader the same way with physical `T3 + C3R3` (Control + D on the stock left layout).
6. Copy the same file to `GO60LHBOOT`.
7. Allow the halves to reconnect and test both wireless split and USB-to-left with TRRS between halves. Do not reset configuration or Bluetooth pairings unless separately approved.

If normal bootloader entry fails, stop and consult the current [MoErgo Go60 troubleshooting guide](https://docs.moergo.com/go60-user-guide/troubleshooting/) before resetting stored settings.

## Current verification status

Earlier versions of the template and full port built in GitHub Actions; see the historical build evidence. The owner reports that both halves work wirelessly, but the right half does not work over TRRS with the latest Studio-enabled firmware. Studio support has been removed after a source-level UART configuration check reproduced a mismatch between wired split and its driver when the Studio USB snippet is enabled. A firmware build of this change is still pending; wired operation remains **UNVERIFIED ON HARDWARE**.
