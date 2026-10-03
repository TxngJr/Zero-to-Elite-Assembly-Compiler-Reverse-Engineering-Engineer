fn sum8(a:int,b:int,c:int,d:int,e:int,f:int,g:int,h:int) -> int {
  return a+b+c+d+e+f+g+h;
}

fn fact(n:int) -> int {
  if (n <= 1) {
    return 1;
  } else {
    return n * fact(n - 1);
  }
}

fn series(n:int) -> int {
  let i:int = 0;
  let total:int = 0;
  while (i < n) {
    total = total + i;
    i = i + 1;
  }
  return total;
}

fn main() -> int {
  let a:int = fact(5);
  let b:int = series(11);
  let c:int = sum8(1,2,3,4,5,6,7,8);

  if ((a == 120) && ((b == 55) && (c == 36))) {
    return 0;
  } else {
    return 1;
  }
}
