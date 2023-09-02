export function generate_code(): string {
  const base_num = Math.floor(Math.random() * 1000000);
  return base_num.toString().padStart(6, "0");
}
