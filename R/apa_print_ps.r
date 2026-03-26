apa_print_ps <- function(x, ...) {
  UseMethod("apa_print_ps", x)
}

apa_print_ps.afex_aov <- function(x, ...) {
  library("dplyr")
  
  aov_table <- apa_print(x, ...)$table
  
  x$anova_table <- x$anova_table[as.numeric(rownames(aov_table)), ]
  x$anova_table$between <- FALSE
  between_vars <- names(attr(x, "between"))
  if(!is.null(between_vars)) x$anova_table$between <- grepl(paste(between_vars, collapse = "|"), rownames(x$anova_table))
  
  ellipsis <- list(...)

  aov_eta_table <- effectsize::eta_squared(x$anova_table, include_intercept = isTRUE(ellipsis$intercept), partial = TRUE, alternative = "two.sided", ci = 0.90)[as.numeric(rownames(aov_table)), ] %>% 
    data.frame()

  is_partial <- "Eta2_partial" %in% colnames(aov_eta_table)
  is_generalized <- "Eta2_generalized" %in% colnames(aov_eta_table)
  
  aov_eta_table <- aov_eta_table %>%
    rename(
      any_of(c(
        eta = "Eta2_partial"
        , eta = "Eta2"
        , ll = "CI_low"
        , ul = "CI_high"
      ))
    )
  
  aov_d_table <- x$anova_table %>% 
    rowwise() %>% 
    do(
      with(
        .
        , if(`num Df` == 1) {
          effectsize::F_to_d(f = `F`, df = `num Df`, df_error = `den Df`, paired = !between)
        } else data.frame(d = NA)
      )
    ) %>% 
    data.frame %>% 
    rename(
      ll = CI_low
      , ul = CI_high
    ) %>% 
    cbind(Parameter = rownames(x$anova_table), .)
  
  aov_es_table <- full_join(aov_eta_table, aov_d_table[, c("Parameter", "d")], by = "Parameter")
  aov_es_table$ll[!is.na(aov_d_table$ll)] <- aov_d_table$ll[!is.na(aov_d_table$ll)]
  aov_es_table$ul[!is.na(aov_d_table$ul)] <- aov_d_table$ul[!is.na(aov_d_table$ul)]
  aov_es_table$eta[!is.na(aov_d_table$d)] <- NA
  
  aov_es_table <- aov_es_table %>% 
    mutate(
      eta = printnum(eta, gt1 = FALSE, digits = 3, na_string = "")
      , d = printnum(d, na_string = "")
      , estimate = paste0(eta, d)
      , CI = 100*CI
    ) %>% 
    rowwise() %>% 
    mutate(
      ci = print_confint(ll, ul, gt1 = d != "", digits = 2 + (d == ""))
    ) %>% 
    label_variables(
      eta = "\\hat\\eta^2" %>% { if(is_partial) paste0(., "_p") else if(is_generalized) paste0(., "_G") else . }
    ) # %>% 
  # select(estimate, ci)
  
  res <- cbind(aov_table, aov_es_table)
  
  class(res) <- c("apa_results_table", class(res))

  glue_apa_results(
    res
    , between_vars = x$anova_table$between
    , intercept = if(isTRUE(ellipsis$intercept)) c(TRUE, rep(FALSE, nrow(aov_table) - 1)) else rep(FALSE, nrow(aov_table))
    , est_glue = "$<<ifelse(!eta == '', svl(eta), paste0('d', ifelse(!between_vars & !intercept, '_z', '')))>> = <<estimate>>$, <<as.integer(CI)>>% $<<ci>>$"
    , stat_glue = "$F(<<df>>, <<df.residual>>) = <<statistic>>$, $<<svl(mse)>> = <<mse>>$, $p <<papaja:::add_equals(p.value)>>$"
    , term_names = names(apa_print(x, ...)$statistic)[as.numeric(rownames(aov_table))]
  )
}

apa_print_ps.emmGrid <- function(x, model, est_name = NULL, ...) {
  apa_table <- apa_print(x, ...)$table
  
  effect_size <- eff_size(
    x
    , sigma = sqrt(mean((data.frame(x)$SE * sqrt(df.residual(model)))^2))
    , edf = df.residual(model)
    , method = "identity"
  ) %>%
    tibble::as_tibble() %>% 
    rename(
      estimate = effect.size
      , conf.low = lower.CL
      , conf.high = upper.CL
    ) %>% 
    rowwise() %>% 
    mutate(
      conf.int = print_confint(conf.low, conf.high)
      , estimate = printnum(estimate)
    )
  
  apa_table$estimate <- effect_size$estimate
  apa_table$ci <- NULL
  apa_table$conf.int <- effect_size$conf.int
  variable_label(apa_table$conf.int) <- "95% CI"
  
  if(!is.null(est_name)) variable_label(apa_table$estimate) <- est_name
  
  glue_apa_results(
    apa_table
    , est_glue = papaja:::construct_glue(apa_table, "estimate")
    , stat_glue = papaja:::construct_glue(apa_table, "statistic")
    , term_names = names(apa_print(x)$statistic)
  )
}


