# Toucan-to-Go60 port

## Proposed 34-key position map

Go60 binding order is four 12-key rows, six bottom-corner keys, then the thumbs in this order: `L_T1 L_T2 L_T3 R_T3 R_T2 R_T1`.

The finger map uses Go60 C5 through C1 on the left and C1 through C5 on the right, leaving each C6 outer column unused. The thumb map uses T2 and T3 on each half because those are the inner two, matching the Toucan's two active thumb positions. This is a proposed physical mapping and must be validated on the keyboard.

| Toucan position | Go60 position | Go60 index | BASE binding |
|---:|---|---:|---|
| 1 | L_C5R1 | 1 | `Q` |
| 2 | L_C4R1 | 2 | `W` |
| 3 | L_C3R1 | 3 | `E` |
| 4 | L_C2R1 | 4 | `R` |
| 5 | L_C1R1 | 5 | `T` |
| 6 | R_C1R1 | 6 | `Y` |
| 7 | R_C2R1 | 7 | `U` |
| 8 | R_C3R1 | 8 | `I` |
| 9 | R_C4R1 | 9 | `O` |
| 10 | R_C5R1 | 10 | `P` |
| 13 | L_C5R2 | 13 | `A` |
| 14 | L_C4R2 | 14 | `S` |
| 15 | L_C3R2 | 15 | hold `NAV`, tap `D` |
| 16 | L_C2R2 | 16 | hold `SYM_RIGHT`, tap `F` |
| 17 | L_C1R2 | 17 | `G` |
| 18 | R_C1R2 | 18 | `H` |
| 19 | R_C2R2 | 19 | hold `SYM_LEFT`, tap `J` |
| 20 | R_C3R2 | 20 | hold `NUM`, tap `K` |
| 21 | R_C4R2 | 21 | `L` |
| 22 | R_C5R2 | 22 | Backspace |
| 25 | L_C5R3 | 25 | `Z` |
| 26 | L_C4R3 | 26 | `X` |
| 27 | L_C3R3 | 27 | `C` |
| 28 | L_C2R3 | 28 | `V` |
| 29 | L_C1R3 | 29 | `B` |
| 30 | R_C1R3 | 30 | `N` |
| 31 | R_C2R3 | 31 | `M` |
| 32 | R_C3R3 | 32 | Comma |
| 33 | R_C4R3 | 33 | Period |
| 34 | R_C5R3 | 34 | Enter |
| 37 | L_T2 | 55 | hold Left GUI, tap F12 |
| 38 | L_T3 | 56 | Left Shift |
| 39 | R_T3 | 57 | hold `UTIL`, tap Space |
| 40 | R_T2 | 58 | hold Left Control, tap Tab |

The matching finger indices happen to have the same numbers in the two layouts because both orders begin with six positions per half. Combos were rebuilt against named Go60 physical positions in `config/go60.keymap`; the Toucan's numeric combo arrays were not copied.

Excluded Go60 positions are C6 on the first three rows, all 12 keys on row 4, all six bottom-corner keys, and T1 on each half. They are `&none` on every layer.

## Parity checklist

### Preserved

- Eight layers and their typing/navigation intent.
- `&mt`: balanced, 280 ms tapping term, 175 ms quick tap and prior-idle requirement.
- `&lt`: balanced, 200 ms tapping term, 175 ms quick tap.
- `&sk`: 900 ms release, quick release, modifier presses ignored.
- The custom hold-preferred `qt` behavior and its 200 ms timing.
- Six combos: SYS, Escape, left/right Hyper, and left/right Meh. Combo members use Go60 position names.
- Toucan macros for Hyper, 1Password, and Raycast.
- MoErgo's right Cirque pointer scaling and left Cirque scroll/right-click processing, including the vendor layer 2 and layer 4 overrides.

### Changed intentionally

- Each layer has 60 bindings; 26 positions are always disabled.
- The active thumbs move to Go60 T2/T3. This is an ergonomic proposal, not a measured result.
- `SYS` adds `OUT_USB`, `OUT_BLE`, and `&studio_unlock` on positions that were transparent in the Toucan map. Hold both active right thumbs for `SYS`; the unlock binding is L_C1R1.
- Toucan middle-click bindings were on the two excluded outer thumbs. They are not moved onto another key, because every position outside the 34-key footprint must remain `&none`.

### Different or unsupported

- Toucan's Azoteq TPS43 driver, display, GPIO/matrix, split-input, zoom, swipe, three-finger gesture, and touch-to-`MOUSE` processor are not copied.
- Go60 keeps its two vendor Cirque trackpads. The right pad is a pointer by default and is faster on layer 2 (`SYM_RIGHT`). The left pad scrolls and maps click to right-click by default, then becomes a pointer on layer 4 (`NUM`).
- `MOUSE` retains left/right click bindings on the four active thumbs, but Toucan's touch-driven layer activation is unavailable without changing Go60's vendor input processors. No replacement activation gesture is claimed.

### Unverified on hardware

- T2/T3 comfort and reach.
- All layer-taps, mod-taps, sticky modifiers, and six combos under real typing.
- Studio unlock, USB/BLE Studio connections, a saved live edit, and restore behavior.
- Both Cirque trackpads, their layer-specific modes, split reconnect, reboot persistence, and firmware flashing.
