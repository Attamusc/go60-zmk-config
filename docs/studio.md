# ZMK Studio workflow

## Source-of-truth rule

The committed files in this repository are the firmware source of truth. Studio is an experiment surface for live binding changes.

Studio can assign bindings and manage the layers already declared in devicetree. It cannot be treated as the source for new behaviors, combos, timing, input processors, or physical layouts. Saved Studio changes are stored on the keyboard and are not written back to `config/go60.keymap`.

A saved Studio keymap overrides compiled bindings after later firmware flashes. Use **Restore Stock Settings** before judging a newly compiled keymap. This action removes Studio's stored keymap/layer overrides and reloads the bindings compiled into the current firmware; it is not firmware flashing or a general Bluetooth/settings reset.

## Connection methods on the development machine

The firmware enables Studio on the left/central half. BLE Studio support comes from `CONFIG_ZMK_STUDIO`; USB Studio support comes from the left-only `studio-rpc-usb-uart` snippet.

The development host is Fedora 44 and has a powered BlueZ Bluetooth controller. It has Firefox, but no Chrome/Edge or native ZMK Studio installation. Official Studio supports BLE from the Linux web app and native apps, while the web app itself requires Chrome/Edge. Therefore:

- **BLE:** the host adapter is capable, but no Go60 or Studio client was present to complete a connection. Install the native Linux Studio app or a supported Chrome/Edge browser, select `OUT_BLE`, and treat the result as unverified until a live edit succeeds.
- **USB:** the firmware transport is built, but no Go60 serial device was present. Select `OUT_USB` from `SYS`. Linux must grant the Studio client access to the resulting serial device; the current user is not in `dialout` or `uucp`, although desktop device ACLs may still grant access.
- Firefox alone is not a supported web-client path for this procedure.

Do not clear pairings merely to test BLE. Ask before any pairing reset.

## Live experiment

1. Flash the tested combined firmware to both halves using the procedure below.
2. Connect to the left/central half using BLE or USB.
3. Hold both active right thumbs (`R_T3` + `R_T2`) to enter `SYS`, then press `L_C1R2` for `&studio_unlock`.
4. In Studio, change one low-risk binding and save it.
5. Confirm the binding changes immediately.
6. Disconnect and reconnect, then reboot the keyboard and confirm whether the saved edit persists.
7. Record the successful change in `config/go60.keymap`. If it needs a new behavior, combo, timing value, or input processor, implement that directly in devicetree instead of trying to define it in Studio.
8. Commit and push the source change, wait for a successful build, and download the new `go60.uf2`.
9. In Studio, choose **Restore Stock Settings** so the saved experiment cannot mask compiled bindings. Flash the new firmware. Reconnect and use Restore Stock Settings again if an override is still present.
10. Verify that the compiled binding now appears without reapplying the Studio edit.

Do not use MoErgo Layout Editor as another authoritative keymap editor for this repository.

## Recovery flashing

Obtain the `go60.uf2` artifact from the successful GitHub Actions run. The same combined file contains firmware for both halves.

1. Get approval before flashing.
2. Flash the **right half first**, then the left half.
3. Enter the right bootloader. If the running keymap is unusable, power the half off, connect USB, hold physical `T3 + C3R3` (Alt + K on the stock right layout), and power it on.
4. Copy `go60.uf2` to `GO60RHBOOT`. The volume disappearing, sometimes with a host copy error at the end, normally indicates the bootloader rebooted.
5. Enter the left bootloader the same way with physical `T3 + C3R3` (Control + D on the stock left layout).
6. Copy the same file to `GO60LHBOOT`.
7. Allow the halves to reconnect. Do not reset configuration or Bluetooth pairings unless separately approved.
8. Connect Studio and run **Restore Stock Settings** if a saved Studio keymap masks the compiled map.

If normal bootloader entry fails, stop and consult the current [MoErgo Go60 troubleshooting guide](https://docs.moergo.com/go60-user-guide/troubleshooting/) before resetting stored settings.

## Hardware acceptance checklist

- [ ] Studio connects to the left half through the selected transport.
- [ ] One binding changes live, survives reconnect/reboot as expected, and can be restored.
- [ ] Only the mapped 34 positions act on all eight layers.
- [ ] All six combos trigger without accidental activations.
- [ ] Layer-taps, mod-taps, and sticky modifiers match the Toucan timing intent.
- [ ] Both Cirque trackpads and the vendor layer 2/layer 4 modes behave correctly.
- [ ] Both halves reconnect after reboot.
- [ ] Restore Stock Settings exposes the committed keymap.
- [ ] Recovery flashing works on both halves.

All items remain **UNVERIFIED ON HARDWARE** until tested with a physical Go60.

## References

- [ZMK Studio capabilities and restore warning](https://zmk.dev/docs/features/studio/)
- [Studio unlock behavior](https://zmk.dev/docs/keymaps/behaviors/studio-unlock/)
- [MoErgo Go60 customization and flashing](https://docs.moergo.com/go60-user-guide/customizing-key-layout/)
- [MoErgo Go60 troubleshooting](https://docs.moergo.com/go60-user-guide/troubleshooting/)
