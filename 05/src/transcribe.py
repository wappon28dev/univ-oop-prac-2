from pathlib import Path
from typing import Final

import mlx_whisper

from paths import DIR_ASSETS


def transcribe_from_audio(audio_path: Path) -> str:
    """指定された音声ファイルパスから音声ファイルを読み込み、文字起こしを実行します。

    Args:
        audio_path (Union[str, Path]):
            文字起こしする音声ファイル（例: .wav, .mp3など）のパス。
            Pathオブジェクトを受け入れます。

    Returns:
        str: 文字起こしされたテキスト。文字起こしに失敗した場合は空文字列を返します。

    """
    model: Final = DIR_ASSETS / "whisper-base-mlx"
    if not model.exists():
        raise FileNotFoundError

    result: Final = mlx_whisper.transcribe(str(audio_path), path_or_hf_repo=str(model.resolve()))
    text = result["text"]
    return str(text)
