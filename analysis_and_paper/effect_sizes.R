pes_to_dz <- function(pes, n, n_groups = 2) {
  # I *think* sqrt(n_groups) is needed because of the between subject factor
  # either way I validate that the results for pes, f, and dz are correct
  sqrt(((1 - n) * pes)/(n * (pes - 1))) * sqrt(n_groups)
}

dz_to_f <- function(dz, rho) {
  0.5 * dz * sqrt(2 * (1 - rho))
}

pes_to_f <- function(pes, n, rho) {
  dz <- pes_to_dz(pes, n)
  dz_to_f(dz, rho)
}

f_to_dz <- function(f, rho) {
  (sqrt(2) * f) / sqrt(1 - rho)
}

dz_to_pes <- function(dz, n, n_groups = 2) {
  (dz^2 * n)/(dz^2 * n + n*n_groups - n_groups)
}