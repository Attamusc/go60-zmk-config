{ pkgs ?  import <nixpkgs> {}
, firmware ? import ../src {}
}:

let
  config = ./.;

  # The pinned nanopb module uses /usr/bin/env in its generator scripts, but
  # Nix build sandboxes do not provide that path. Keep the module revision and
  # make only its shebangs Nix-compatible for the Studio-enabled build.
  studioNanopb = firmware.zephyr.modules.nanopb.overrideAttrs (old: {
    installPhase = ''
      mkdir -p $out/nanopb
      cp -R ${old.src}/. $out/nanopb
      chmod -R u+w $out/nanopb
      find $out/nanopb/generator -type f -exec \
        sed -i '1s|^#!/usr/bin/env python3$|#!${pkgs.coreutils}/bin/env python3|' {} +
    '';
  });
  studioZephyr = firmware.zephyr.overrideAttrs (old: {
    passthru = old.passthru // {
      modules = old.passthru.modules // { nanopb = studioNanopb; };
    };
  });

  go60_left = firmware.zmk.override {
    board = "go60_lh";
    keymap = "${config}/go60.keymap";
    kconfig = "${config}/go60_lh.conf";
    snippets = [ "studio-rpc-usb-uart" ];
    zephyr = studioZephyr;
  };
  go60_right = firmware.zmk.override {
    board = "go60_rh";
    keymap = "${config}/go60.keymap";
    kconfig = "${config}/go60.conf";
  };

in firmware.combine_uf2 go60_left go60_right "go60"
