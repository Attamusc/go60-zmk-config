# Build evidence

All builds used the repository's GitHub Actions/Nix workflow. The Fedora development host did not have Docker, Nix, west, CMake, or Ninja installed, so no local firmware build is claimed.

| Stage | Config commit | Actions run | Result | Artifact |
|---|---|---|---|---|
| Unmodified official template | `804c650a8a320e687c07696ed80e71b79d0bad7a` | [36571075190](https://github.com/Attamusc/go60-zmk-config/actions/runs/36571075190) | PASS | 862,720 bytes; SHA-256 `bc0cbaf15a399cd8f0808aeac2fd2c5d430634f28c288f81eac61536ee9c2f9d` |
| Pinned template | `f42f86e9ff14fe50ff037ac0da5a9edf218145c8` | [36571519790](https://github.com/Attamusc/go60-zmk-config/actions/runs/36571519790) | PASS | 862,720 bytes; same SHA-256 as the unmodified template |
| Minimal left-only Studio build | `c22aa9c24782ca23051acac253a1c5d17c9c60a0` | [36572406437](https://github.com/Attamusc/go60-zmk-config/actions/runs/36572406437) | PASS | 913,920 bytes; SHA-256 `155079e9f0d9f61a327be4b9c8d3beca3df67456f4934b729d90dc62cc49fa38` |
| Initial full keymap port | `bcab1cefa36db10252bf2702a4b091abdc5874a5` | [36573131245](https://github.com/Attamusc/go60-zmk-config/actions/runs/36573131245) | PASS | 917,504 bytes; SHA-256 `247fb9e135442fad59346968c1a76f01cde494896e148890c3101e2b845c342f` |
| Documented initial port | `3ceee30acbe8951eef154fbdf6c0f80d595221cd` | [36573802883](https://github.com/Attamusc/go60-zmk-config/actions/runs/36573802883) | PASS | 917,504 bytes; same SHA-256 as the initial full port |
| Reviewed alpha-row mapping | `e36ce563ab6f93358066879d85d2956cbee42f04` | [36574775234](https://github.com/Attamusc/go60-zmk-config/actions/runs/36574775234) | PASS | 917,504 bytes; SHA-256 `baf68e1841a27ab583971a2e4c546d97c06018a345a5242f9ced47b3c70e1d68` |
| Manual MOUSE fallback | `1006bfcd20c1be541162123aa55cfec26579dd8c` | [36575574849](https://github.com/Attamusc/go60-zmk-config/actions/runs/36575574849) | PASS | 917,504 bytes; SHA-256 `dc41cf0f2cd1a7a294a3c4fde9c7879a1bc345f62d550185d2ea3560a5c1e82c` |

The first Studio attempt, run [36571622786](https://github.com/Attamusc/go60-zmk-config/actions/runs/36571622786), failed because nanopb's executable Python generators retained `/usr/bin/env` shebangs inside the Nix module symlink. `config/default.nix` makes a Nix-compatible copy of that pinned module for the left Studio build. Run 36572406437 proved the fix before the full keymap was ported.

Every listed run checked out MoErgo ZMK revision `4b2f3b9b718a4508e87111cdec24cda16f3c2726`.
