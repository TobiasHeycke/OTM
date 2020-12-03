################################################################################
###
### Klauer, K. C., Draine, S. C., & Greenwald, A. G. (1998).
### An unbiased errors-in-variables approach to detecting unconscious cognition.
### British Journal of Mathematical and Statistical Psychology, 51(2), 253–267.
### doi:10.1111/j.2044-8317.1998.tb00680.x
###
### R code: Daniel W. Heck (heck@uni-mannheim.de)
### Contact: Simone Malejka (s.malejka@ucl.ac.uk)
###
################################################################################

## regression correction
## usage: fit(data)
## data: data frame with variables x (predictor) and y (criterion)
## (cs)


# library("minqa")
# library("numDeriv")

## only needed for simulations:
#library("parallel")

### Log-likelihood function on p. 258
eiv_loglik <- function(par, dv, iv, const=1e20) {
  mu <- par[1]
  sigma <- par[2]
  sx <- par[3]
  sy <- par[4]
  beta <- par[5]
  alpha <- par[6]
  
  x <- iv
  y <- dv
  
  nu <- (sy * sigma)^2 + (beta * sx * sigma)^2 + (sx * sy)^2
  xi <- 1/sqrt(nu) * (x * sy/sx * sigma + beta * (y - alpha) * sx/sy * sigma +
                        mu * sx * sy / sigma)
  gamma <- x^2 / sx^2 + (y - alpha)^2 / sy^2 + mu^2 / sigma^2
  
  f <- 1/(2*pi*sqrt(nu)) * exp(-1/2 * (gamma - xi^2)) * (1 - pnorm(-xi)) +
    1/(2*pi * sx * sy) * exp(-1/2 * (gamma - (mu/sigma)^2)) * pnorm(-mu / sigma)
  
  ll <- - sum(log(f))
  if(ll == Inf || is.na(ll))
    ll <- const
  ll
}

### Maximum-likelihood estimation
eiv_lm <- function(formula, data, start=NULL, n.optim=3, ...) {
  vars <- all.vars(formula)
  
  data <- model.frame(formula, data, ...)
  
  if (missing(start) || is.null(start))
    start <- runif(6, c(-1, 0, 0, 0, -.2, -.2), c(1, 3, 3, 3, .2, .2))
  cnt <- 1
  oo <- list(fval=Inf)
  while(cnt < n.optim){
    if (cnt > 1)
      start <- runif(6, c(-1, 0, 0, 0, 0, -.1), c(2, 5, 3, 3, 1, 1))
    oo2 <- minqa::bobyqa(start, eiv_loglik, dv = data[[vars[1]]], iv = data[[vars[2]]],
                  lower=c(-Inf, 0, 0, 0, -Inf, -Inf))
    if(oo2$fval < oo$fval)
      oo <- oo2
    cnt <- cnt + 1
  }
  se <- rep(NA, 6)
  try({
    hessian <- numDeriv::hessian(eiv_loglik, oo$par, dv = data[[vars[1]]], iv = data[[vars[2]]])
    se <- sqrt(diag(solve(hessian)))
  })
  res <- list(estimate=oo$par, std.err = se)
  attr(res, "call") <- match.call()
  attr(res, "formula") <- formula
  attr(res, "hessian") <- hessian
  attr(res, "df.residual") <- nrow(data) - 2
  attr(res, "data") <- data
  class(res) <- c("eiv_lm", "lm")
  
  res
}

print.eiv_lm <- function(x) {
  coef <- x$estimate[6:5]
  names(coef) <- c("(Intercept)", all.vars(attr(x, "formula"))[2])
  
  cat("\nCall:\n")
  print(attr(x, "call"))
  cat("\nCoefficents:\n")
  print(format(coef, digits = 3L), print.gap = 2L, quote = FALSE)
  cat("\n")
  
  invisible(x)
}

### NHST
summary.eiv_lm <- function(x) {
  
  data <- attr(x, "data")
  call <- attr(x, "call")
  df.res <- attr(x, "df.residual")
  coef_names <- c("(Intercept)", all.vars(attr(x, "formula"))[2])
  
  list_names <- names(x)
  attributes(x) <- NULL
  names(x) <- list_names
  
  # NHST of the intercept
  alpha <- x$estimate[6]
  SE_alpha <- x$std.err[6]
  
  t_alpha <- alpha / SE_alpha
  p_alpha <- 2 * pt(-abs(t_alpha), df = df.res) # compare to getAnywhere(t.test.default)
  
  # NHST of the slope
  beta <- x$estimate[5]
  SE_beta <- x$std.err[5]
  
  t_beta <- beta / SE_beta
  p_beta <- 2 * pt(-abs(t_beta), df = df.res)
  
  res <- c(data.frame(term = coef_names), as.data.frame(unclass(x))[6:5, ], list(df=df.res, statistic=c(t_alpha, t_beta), p.value=c(p_alpha, p_beta)))
  
  res <- as.data.frame(res)
  attr(res, "call") <- call
  attr(res, "df.residual") <- df.res
  class(res) <- c("summary.eiv_lm", "data.frame")
  
  res
}

confint.eiv_lm <- function(x, level = 0.95) {
  data <- attr(x, "data")
  df.res <- attr(x, "df.residual")
  t.val <- qt(1 - (1 - level)/2, df.res)
  
  coef_names <- c("(Intercept)", all.vars(attr(x, "formula"))[2])
  level_names <- paste(round(c((1 - level)/2, 1 - (1 - level)/2) * 100, digits = 1), "%")
  
  alpha <- x$estimate[6]
  SE_alpha <- x$std.err[6]
  
  beta <- x$estimate[5]
  SE_beta <- x$std.err[5]
  
  matrix(
    c(alpha - SE_alpha * t.val, beta - SE_beta * t.val, alpha + SE_alpha * t.val, beta + SE_beta * t.val)
    , ncol = 2
    , dimnames = list(coef_names, level_names)
  )
}


vcov.eiv_lm <- function(object) {
  solve(attr(object, "hessian"))
}


# See https://janhove.github.io/reporting/2017/05/12/visualising-models-2

predict.eiv_lm <- function(object, newdata = NULL, se.fit = FALSE, interval = "confidence", level = 0.95) {
  data <- attr(object, "data")
  df.res <- attr(object, "df.residual")
  t.val <- qt(1 - (1 - level)/2, df.res)
  
  if(is.null(newdata)) {
    newdata <- data
  }
  
  mm <- model.matrix(attr(object, "formula")[-2], data = newdata)
  
  fitted.values <- mm %*% object$estimate[6:5]
  se.fitted.values <- sqrt(diag(mm %*% vcov(object)[6:5, 6:5] %*% t(mm)))
  
  fit <- data.frame(
    fit = fitted.values
    , lwr = fitted.values - t.val * se.fitted.values
    , upr = fitted.values + t.val * se.fitted.values
  )
  
  res <- list(
    fit = fit
    , df = df.res
  )
  
  if(se.fit) res <- c(res, list(se.fit = se.fitted.values))
  
  res
}

apa_print.eiv_lm <- function(
  x
  , est_name = NULL
  , ci = 0.95
  , in_paren = FALSE
  , ...
) {
  ellipsis <- list(...)
  if(is.null(est_name)) est_name <- "b"
  stat_name <- "t"
  
  if(length(ci) == 1) {
    ci <- suppressMessages({confint(x, level = ci)})
  }
  
  if(is.matrix(ci)) {
    conf_level <- as.numeric(gsub("[^.|\\d]", "", colnames(ci), perl = TRUE))
    conf_level <- 100 - conf_level[1] * 2
  } else {
    conf_level <- 100 * ci
  }
  
  tidy_x <- summary(x)
  rownames(tidy_x) <- papaja:::sanitize_terms(tidy_x$term, standardized = FALSE)
  
  ## Assemble regression table
  regression_table <- data.frame(tidy_x[, c("term", "estimate", "statistic", "p.value")], row.names = NULL)
  regression_table$conf.int <- apply(
    ci
    , 1
    , function(y) do.call(function(...) papaja:::print_confint(x = y[utils::tail(names(y), 2)], ...), ellipsis) # Don't add "x% CI" to each line
  )
  regression_table <- regression_table[, c("term", "estimate", "conf.int", "statistic", "p.value")] # Change order of columns
  regression_table$term <- papaja:::prettify_terms(regression_table$term, standardized = FALSE)
  
  regression_table$estimate <- do.call(function(...) papaja::printnum(regression_table$estimate, ...), ellipsis)
  regression_table$statistic <- papaja::printnum(regression_table$statistic, digits = 2)
  regression_table$p.value <- papaja::printp(regression_table$p.value)
  
  colnames(regression_table) <- c("term", "estimate", "conf.int", "statistic", "p.value")
  
  if(stat_name == "z") {
    test_statistic <- paste0("$", stat_name, "$")
  } else {
    test_statistic <- paste0("$", stat_name, "(", attr(x, "df.residual"), ")$")
  }
  
  papaja::variable_label(regression_table) <- c(
    term = "Predictor"
    , estimate = paste0("$", est_name, "$")
    , conf.int = paste0(conf_level, "\\% CI")
    , statistic = test_statistic
    , p.value = "$p$"
  )
  
  class(regression_table) <- c("apa_regression_table", class(regression_table))
  
  if(class(x)[1] == "glm") {
    attr(regression_table, "family") <- x$family$family
    attr(regression_table, "link") <- x$family$link
  } else if(inherits(x, "lm")) {
    attr(regression_table, "family") <- "gaussian"
    attr(regression_table, "link") <- "identity"
  }
  
  # Concatenate character strings and return as named list
  apa_res <- papaja:::apa_glm_res(regression_table, in_paren = in_paren, conf_level = conf_level)
  names(apa_res$estimate) <- papaja:::sanitize_terms(tidy_x$term)
  names(apa_res$statistic) <- names(apa_res$estimate)
  names(apa_res$full_result) <- names(apa_res$estimate)
  
  apa_res
}



### Data generation for simulated data sets
gen <- function(n, par){
  mu <- par[1]
  sigma <- par[2]
  sx <- par[3]
  sy <- par[4]
  beta <- par[5]
  alpha <- par[6]
  
  # True latent variables
  tx <- rnorm(n, mu, sigma)
  tx[tx<0] <- 0
  ty <- beta * tx + alpha
  
  # Observed variables
  x <- tx + rnorm(n, 0, sx)
  y <- ty + rnorm(n, 0, sy)
  data.frame(x = x, y = y, tx = tx, ty = ty)
}

### Replication function for simulation
replication <- function(i){
  sim <- gen(n, par)
  mod <- eiv_lm(sim, par)
  mod$estimate
}

################################################################################
# 
# ### Example in Klauer (1998, Table 1)
# n <- 1431
# par <- c(mu=-.2, sigma=1.67, sx=.8, sy=.27, beta=.02, alpha=.000)
# sim <- gen(n, par)

# # Check summary statistics on p. 259
# mean(sim$y)
# sd(sim$y)
# quantile(sim$x, seq(1/6, 5/6, 1/6))
# plot(sim$x, sim$y)
# hist(sim$x)
# reg <- lm(y ~ x, sim)
# coef(reg)
# reg_true <- lm(y ~ tx, sim)
# coef(reg_true)
# 
# mod <- eiv_lm(y ~ x, sim, par)
# 
# # Check Table 1
# cbind(true=par, est=mod$est, se=mod$se,
#       lm=c(NA, NA, NA, NA, coef(reg)))

################################################################################
# 
# ### Simulation in Klauer (1998, Table 2)
# cl <- makeCluster(8)
# tmp <- clusterEvalQ(cl, {library("minqa"); library("numDeriv")})
# clusterExport(cl, c("fit", "gen", "eiv_loglik", "n", "par"))
# simulation <- parSapply(cl, 1:300, replication)
# stopCluster(cl)
# 
# # Check Table 2 (values are multiplied by 100)
# cbind("true"=par*100,
#       "mean"=rowMeans(simulation)*100,
#       "MSE"=rowMeans(((simulation-par)*100)^2))





