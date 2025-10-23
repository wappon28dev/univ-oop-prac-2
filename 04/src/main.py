from pathlib import Path
from typing import Final

import mlx_whisper
import numpy as np
from pydub import AudioSegment

DIR_ASSETS: Final = Path(__file__).parent.parent / "assets"
DIR_MODEL: Final = DIR_ASSETS / "whisper-base-mlx"

# 音声ファイルを指定して文字起こし
audio_file_path = DIR_ASSETS / "python-audio-output.wav"

result = mlx_whisper.transcribe(
    str(audio_file_path),
    path_or_hf_repo=str(DIR_MODEL),
)
print(result)


# 音声データを指定して文字起こし
def preprocess_audio(sound: AudioSegment) -> AudioSegment:
    return sound.set_frame_rate(16000).set_sample_width(2).set_channels(1)


audio_data = []

# 音声データを音声ファイルから読み取る
audio_data.append(AudioSegment.from_file(DIR_ASSETS / "audio-output-before.wav", format="wav"))
audio_data.append(AudioSegment.from_file(DIR_ASSETS / "audio-output-after.wav", format="wav"))

for data in audio_data:
    sound = preprocess_audio(data)
    # Metal(GPU)が扱えるNumpy Array形式に変換
    arr = np.array(sound.get_array_of_samples()).astype(np.float32) / 32768.0
    result = mlx_whisper.transcribe(
        arr,
        path_or_hf_repo=str(DIR_MODEL),
    )
    print(result)
