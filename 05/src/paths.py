from pathlib import Path
from typing import Final

DIR_PJ: Final = Path(__file__).resolve().parent.parent

DIR_ASSETS: Final = DIR_PJ / "assets"

DIR_OUT: Final = DIR_PJ / "out"
DIR_OUT.mkdir(parents=True, exist_ok=True)
