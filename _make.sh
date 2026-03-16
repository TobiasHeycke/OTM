#!/usr/bin/env Rscript

project <- "otm2"
Sys.setenv(TAR_PROJECT = project)

distributed <- TRUE
notify <- TRUE

# Subset targets --------------------------------------------------------------

tbd_targets <- c(
  NULL
)

# Predicted computation time ---------------------------------------------

outdated_targets <- targets::tar_outdated(names = !!tbd_targets, reporter = "silent")
targets_metadata <- targets::tar_meta(names = !!outdated_targets, fields = c("name", "seconds"))

if(length(outdated_targets) > 0) {
  targets_metadata <- targets_metadata |>
    dplyr::filter(name %in% outdated_targets)
  
  rerun_time <- targets_metadata$seconds
  if(length(rerun_time) == 0) rerun_time <- numeric(0)

  untimed_targets <- dplyr::filter(
    targets_metadata, is.na(seconds)
  )$name
} else {
  rerun_time <- numeric(0)
  untimed_targets <- character(0)
}


# Run targets plan (analyse data & build reports) -----------------------------

workers <- if(isTRUE(distributed)) targets::tar_config_get("workers") else 1
predicted_rerun_time <- sum(rerun_time, na.rm = TRUE) / workers
start_time <- Sys.time()
start_time_msg <- paste("Start time:    ", format(start_time, "%Y-%m-%d %H:%M:%S"), "\n")

cat("--- Dispatch summary -----------------------------------------\n\n")

cat("Project:       ", project, "\n\n")
cat("Targets:       ", length(outdated_targets), "\n")
cat("Workers:       ", workers, "\n")

if(length(rerun_time) > 0) {

  cat(
    "Predicted time:"
    , lubridate::seconds_to_period(
      round(predicted_rerun_time)
    ) |>
      as.character()
    , "\n\n"
  )
  cat(start_time_msg)
  cat("Check back:    ", format(start_time + predicted_rerun_time, "%Y-%m-%d %H:%M:%S"), "\n"
  )
} else {
  cat("Predicted time: ???\n\n")
  cat(start_time_msg)
}


if(length(untimed_targets) == 0) {
  cat("\n")
} else {
  cat(
    "Nonestimable:  "
    , paste(untimed_targets, collapse = ", ")
    , "\n\n"
  )
}

if(length(outdated_targets) > 0) {
  cat("--- targets report -------------------------------------------\n\n")

  if(isTRUE(distributed)) {
    targets::tar_make_future(names = !!tbd_targets)
  } else {
    targets::tar_make(names = !!tbd_targets) # , callr_function = NULL
  }

  end_time <- Sys.time()


  # Notify user -----------------------------------------------------------------

  if(isTRUE(notify)) {
    targets_metadata <- targets::tar_meta(names = !!outdated_targets, fields = c("error"))

    cat("\n")
    cat("--- Notification ---------------------------------------------\n\n")
    methexp::tar_e_mail_notification(
      project
      , "frederik.aust@uni-koeln.de"
      , start_time, end_time
      , targets_metadata
    )
    cat("\n\n")
  }

  cat("--- End time ------------------------------------------------\n\n")

  cat("Finished:    ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n\n")
  
} else {
  cat("No outdated targets.\n\n")
}
