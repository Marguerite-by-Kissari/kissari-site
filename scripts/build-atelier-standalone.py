"""Compatibility entry point: regenerate the complete integrated M15 atelier."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('build-editorial-prototype.py')), run_name='__main__')
