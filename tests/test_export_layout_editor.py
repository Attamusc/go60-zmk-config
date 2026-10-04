import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LayoutEditorExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts/export-layout-editor.py")], check=True)
        cls.layout = json.loads((ROOT / "config/go60-layout-editor.json").read_text())

    def test_layers_and_combos_are_present(self):
        self.assertEqual([len(layer) for layer in self.layout["layers"]], [60] * 8)
        self.assertEqual(len(self.layout["combos"]), 6)
        self.assertTrue(all(combo["layers"] == [-1] for combo in self.layout["combos"]))

    def test_editor_keycode_aliases(self):
        layers = self.layout["layers"]
        self.assertEqual(layers[0][59]["params"][0]["value"], "LCTRL")
        self.assertEqual(layers[3][32]["params"][0]["value"], "EQUAL")
        self.assertEqual(layers[4][41]["params"][0]["value"], "EQUAL")
        self.assertEqual(layers[5][32]["params"][0]["value"], "LCTRL")
        self.assertNotIn('"LCTL"', json.dumps(layers))
        self.assertNotIn('"EQL"', json.dumps(layers))

    def test_studio_unlock_uses_editor_custom_binding(self):
        self.assertEqual(
            self.layout["layers"][6][17],
            {"value": "Custom", "params": [{"value": "&studio_unlock"}]},
        )

    def test_owner_thumb_layout_on_every_layer(self):
        base = [
            {"value": "&mt", "params": [{"value": "LGUI"}, {"value": "F12"}]},
            {"value": "&kp", "params": [{"value": "LSHIFT"}]},
            {"value": "&none"},
            {"value": "&kp", "params": [{"value": "LC", "params": [{"value": "ENTER"}]}]},
            {"value": "&lt", "params": [{"value": 5}, {"value": "SPACE"}]},
            {"value": "&mt", "params": [{"value": "LCTRL"}, {"value": "TAB"}]},
        ]
        transparent = [{"value": "&trans"}] * 6
        system = [{"value": v} for v in ["&none", "&none", "&trans", "&trans", "&trans", "&none"]]
        mouse = [{"value": "&mkp", "params": [{"value": v}]} for v in ["RCLK", "LCLK", "MCLK"]]
        expected = [base] + [transparent] * 5 + [system, mouse + transparent[:3]]
        for name, layer, thumbs in zip(self.layout["layer_names"], self.layout["layers"], expected):
            with self.subTest(layer=name):
                self.assertEqual(layer[54:60], thumbs)

    def test_owner_trackpad_processor_order(self):
        self.assertEqual(self.layout["inputListeners"], [
            {
                "code": "&cirque_rh_listener",
                "inputProcessors": [{"code": "&zip_xy_scaler", "params": [3, 1]}],
                "nodes": [{"code": "layer_2", "layers": [2], "inputProcessors": [{"code": "&zip_xy_scaler", "params": [9, 1]}]}],
            },
            {
                "code": "&cirque_lh_listener",
                "inputProcessors": [
                    {"code": "&zip_xy_scaler", "params": [1, 8]},
                    {"code": "&zip_xy_to_scroll_mapper", "params": []},
                    {"code": "&zip_click_to_right_click_mapper", "params": []},
                ],
                "nodes": [{"code": "layer_4", "layers": [4], "inputProcessors": [{"code": "&zip_xy_scaler", "params": [3, 1]}]}],
            },
        ])

    def test_sys_combo_keeps_owner_positions(self):
        self.assertEqual(self.layout["combos"][0]["keyPositions"], [57, 58])
        self.assertEqual(self.layout["combos"][0]["binding"], {"value": "&mo", "params": [{"value": 6}]})

    def test_owner_symbol_representation(self):
        shifted_keys = {
            2: {19: "MINUS", 21: "BSLH", 25: "N6", 26: "N8", 27: "N7", 30: "N3", 32: "SINGLE_QUOTE", 34: "N4", 43: "GRAVE"},
            3: {14: "N1", 15: "SEMI", 25: "COMMA", 27: "LBKT", 28: "N9", 29: "N2", 33: "EQUAL", 34: "N5", 37: "DOT", 39: "RBKT", 40: "N0"},
            4: {17: "EQUAL", 37: "N8"},
            5: {14: "SEMI", 15: "FSLH", 16: "N1"},
        }
        for layer, positions in shifted_keys.items():
            for position, code in positions.items():
                with self.subTest(layer=layer, position=position):
                    self.assertEqual(self.layout["layers"][layer][position], {
                        "value": "&kp", "params": [{"value": "LS", "params": [{"value": code}]}],
                    })


if __name__ == "__main__":
    unittest.main()
