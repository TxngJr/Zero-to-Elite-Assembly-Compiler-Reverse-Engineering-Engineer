fn boom() -> bool { return (1 / 0) == 0; }
fn main() -> int {
  if (false && boom()) { return 1; } else { return 0; }
}
