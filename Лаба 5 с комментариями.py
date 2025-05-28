import timeit #модуль для замера времени выполнения кода.
from itertools import product #функция для генерации декартова произведения (всех возможных комбинаций элементов)
### 1 часть
##Алгоритмический метод (без itertools)
def algorithmic_method(K):
    result = ['']     # Начинаем с пустой строки
    for _ in range(K):  # Повторяем K раз (по числу разрядов)
        result = [num + d for num in result for d in '1357']  # Добавляем каждую цифру к каждой строке, '1357' - восьмеричные числа
    return result

##функции питона
def python_method(K):
    return [''.join(p) for p in product('1357', repeat=K)] #генерирует все возможные комбинации длиной K из цифр '1','3','5','7'.
#''.join(p) — объединяет кортеж символов в строку (например, ('1','3') → '13')

K = 3  # Можно изменить разрядность
print("Алгоритмический метод:", algorithmic_method(K)[:10])  # Первые 10 чисел
print("Метод с itertools:", python_method(K)[:10])

print("\nСравнение скорости:")
print("Алгоритмический:", timeit.timeit(lambda: algorithmic_method(K), number=1000), " itertools:", timeit.timeit(lambda: python_method(K), number=1000)) #замеряет время 1000 выполнений функции.

### 2 часть
def optimized_method(K, max_sum):
    nums = [(''.join(p), sum(int(d) for d in p)) for p in product('1357', repeat=K) if sum(int(d) for d in p) <= max_sum]
    # Генерируем список кортежей (число, сумма цифр) для чисел, где сумма <= max_sum
    return max(nums, key=lambda x: x[1]) if nums else None
    # Возвращаем число с максимальной суммой цифр или None, если нет подходящих чисел
    #max(numbers, key=lambda x: x[1]) — находит число с максимальной суммой цифр.


K, max_sum = 3, 12

# Находим оптимальное число
optimal = optimized_method(K, max_sum)

# Выводим результат (если он есть) или сообщение об отсутствии подходящих чисел
print(f"\nОптимальное: {optimal[0]} (сумма: {optimal[1]})" if optimal else "Нет чисел")

