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
        self.assertEqual(layers[0][58]["params"][0]["value"], "LCTRL")
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

    def test_thumbs_stay_on_the_correct_halves(self):
        layers = self.layout["layers"]
        self.assertEqual(layers[0][55]["params"][1]["value"], "F12")
        self.assertEqual(layers[0][57]["params"][0]["value"], 5)
        self.assertEqual([key["params"][0]["value"] for key in layers[7][54:57]], ["MCLK", "LCLK", "RCLK"])
        self.assertEqual([key["value"] for key in layers[7][57:60]], ["&trans"] * 3)


if __name__ == "__main__":
    unittest.main()
