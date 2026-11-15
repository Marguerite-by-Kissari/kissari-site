from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class PublicationUI(unittest.TestCase):
    def test_portable_builder_includes_real_publication_module(self):
        builder=(ROOT/'scripts/build-editorial-prototype.py').read_text()
        self.assertIn("folder/'publication-ui.js'",builder,'Portable atelier does not include the publication module')
if __name__=='__main__':unittest.main(verbosity=2)
