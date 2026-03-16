# Libraries ---------------------------------------------------------------

library("targets")
library("tarchetypes")
library("rlang")

# Configure plan execution ------------------------------------------------

tar_option_set(
  storage = "main"
  , retrieval = "main"
  , memory = "transient"
  , garbage_collection = TRUE
  , workspace_on_error = TRUE
)

# Define plan -------------------------------------------------------------

list(
  # Render report
  , tar_render(
    paper
    , "./analysis_and_paper/manuscript.Rmd"
    , deployment = "main"
    , quiet = TRUE
  )
  , tar_render(
    supplementary_material
    , "./analysis_and_paper/supplements.Rmd"
    , deployment = "main"
    , quiet = TRUE
  )
  , tar_target(
    spellcheck_exceptions
    # Add new exceptions here
    , c("brms")
  )
  , tar_target(
    spellcheck_rmds
    , spelling::spell_check_files(
      c(paper)
      , ignore = spellcheck_exceptions
    )
  )
  , tar_force(
    spellcheck_report_results
    , print(spellcheck_rmds)
    , nrow(spellcheck_rmds) > 0
  )
)
