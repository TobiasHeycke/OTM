apa_print_bf <- function(x, ...) {
  UseMethod("apa_print_bf", x)
}

apa_print_bf.default <- function(x, ...) papaja:::no_method(x)

apa_print_bf.numeric <- function(
  x
  , ratio_subscript = "10"
  , auto_invert = TRUE
  , scientific = TRUE
  , max = 1000
  , min = 1 / max
  , evidential_boost = NULL
  # , logbf = FALSE
  , ...
) {
  papaja:::validate(x, check_NA = TRUE)
  papaja:::validate(ratio_subscript, check_class = "character", check_length = 1)
  papaja:::validate(auto_invert, check_class = "logical", check_length = 1)
  papaja:::validate(scientific, check_class = "logical", check_length = 1)
  papaja:::validate(max, check_class = "numeric", check_length = 1)
  papaja:::validate(min, check_class = "numeric", check_length = 1)
  if(!is.null(evidential_boost)) papaja:::validate(evidential_boost, check_class = "numeric", check_length = length(x))
  # validate(logbf, check_class = "logical", check_length = 1)

  ellipsis <- list(...)
  ellipsis$x <- as.vector(x)

  if(!is.null(evidential_boost)) {
    ellipsis$x <- ellipsis$x * evidential_boost
  }

  if(auto_invert) {
    to_invert <- ellipsis$x < 1
    ellipsis$x[to_invert] <- 1 / ellipsis$x[to_invert]

    ratio_subscript[to_invert] <- invert_subscript(ratio_subscript)
  }

  if(scientific & (ellipsis$x > max - 1 | ellipsis$x < min)) {
    ellipsis$format <- "e"
    if(is.null(ellipsis$digits)) ellipsis$digits <- 2

    bf <- do.call("formatC", ellipsis)
    bf <- typeset_scientific(bf)
  } else {
    if(is.null(ellipsis$zero)) ellipsis$zero <- FALSE
    bf <- do.call("printnum", ellipsis)
  }

  if(!grepl("<|>", bf)) eq <- " = " else eq <- " "

  bf <- paste0("$\\mathrm{BF}_{", ratio_subscript, "}", eq, bf, "$")
  bf <- setNames(bf, names(x))
  bf
}

invert_subscript <- function(x) {
  seperator <- if(nchar(x) == 2) "" else "/"
  paste(rev(unlist(strsplit(x, seperator))), collapse = "")
}

typeset_scientific <- function(x) {
  x <- gsub("e\\+00$", "", x)
  x <- gsub("e\\+0?(\\d+)$", " \\\\times 10\\^\\{\\1\\}", x)
  x <- gsub("e\\-0?(\\d+)$", " \\\\times 10\\^\\{-\\1\\}", x)
  x
}
