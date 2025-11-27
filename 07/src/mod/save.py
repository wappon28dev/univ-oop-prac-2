from datetime import datetime
from pathlib import Path

from mod.paths import DIR_OUT


def save_with_timestamp(text: str, output_dir: Path = DIR_OUT) -> None:
    """現在のタイムスタンプを用いたファイル名で、指定された文字列を.txtファイルに保存します。

    ファイルは上書きされず、毎回新しいファイルが作成されます。
    Args:
        text (str): 保存する文字列
        output_dir (Path, optional): 出力先ディレクトリ（デフォルトは 'out'）
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # noqa: DTZ005
    filename = output_dir / f"transcription_{timestamp}.txt"
    with filename.open("w", encoding="utf-8") as f:
        f.write(text)
