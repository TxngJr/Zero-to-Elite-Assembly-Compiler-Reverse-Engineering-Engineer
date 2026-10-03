fn fact(n: int) -> int {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
}
fn main() -> int {
  if (fact(5) == 120) { return 0; } else { return 1; }
}
