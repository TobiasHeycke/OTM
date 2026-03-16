batch_read <- function(x, read_fun, ...) {
  data <- lapply(x, read_fun, ...)
  data <- do.call("rbind", data)
  data
}
