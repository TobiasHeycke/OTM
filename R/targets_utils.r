tar_read_factory <- function(x, experiment, path, pattern, ...) {
  var_paths <- paste0(experiment, "_", x, "_paths")
  var_files <- paste0(experiment, "_", x, "_files")
  ellipsis <- list(...)
  
  list(
    tar_target_raw(
      var_paths
      , substitute(
        list.files(
          x
          , pattern = pattern
          , recursive = TRUE
          , full.names = TRUE
        ) |>
          unlist()
        , list(x = path, pattern = pattern)
      )
      , deployment = "main"
    )
    , tar_target_raw(
      var_files
      , parse(text = var_paths)
      , format = "file"
      , pattern = parse(text = paste0("map(", var_paths, ")"))
      , deployment = "main"
    )
    , tar_target_raw(
      paste0(experiment, "_", x)
      , substitute(
        {
          do.call(
            batch_read
            , c(list(x = eval(paths), read_fun = read.delim), ellipsis)
          )
        }
        , list(paths = parse(text = var_paths), ellipsis = ellipsis)
      )
      , deployment = "main"
      , deps = var_paths
    )
  )
}
