def f(v, b, n, a):
  for i in range(n):
    v[i] = v[i] * (1-a) + b[i] * a
  return v

def main():
  a = 0.5
  k = 0
  n = 10
  v = [1/n] * n
  b = [0] * n
  b[k] = 1
  print("v: ", v)
  print("b: ", b)
  for i in range(100):
    v = f(v, b, n, a)
  print("v: ", v)
  print("sum v: ", sum(v))

if __name__ == "__main__":
  main()
