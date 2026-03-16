BayesFactor_design_matrix <- function(formula, data, whichRandom) {
  data <- BayesFactor:::marshallTibble(data)
  data <- BayesFactor:::reFactorData(data)
  dataTypes <- BayesFactor:::createDataTypes(
    formula
    , whichRandom = whichRandom
    , data = data
    , analysis = "lm"
  )
  BayesFactor:::fullDesignMatrix(formula, data, dataTypes)
}

g_map <- function(x) {
  g_map <- (1:ncol(x)) |>
  setNames(colnames(x))

  names(g_map) <- gsub(
    names(g_map)
    , pattern = "_redu_\\d\\.\\&\\."
    , replacement = ":"
  )

  names(g_map) <- gsub(
    names(g_map)
    , pattern = "(-*\\d+$)|(_redu_\\d$)"
    , replacement = ""
  )

  g_map_names <- names(g_map)
  g_map <- pmatch(g_map_names, unique(g_map_names), duplicates.ok = TRUE) |>
    setNames(g_map_names)
  g_map - 1
}

r_scale <- function(x, whichRandom = "ParticipantNumber", fixed = 0.5, random = 1) {
  random_inc <- random - fixed
  grepl(names(x), pattern = whichRandom) * random_inc + fixed
}

n_way_anova <- function(y, X, fixed = 0.5, random = 1, ..., seed = NULL) {
  g <- g_map(X)

  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  BayesFactor::nWayAOV(
    y = y
    , X = X
    , gMap = g
    , rscale = r_scale(g[!duplicated(g)], fixed = fixed, random = random)
    , ...
  )
}
