def w(n): return ' '.join(['ноль','один','два','три','четыре','пять','шесть','семь','восемь','девять'][int(d)] for d in str(n))

nums = []
with open('input.txt') as f:
    for line in f:
        for x in line.split():
            if (n:=int(x))%2 and n<=4095 and (h:=hex(n)[2:].zfill(2))[-2]=='c':
                nums.append(n)

if nums:
    print(*[f"{n} (0x{hex(n)[2:]}) - {w(n)}" for n in sorted(nums)],
          f"\nВсего: {len(nums)}\nМинимальное: {w(min(nums))} ({min(nums)})", sep='\n')
else:
    print("Числа не найдены")