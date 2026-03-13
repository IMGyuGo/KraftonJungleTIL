from typing import Any, Sequence

def max_of(a: Sequence) -> Any:
  """시퀀스형 a 원소의 최댓값을 반환"""
  max = a[0]
  for i in range(1, len(a)) :
    if a[i] > max :
      max = a[i]
  return max