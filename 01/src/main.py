#!/bin/env python
# -*- coding: utf-8 -*-
"""utils から関数をimportして利用します。"""

from utils import fizzbuzz_function, list_generator_function, print_process

if __name__ == "__main__":
    """ここでlist_generator_functionは他人が作成した関数と考え、例外処理で堅牢に実装します。"""
    try:
        factory = list_generator_function()  # デフォルトの20個の整数リストを生成
    except Exception as e:
        print(f"エラー１: {e}")
        exit(1)

    """この処理は他人の作成した関数が信頼できるなら不要（デバッグ中にはあると嬉しい）"""
    # if not isinstance(factory, list) or not all(isinstance(i, int) for i in factory):
    #     print("`list_generator_function`の戻り値が整数を含むリストではありません。関数の使い方を確認してください。")
    #     exit(1)

    fizzbuzz_results = []  # FizzBuzzの結果を格納するリストを初期化

    """ここでfizzbuzz_functionは自作関数と考え、例外処理ではなく次回講義で触れる単体テストを実装することで品質を担保します。"""
    for number in factory:
        fizzbuzz_results.append(
            (number, fizzbuzz_function(number))
        )  # FizzBuzzの結果を取得

    """ここでprint_processは他人が作成した関数と考え、例外処理で堅牢に実装します。"""
    try:
        for number, fizzbuzz_result in fizzbuzz_results:
            print_process(number, fizzbuzz_result)  # FizzBuzzの結果を出力
    except Exception as e:
        print(f"エラー２: {e}")
