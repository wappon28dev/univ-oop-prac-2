from pathlib import Path
from typing import Final

import ffmpeg

DIR_OUT: Final = Path(__file__).parent.parent / "out"

DIR_OUT.mkdir(exist_ok=True)

# 録音時間（秒）
duration = 10
# 出力ファイル名
output_file = DIR_OUT / "python-audio-output.wav"

print(f"{duration}秒間、マイクからの録音を開始します...")
# FFmpegコマンドを実行
# -f <デバイス入力形式>: OSに応じたデバイス入力形式を指定
#   - Windows: 'dshow' または 'gdigrab'
#   - macOS: 'avfoundation'
#   - Linux: 'alsa'
# -i <入力デバイス名>: デバイス名を指定
(
    ffmpeg.input(":0", f="avfoundation", t=duration)  # macOSの例
    .output(filename=output_file, acodec="pcm_s16le", ar="44100", ac=1)
    .run(overwrite_output=True)
)
print(f"録音が完了しました。{output_file}に保存されました。")
