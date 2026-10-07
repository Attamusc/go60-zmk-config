# Toucan-to-Go60 port

## Toucan typing-position map

Go60 binding order is four 12-key rows, six bottom-corner keys, then the thumbs in this order: `L_T1 L_T2 L_T3 R_T3 R_T2 R_T1`.

The Toucan's three typing rows map to the Go60's three stock alpha rows, R2 through R4. Each alpha row uses C5 through C1 on the left and C1 through C5 on the right, leaving C6 unused. The ten inner R1 keys provide digits. The thumb mapping below incorporates the owner's revised Layout Editor export; it replaces the original T2/T3 proposal.

| Toucan position | Go60 position | Go60 index | BASE binding |
|---:|---|---:|---|
| 1 | L_C5R2 | 13 | `Q` |
| 2 | L_C4R2 | 14 | `W` |
| 3 | L_C3R2 | 15 | `E` |
| 4 | L_C2R2 | 16 | `R` |
| 5 | L_C1R2 | 17 | `T` |
| 6 | R_C1R2 | 18 | `Y` |
| 7 | R_C2R2 | 19 | `U` |
| 8 | R_C3R2 | 20 | `I` |
| 9 | R_C4R2 | 21 | `O` |
| 10 | R_C5R2 | 22 | `P` |
| 13 | L_C5R3 | 25 | `A` |
| 14 | L_C4R3 | 26 | `S` |
| 15 | L_C3R3 | 27 | hold `NAV`, tap `D` |
| 16 | L_C2R3 | 28 | hold `SYM_RIGHT`, tap `F` |
| 17 | L_C1R3 | 29 | `G` |
| 18 | R_C1R3 | 30 | `H` |
| 19 | R_C2R3 | 31 | hold `SYM_LEFT`, tap `J` |
| 20 | R_C3R3 | 32 | hold `NUM`, tap `K` |
| 21 | R_C4R3 | 33 | `L` |
| 22 | R_C5R3 | 34 | Backspace |
| 25 | L_C5R4 | 37 | `Z` |
| 26 | L_C4R4 | 38 | `X` |
| 27 | L_C3R4 | 39 | `C` |
| 28 | L_C2R4 | 40 | `V` |
| 29 | L_C1R4 | 41 | `B` |
| 30 | R_C1R4 | 42 | `N` |
| 31 | R_C2R4 | 43 | `M` |
| 32 | R_C3R4 | 44 | Comma |
| 33 | R_C4R4 | 45 | Period |
| 34 | R_C5R4 | 46 | Enter |
| 37 | L_T1 | 54 | hold Left GUI, tap F12 |
| 38 | L_T2 | 55 | Left Shift |
| 39 | R_T2 | 58 | hold `UTIL`, tap Space |
| 40 | R_T1 | 59 | hold Left Control, tap Tab |

Combos were rebuilt against these named Go60 physical positions in `config/go60.keymap`; the Toucan's numeric combo arrays were not copied.

The two outer R1 keys, C6 on R2 through R4, and all six bottom-corner keys remain `&none` on every layer (14 positions). L_T3 is disabled on BASE but sends middle-click on MOUSE.

The BASE layer additionally maps L_C5R1 through L_C1R1 to `1`–`5`, R_C1R1 through R_C5R1 to `6`–`0`, and R_T3 to `Ctrl+Enter` (Pi input newline). NAV, both symbol layers, NUM, and UTIL pass all six thumbs through; SYS uses `none/none/trans/trans/trans/none` in binding order.

## Parity checklist

### Preserved

- All eight layer definitions. `BASE` through `SYS` retain their typing/navigation intent; `MOUSE` places right/left/middle clicks on the left thumbs and leaves the right thumbs transparent.
- `&mt`: balanced, 280 ms tapping term, 175 ms quick tap and prior-idle requirement.
- `&lt`: balanced, 200 ms tapping term, 175 ms quick tap.
- `&sk`: 900 ms release, quick release, modifier presses ignored.
- The custom hold-preferred `qt` definition and its 200 ms timing. It remains unreferenced, as it was in the active Toucan keymap.
- Six combos: SYS, Escape, left/right Hyper, and left/right Meh. Combo members use Go60 position names.
- Toucan macros for Hyper, 1Password, and Raycast.
- MoErgo's right Cirque pointer scaling and the vendor layer 2 and layer 4 overrides.

### Changed intentionally

- Each layer has 60 bindings; 14 positions remain disabled on every layer. BASE adds ten number-row keys and right T3. MOUSE passes those bindings through and assigns L_T3 to middle-click.
- The owner's revised thumb mapping moves GUI/F12 and Shift to left T1/T2, and Space/UTIL and Tab/Control to right T2/T1. Mouse clicks are right/left/middle on left T1/T2/T3.
- `SYS` adds `OUT_USB`, `OUT_BLE`, and a manual `&tog MOUSE` fallback. Hold R_T3 + R_T2 (`Ctrl+Enter` + Space on BASE) for `SYS`; combo positions 57/58 remain exactly as supplied by the owner. The mouse toggle is R_C1R2.
- The left pad scales X/Y by 1/8 before mapping to scroll, then maps click to right-click. This processor order follows the owner's export, replacing scroll-before-scale.
- Symbol bindings use explicit shifted keycodes matching the editor export; Control and Equal use canonical `LCTRL` and `EQUAL` names.

### Different or unsupported

- Toucan's Azoteq TPS43 driver, display, GPIO/matrix, split-input, zoom, swipe, three-finger gesture, and touch-to-`MOUSE` processor are not copied.
- Go60 keeps its two vendor Cirque trackpads. The right pad is a pointer by default and is faster on layer 2 (`SYM_RIGHT`). The left pad scrolls and maps click to right-click by default, then becomes a pointer on layer 4 (`NUM`).
- Toucan's touch-driven `MOUSE` activation is unavailable without changing Go60's vendor input processors. Use the documented `SYS` binding at R_C1R2 to toggle `MOUSE` manually. The right pad remains the pointer, the left pad remains the scroll/right-click pad, and MOUSE leaves right thumbs, number row, and `Ctrl+Enter` available; no replacement touch gesture is claimed.

### Unverified on hardware

- The revised thumbs (including left T3 middle-click and right T3 `Ctrl+Enter`) and number-row keys in compiled firmware.
- All layer-taps, mod-taps, sticky modifiers, and six combos under real typing.
- Both Cirque trackpads, their layer-specific modes, split reconnect, reboot persistence, and firmware flashing.
