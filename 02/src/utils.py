def fizzbuzz_function(number: int) -> str:
    """int型の引数numberを受け取り、FizzBuzzのルールに従って文字列を返す関数。

    Args:
        number (int): FizzBuzzのルールを適用する整数

    Returns:
        str: FizzBuzzの結果

    """
    if number % 3 == 0 and number % 5 == 0:
        return "FizzBuzz"
    if number % 3 == 0:
        return "Fizz"
    if number % 5 == 0:
        return "Buzz"
    return str(number)


def list_generator_function(count: int = 20) -> list[int]:
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
        msg = "numberは整数である必要があります。"
        raise TypeError(msg)
    if not isinstance(fizzbuzz_result, str):
        msg = "fizzbuzz_resultは文字列である必要があります。"
        raise TypeError(msg)
    if fizzbuzz_function(number) != fizzbuzz_result:
        msg = "fizzbuzz_resultがnumberに対する正しいFizzBuzzの結果ではありません。"
        raise ValueError(msg)
    print(f"Number: {number:02}, Result: {fizzbuzz_result}")
