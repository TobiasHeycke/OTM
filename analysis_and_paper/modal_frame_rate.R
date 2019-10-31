#' Calculate per Person Frame Rate
#'
#' @param data.frame. Experimental log data
#'
#' @export

modal_frame_rate <- function(x) {
  rounded_frame_rate <- apply(x, 1, function(y) round(1 / y))
  
  apply(
    rounded_frame_rate
    , 2
    , function(z) names(sort(-table(z)))[1]
  )
}