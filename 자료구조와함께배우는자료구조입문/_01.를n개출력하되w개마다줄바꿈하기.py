# *를 n개 출력하되 w개마다 줄바꿈하기

n = int(input('몇 개를 출력할까요?: '))
w = int(input('몇 개마다 줄바꿈할까요?: '))

# for i in range(n) :
#   if i % w == 0 :
#     print()
#   print("*", end='')

# 개선 방법
for i in range(n//w) :
  print("*" * w)


rest = n%w
print("*" * rest)