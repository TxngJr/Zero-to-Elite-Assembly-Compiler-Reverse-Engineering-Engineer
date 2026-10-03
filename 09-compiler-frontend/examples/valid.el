fn add(a: int, b: int) -> int { return a + b; }
fn main() -> int {
  let x: int = 6;
  let y: int = 7;
  if (x < y) { return add(x, y); } else { return 0; }
}
