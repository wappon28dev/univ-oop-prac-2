def fizzbuzz_function(number) -> str:
    """int型の引数numberを受け取り、FizzBuzzのルールに従って文字列を返す関数。
    Args:
        number (int):
    FizzBuzzのルール:
        - 3の倍数なら"Fizz"
        - 5の倍数なら"Buzz"
        - 3と5の両方の倍数なら"FizzBuzz"
        - それ以外はそのまま数字を文字列に変換して返す
    """
    if number % 3 == 0 and number % 5 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return str(number)


def list_generator_function(count=20) -> list[int]:
    """指定された数の整数を含むリストを生成する関数。
    Args:
        count (int): 生成するリストの要素数。デフォルトは20。
    Returns:
        list: 1からcountまでの整数を含むリスト。
    """
    return list(range(1, count + 1))


def print_process(number: int, fizzbuzz_result: str) -> None:
    """FizzBuzzの結果の処理（出力やファイル保存など）をする関数。
    Args:
        number (int): 処理対象の整数。
        fizzbuzz_result (str): FizzBuzzの結果文字列。
    Rises:
        TypeError: 引数の型が期待される型でない場合に発生
        ValueError: fizzbuzz_resultがnumberに対する正しいFizzBuzzの結果でない場合に発生
    """
    if not isinstance(number, int):
        raise TypeError("numberは整数である必要があります。")
    if not isinstance(fizzbuzz_result, str):
        raise TypeError("fizzbuzz_resultは文字列である必要があります。")
    if not fizzbuzz_function(number) == fizzbuzz_result:
        raise ValueError(
            "fizzbuzz_resultがnumberに対する正しいFizzBuzzの結果ではありません。"
        )
    print(f"Number: {number:02}, Result: {fizzbuzz_result}")
