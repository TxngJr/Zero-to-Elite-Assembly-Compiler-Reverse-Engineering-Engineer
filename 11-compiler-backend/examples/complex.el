fn sum8(a: int,b: int,c: int,d: int,e: int,f: int,g: int,h: int) -> int {
  return a+b+c+d+e+f+g+h;
}
fn fact(n: int) -> int {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
}
fn main() -> int {
  let x: int = sum8(1,2,3,4,5,6,7,8);
  let y: int = fact(5);
  if ((x == 36) && (y == 120)) { return 0; } else { return 1; }
}
