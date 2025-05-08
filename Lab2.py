import re
def w(n): return ' '.join(['ноль','один','два','три','четыре','пять','шесть','семь','восемь','девять'][int(d)] for d in str(n))
nums = []
with open('input.txt') as f:
    for n in re.findall(r'\b\d+\b', f.read()):
        if (n:=int(n))%2 and n<=4095 and re.search(r'c[\da-f]$', hex(n)[2:], re.I):
            nums.append(n)
if nums:
    print(*[f"{n} (0x{hex(n)[2:]}) - {w(n)}" for n in sorted(nums)],
          f"\nВсего: {len(nums)}\nМинимальное: {w(min(nums))} ({min(nums)})", sep='\n')
else:
    print("Числа не найдены")