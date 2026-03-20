
# Libraries ---------------------------------------------------------------

library("targets")
library("tarchetypes")
library("rlang")

# Configure plan execution ------------------------------------------------

scripts <- list.files(path = "./R", pattern = "*.r", full.names = TRUE)
sourced <- sapply(scripts, source, .GlobalEnv)

options(tidyverse.quiet = TRUE)

tar_option_set(
  packages = c(
    "dplyr"
    , "tidyr"
  )
  , storage = "main"
  , retrieval = "main"
  , memory = "transient"
  , garbage_collection = TRUE
  , error = "continue"
  , workspace_on_error = TRUE
)

# Parallelized execution
library("future")
options("future.alive.timeout" = 120)

plan(multisession, workers = 3L)


# Define plan -------------------------------------------------------------

otm2_path <- "./otm2/results"
raw_data_path <- file.path(otm2_path, "data_raw")
processed_data_path <- file.path(otm2_path, "data_processed")
codebook_path <- file.path(otm2_path, "codebooks")

list(
  # Read data --------------------------------------------------------------
  tar_target(otm2_n_mcmc_samples, 1e6)
  , tar_read_factory(
    x = "demo"
    , experiment = "otm2"
    , path = raw_data_path
    , pattern = "Demographics"
    , quote = "~" # Participants used " in their input
  )
  , tar_target(
    otm2_demo_codebook
    , otm2_demo |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Age = "Age in years (open response)"
        , Study = "Field of study (open response)"
        , Gender = "Gender (open response)"
        , Goal = "What do you think was the goal of the experiment? (open response)"
        , Comment = "Any further comments (open response)"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "data_raw/otm2_demographics_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_read_factory(
    x = "eval"
    , experiment = "otm2"
    , path = raw_data_path
    , pattern = "Eval"
  )
  , tar_target(
    otm2_eval_codebook
    , otm2_eval |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Florida, Williams, HongKong, Illinois, Yale)"
        , Name = "Name of evaluation target (Bob)"
        , Block = "Block of learning procedure (1 vs. 2)"
        , ValenceBlock = "Valence of behavior description and briefly flashed words in block (1 = Positive behavior/negative flashed words in first block vs. 2 = Negative behavior/positive flashed words in first block)"
        , MeasureOrder = "Order of attitude measures (1 = Implicit-explicit vs. 2 = Explicit-implicit)"
        , Eval1 = "Evaluation of Bob on a 9-point Likert scale: How likable is Bob? (1 = very unlikable, 9 = very likable)"
        , Eval2 = "Evaluation of Bob on a 9-point Likert scale: I think that Bob is (1 = Bad, 9 = Good)"
        , Eval3 = "Evaluation of Bob on a 9-point Likert scale: I think that Bob is (1 = Mean, 9 = Pleasant)"
        , Eval4 = "Evaluation of Bob on a 9-point Likert scale: I think that Bob is (1 = Disagreeable, 9 = Agreeable)"
        , Eval5 = "Evaluation of Bob on a 9-point Likert scale: I think that Bob is (1 = Uncaring, 9 = Caring)"
        , Eval6 = "Evaluation of Bob on a 9-point Likert scale: I think that Bob is (1 = Cruel, 9 = Kind)"
        , Eval7 = "Evaluation of Bob on a 'feeling thermometer' scale:  (Extremely unfavorable = 0-100 = Extremely favorable)"
        , computerName = "Computer used for participation"
        , timeStamp = "Time of participation [YYYY-MM-DD_HH.MM.SS.SSSSSS]" 
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "data_raw/otm2_eval_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_read_factory(
    x = "iat"
    , experiment = "otm2"
    , path = raw_data_path
    , pattern = "IAT"
  )
  , tar_target(
    otm2_iat_codebook
    , otm2_iat |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Florida, Williams, HongKong, Illinois, Yale)"
        , Block = "Block of learning procedure (1 vs. 2)"
        , Combination = "Combination of categories in the IAT (1 = Combination 1: Bob = negative in Block 3 & 4 vs. 2 = Combination 2: Bob = negative in Block 6 & 7)"
        , ValenceBlock = "Valence of behavior description and briefly flashed words in block (1 = Positive behavior/negative flashed words in first block vs. 2 = Negative behavior/positive flashed words in first block)"
        , MeasureOrder = "Order of attitude measures (1 = Implicit-explicit vs. 2 = Explicit-implicit)"
        , IATBlock = "Block of IAT (1, 2, 34 (critical), 5, or 67 (critical))"
        , Stimulus = "Stimulus presented in the trial (words or faces)"
        , Category = "Category of the stimulus (Image vs. Text)"
        , Type = "Type of stimulus (Bob vs. non-Bob vs positive vs. negative)"
        , keyToPress = "Correct response in the trial (d vs. k)"
        , keyPress = "Key pressed by the participant in the trial (d vs. k vs. ['d', 'k'] vs. ['k', 'd'])"
        , Correct = "Whether the participant's first response in the trial was correct (correct vs. error)"
        , RT = "Response time in seconds for the participant's first response in the trial"
        , RTafterError = "Response time in seconds until correct response (0 if the participant responded correctly on the first response)"
        , computerName = "Computer used for participation"
        , timeStamp = "Time of participation [YYYY-MM-DD_HH.MM.SS.SSSSSS]" 
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "data_raw/otm2_iat_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_read_factory(
    x = "mem"
    , experiment = "otm2"
    , path = raw_data_path
    , pattern = "MemTest"
  )
  , tar_target(
    otm2_mem_codebook
    , otm2_mem |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Florida, Williams, HongKong, Illinois, Yale)"
        , Block = "Block of learning procedure (2)"
        , ValenceBlock = "Valence of behavior description and briefly flashed words in block (1 = Positive behavior/negative flashed words in first block vs. 2 = Negative behavior/positive flashed words in first block)"
        , MeasureOrder = "Order of attitude measures (1 = Implicit-explicit vs. 2 = Explicit-implicit)"
        , NumbercorrectIdent = "Number of correct responses in recognition test for briefly flashed words (0-20)"
        , chosenItems = "Comma-separated list of the 20 words identified by the participant as 'old' in the recognition test for briefly flashed words"
        , correctList = "Comma-separated list indicating for each of the words identified as 'old' in the recognition test whether it was indeed old (correctIdent) or new (falseIdent)"
        , computerName = "Computer used for participation"
        , timeStamp = "Time of participation [YYYY-MM-DD_HH.MM.SS.SSSSSS]"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "data_raw/otm2_memtest_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_target(
    otm2_log_paths
    , list.files(
      !!raw_data_path
      , pattern = "ScreenLog"
      , recursive = TRUE
      , full.names = TRUE
    )
    , deployment = "main"
  )
  , tar_target(
    otm2_log_files
    , otm2_log_paths
    , format = "file"
    , pattern = map(otm2_log_paths)
    , deployment = "main"
  )
  , tar_target(
    otm2_log
    , {
      logs <- lapply(
        otm2_log_files
        , \(x) as.numeric(strsplit(readLines(x), ", ")[[1]])
      ) |>
        setNames(basename(otm2_log_files))

      data.frame(
        ParticipantNumber = names(logs) |>
          stringr::str_extract("_\\d+") |>
          gsub(pattern = "_", replacement = "") |>
          as.numeric()
        , frameRate = sapply(
          logs
          , \(x) round(median(1 / x))
        )
      )
    }
    , deployment = "main"
  )

  # Process data -----------------------------------------------------------
  , tar_target(
    otm2_wrong_framerate
    , otm2_log |>
      filter(!frameRate %in% c(75 + -3:3, 100 + -3:3)) |>
      pull(ParticipantNumber) |>
      as.character()
  )
  , tar_target(
    otm2_technical_failure
    , c("101")
  )
  , tar_target(
    otm2_noncompliance
    , c("169")
  )
  , tar_target(
    otm2_exclude
    , c(
      otm2_wrong_framerate
      , otm2_technical_failure
      , otm2_noncompliance
    ) |>
      unique()
  )
  , tar_target(
    otm2_eval2
    , otm2_eval %>%
      mutate_at(vars(starts_with("Eval")), scale) %>%
      select(starts_with("Eval")) %>%
      rowwise() %>%
      do(data.frame(Eval = mean(unlist(.)))) %>% 
      bind_cols(otm2_eval, .) %>%
      mutate(
        ParticipantNumber = factor(ParticipantNumber)
        , ValenceBlock = ifelse(
          ValenceBlock == 1, "Positive-negative", "Negative-positive"
        ) %>% factor()
        , MeasureOrder = ifelse(
          MeasureOrder == 1, "Implicit-explicit", "Explicit-implicit"
        ) %>% factor()
        , Block = factor(Block)
      ) |>
        filter(!as.character(ParticipantNumber) %in% otm2_exclude) |>
        droplevels()
    , packages = c("dplyr")
  )
  , tar_target(
    otm2_iat2
    , otm2_iat %>%
      mutate(
        ParticipantNumber = factor(ParticipantNumber)
        , ValenceBlock = ifelse(
          ValenceBlock == 1, "Positive-negative", "Negative-positive"
        ) %>% factor()
        , MeasureOrder = ifelse(
          MeasureOrder == 1, "Implicit-explicit", "Explicit-implicit"
        ) %>% factor()
        , Block = factor(Block)
        , IATBlock = factor(paste0("Block", IATBlock))
      ) %>%
      dplyr::filter(IATBlock %in% c("Block34", "Block67")) %>%
      mutate(
        Correct = ifelse(Correct == "correct", 1, 0)
        , RT = ifelse(Correct == 1, RT, RTafterError)
        , cleanRT = ifelse(RT < 0.3, 0.3, RT)
        , cleanRT = ifelse(cleanRT > 3, 3, cleanRT)
        , logCleanRT = log(cleanRT)
      ) |>
        filter(!as.character(ParticipantNumber) %in% otm2_exclude) |>
        droplevels()
    , packages = c("dplyr")
  )
  , tar_target(
    otm2_memory
    , {
      demo <- left_join(otm2_demo, otm2_log, by = "ParticipantNumber")
      
      left_join(otm2_mem, demo, by = "ParticipantNumber") |>
        mutate(
          ParticipantNumber = factor(ParticipantNumber)
          , ValenceBlock = ifelse(
              ValenceBlock == 1, "Positive-negative", "Negative-positive"
            ) %>% factor()
          , MeasureOrder = ifelse(
              MeasureOrder == 1, "Implicit-explicit", "Explicit-implicit"
            ) %>% factor()
          , Block = factor(Block)
          , Country = factor(
              ifelse(Location == "HongKong", "Hong Kong",  "USA")
            )
          , Duration = factor(
              ifelse(Location %in% c("Florida", "Williams"), "13", "20")
              , levels = c("13", "20")
            )
          , Location = if_else(Location == "HongKong", "Hong Kong", Location) |>
            factor(levels = c("Florida", "Williams", "Hong Kong", "Illinois", "Yale"))
          , Accuracy = NumbercorrectIdent / 20
          , Age = gsub("^\\D", "", Age)
          , Age = as.numeric(Age)
          , Gender = case_when(
            grepl("^(f|cis-f|w)", Gender, ignore.case = TRUE) ~ "female"
            , grepl("^m", Gender, ignore.case = TRUE) ~ "male"
            , grepl("non", Gender, ignore.case = TRUE) ~ "nonbinary"
          )
        ) |>
        filter(!as.character(ParticipantNumber) %in% otm2_exclude) |>
        droplevels()
    }
    , packages = c("dplyr")
  )
  , tar_target(
    otm2_attitudes
    , {
      otm2_analysis_factors <- c("ParticipantNumber", "Location", "Block", "ValenceBlock")
  
      otm2_iat2 %>%
        group_by(ParticipantNumber, Location, MeasureOrder, Block, IATBlock, Combination, ValenceBlock) %>%
        summarize(meanRT = mean(logCleanRT), nRT = length(logCleanRT)) %>%
        ungroup() %>%
        tidyr::spread(IATBlock, meanRT) %>%
        # Combination 1: Combination 1 (Bob = negative) in Block 3 & 4
        # Combination 2: Combination 1 (Bob = negative) in Block 6 & 7
        mutate(
          IATscore = ifelse(
            Combination == 1
            , Block34 - Block67
            , Block67 - Block34
          )
        ) %>%
        select(c(all_of(otm2_analysis_factors), "IATscore")) %>%
        left_join(
          select(otm2_eval2, c(all_of(otm2_analysis_factors), "Eval"))
          , by = otm2_analysis_factors
        ) |>
        left_join(
          select(otm2_memory, ParticipantNumber, frameRate)
          , by = "ParticipantNumber"
        ) %>% 
        mutate(
          ParticipantNumber = factor(ParticipantNumber)
          , Duration = factor(
            ifelse(Location %in% c("Florida", "Williams"), "13", "20")
            , levels = c("13", "20")
          )
          , Country = factor(
            ifelse(Location == "HongKong", "Hong Kong",  "USA")
          )
          , Location = if_else(Location == "HongKong", "Hong Kong", Location) |>
            factor(levels = c("Florida", "Williams", "Hong Kong", "Illinois", "Yale"))
        ) |>
        filter(!as.character(ParticipantNumber) %in% otm2_exclude) |>
        droplevels()
    }
    , packages = c("dplyr", "tidyr")
  )
  , tar_target(
    otm2_attitudes_collapsed
    , {
      otm2_attitudes %>%
      mutate(
        Block = ifelse(
          ValenceBlock == "Negative-positive"
          , 3 - as.numeric(as.character(Block))
          , Block
        ) %>% factor()
      ) %>%
      select(-ValenceBlock) %>%
      mutate(
        Eval = scale(Eval) %>% as.vector()
        , IATscore = scale(IATscore) %>% as.vector()
      ) %>%
      tidyr::gather("Measure", "Attitude", Eval, IATscore)
    }
    , packages = c("dplyr", "tidyr")
  )
  , tar_target(
    otm2_attitudes_share
    , saveRDS(
      otm2_attitudes
      , file = file.path(!!processed_data_path, "otm2_attitudes.rds")
    )
    , format = "file"
    , deployment = "main"
  )
  , tar_target(
    otm2_attitudes_codebook
    , otm2_attitudes |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Florida, Williams, Hong Kong, Illinois, Yale)"
        , Block = "Block of learning procedure (1 vs. 2)"
        , ValenceBlock = "Order of valence of behavior description (Positive-negative vs. Negative-positive)"
        , IATscore = "Mean difference of cleaned log-transformed RTs between congruent (Bob & negative words) and incongruent (Bob & positive words) blocks"
        , Eval = "Average of the z-standardized evaluative Likert-scale responses"
        , frameRate = "Frame rate [Hz]"
        , Duration = "Presentation duration of briefly flashed words (13 ms vs. 20 ms)"
        , Country = "Country of data collection (USA vs. Hong Kong)"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "otm2_attitudes_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_target(
    otm2_attitudes_collapsed_share
    , saveRDS(
      otm2_attitudes_collapsed
      , file = file.path(!!processed_data_path, "otm2_attitudes_collapsed.rds")
    )
    , format = "file"
    , deployment = "main"
  )
  , tar_target(
    otm2_attitudes_collapsed_codebook
    , otm2_attitudes_collapsed |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Florida, Williams, Hong Kong, Illinois, Yale)"
        , Block = "Block of learning procedure recoded such that 1 represents the block with positive behavior description and 2 the block with negative behavior description (1 vs. 2)"
        , Measure = "Type of attitude measure (Eval vs. IATscore)"
        , Attitude = "Average of the z-standardized evaluative Likert-scale responses or mean difference of cleaned log-transformed RTs between congruent (Bob & negative words) and incongruent (Bob & positive words) blocks (each z-standardized within measure)"
        , frameRate = "Frame rate [Hz]"
        , Duration = "Presentation duration of briefly flashed words (13 ms vs. 20 ms)"
        , Country = "Country of data collection (USA vs. Hong Kong)"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "otm2_attitudes_collapsed_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_target(
    otm2_memory_share
    , saveRDS(
      otm2_memory
      , file = file.path(!!processed_data_path, "otm2_memory.rds")
    )
    , format = "file"
    , deployment = "main"
  )
  , tar_target(
    otm2_memory_codebook
    , otm2_memory |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Florida, Williams, Hong Kong, Illinois, Yale)"
        , Block = "Block of learning procedure (2)"
        , ValenceBlock = "Order of valence of behavior description (Positive-negative vs. Negative-positive)"
        , NumbercorrectIdent = "Number of correct responses in recognition test for briefly flashed words (0-20)"
        , chosenItems = "Comma-separated list of the words identified by the participant as 'old' in the recognition test for briefly flashed words"
        , correctList = "Comma-separated list indicating for each of the words identified as 'old' in the recognition test whether it was indeed old (correctIdent) or new (falseIdent)"
        , MeasureOrder = "Order of attitude measures (Implicit-explicit vs. Explicit-implicit)"
        , computerName = "Computer used for participation"
        , timeStamp = "Time of participation [YYYY-MM-DD_HH.MM.SS.SSSSSS]"
        , Age = "Age in years"
        , Study = "Field of study"
        , Gender = "Gender (male, female, nonbinary)"
        , Goal = "Participants' guess of the study's goal in their own words"
        , Comment = "Participants' comments in their own words"
        , frameRate = "Frame rate [Hz]"
        , Duration = "Presentation duration of briefly flashed words (13 ms vs. 20 ms)"
        , Country = "Country of data collection (USA vs. Hong Kong)"
        , Accuracy = "Relative frequency of correct responses in recognition test for briefly flashed words (0-1)"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "otm2_memory_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )

  # Bayesian replication analysis -----------------------------------------
  ## Contsturct model matrices
  , tar_target(
    otm2_unconstrained_model_matrix
    , {
      effect_matrix <- BayesFactor_design_matrix(
        y ~ Measure + Block + Duration
        , data = otm2_attitudes_collapsed
        , whichRandom = "ParticipantNumber"
      ) |>
        as.matrix()

      random_intercpet_matrix <- BayesFactor:::oneDesignMatrix(
        trm = "ParticipantNumber"
        , data = otm2_attitudes_collapsed
        , dataTypes = c("ParticipantNumber" = "random")
      ) |>
        as.matrix()

      unconstrained_simple_effect_matrix <- effect_matrix |>
        as.matrix() |>
        as.data.frame() |>
        rename(
          eta = Duration_redu_1    # Presentation duration effect
          , measure = Measure_redu_1
          , block = Block_redu_1
        ) |>
        mutate(
          measure = measure < 0
          , alpha = block * measure # Simple block effect for attitude ratings
          , beta = block * !measure # Simple block effect for IAT scores
          , tau = alpha * eta       # Presentation duration effect on simple block effect for attitude ratings
          , upsilon = beta * eta    # Presentation duration effect on simple block effect for IAT scores
        ) |>
        dplyr::select(eta, alpha, tau, beta, upsilon) |>
        as.matrix()

      cbind(
        unconstrained_simple_effect_matrix
        , random_intercpet_matrix
        # Random slopes for simple block effect for attitude ratings
        , (random_intercpet_matrix * unconstrained_simple_effect_matrix[, "alpha"]) |>
          as.data.frame() |>
          rename_with(~ paste0("alpha.&.", .), everything()) |>
          as.matrix()
        # Random slopes for simple block effect for IAT scores
        , (random_intercpet_matrix * unconstrained_simple_effect_matrix[, "beta"]) |>
          as.data.frame() |>
          rename_with(~ paste0("beta.&.", .), everything()) |>
          as.matrix()
      )
    }
    , packages = c("dplyr", "BayesFactor")
  )
  , tar_target(
    otm2_no_duration_effect_model_matrix
    , otm2_unconstrained_model_matrix[, -which(colnames(otm2_unconstrained_model_matrix) %in% c("tau", "upsilon"))]
  )
  , tar_target(
    otm2_null_model_matrix
    , otm2_no_duration_effect_model_matrix[, -which(colnames(otm2_no_duration_effect_model_matrix) %in% c("alpha", "beta"))]
  )
  
  ## Fit models
  , tar_target(
    otm2_no_effect
    , n_way_anova(
      y = otm2_attitudes_collapsed$Attitude
      , X = otm2_null_model_matrix
      , iterations = otm2_n_mcmc_samples
      , seed = 847984132
    )
    , packages = c("BayesFactor")
  )
  , tar_target(
    otm2_unconstrained
    , n_way_anova(
      y = otm2_attitudes_collapsed$Attitude
      , X = otm2_unconstrained_model_matrix
      , iterations = otm2_n_mcmc_samples
      , seed = 847984132
    )
    , packages = c("BayesFactor")
  )
  , tar_target(
    otm2_no_duration_effect
    , n_way_anova(
      y = otm2_attitudes_collapsed$Attitude
      , X = otm2_no_duration_effect_model_matrix
      , iterations = otm2_n_mcmc_samples
      , seed = 847984132
    )
    , packages = c("BayesFactor")
  )
  , tar_target(
    otm2_unconstrained_samples_raw
    , {
      samples <- n_way_anova(
        y = otm2_attitudes_collapsed$Attitude
        , X = otm2_unconstrained_model_matrix
        , posterior = TRUE
        , iterations = otm2_n_mcmc_samples
        , seed = 847984132
      )
      colnames(samples)[1:ncol(otm2_unconstrained_model_matrix) + 1] <- colnames(otm2_unconstrained_model_matrix)
      
      samples
    }
    , packages = c("BayesFactor")
    , deployment = "main"
  )
  , tar_target(
    otm2_unconstrained_samples
    , {
      a <- BayesFactor:::fixedFromRandomProjection(2) |> as.vector()
      b <- a

      otm2_unconstrained_samples_raw |>
        as.data.frame() |>
        mutate(
          a1 = a[1]
          , a2 = a[2]
          , b1 = b[1]
          , b2 = b[2]
        ) |>
        duckplyr::as_duckdb_tibble() |>
        select(alpha, beta, tau, upsilon, a1:b2) |>
        mutate(
          alpha_13           = a1 * (alpha + b1 * tau)
          , alpha_20         = a1 * (alpha + b2 * tau)
          , alpha            = a1 * alpha
          , Eval_13          = 2 * alpha_13
          , Eval_20          = 2 * alpha_20
          , Eval_Overall     = 2 * alpha
          , beta_13          = a1 * (beta + b1 * upsilon)
          , beta_20          = a1 * (beta + b2 * upsilon)
          , beta             = a1 * beta
          , IATscore_13      = 2 * beta_13
          , IATscore_20      = 2 * beta_20
          , IATscore_Overall = 2 * beta
        ) |>
        as.matrix()
    }
    , packages = c("BayesFactor", "dplyr", "duckplyr")
    , deployment = "main"
  )

  ## Posterior postdictions
  , tar_target(
    otm2_unconstrained_pp
    , {
      otm2_unconstrained_samples |>
        as.data.frame() |>
        duckplyr::as_duckdb_tibble() |>
        select(matches("Eval|IATscore")) |>
        mutate(iteration = row_number()) |>
        tidyr::pivot_longer(cols = matches("Eval|IATscore"), names_to = c("Measure", "Duration"), values_to = "value", names_sep = "_") |>
        tidyr::spread(Measure, value)
    }
    , packages = c("dplyr", "tidyr", "duckplyr")
    , deployment = "main"
  )

  ## Sensitivity analysis for Bayesian replication analysis
  , tar_target(otm2_n_mcmc_samples_sensitivity, 5e5)
  , tar_target(
    sensitivity_rscales
    , expand.grid(
        rating = seq(sqrt(2)/2, 2, length.out = 2)
        , iat = seq(0.2, 1, length.out = 2)
      ) |>
        dplyr::filter(iat <= rating) |>
        as.matrix() |>
        (\(x) x / sqrt(2))() |> # Rescale to ANOVA specification (see https://forum.cogsci.nl/discussion/3746/bayesfactor-scale-of-cauchy-prior-in-t-tests-and-anova)
        as.data.frame() |>
        dplyr::rowwise() |>
        targets::tar_group()
    , packages = c("dplyr", "targets")
    , iteration = "group"
  )
  , tar_target(
    otm2_prior_sensitivity_analysis
    , {
      rscales <- c(
        eta = 0.5
        , alpha = unname(sensitivity_rscales$rating)
        , tau = 0.5
        , beta = unname(sensitivity_rscales$iat)
        , upsilon = 0.5
      )

      # unconstrained <- n_way_anova(
      #   y = otm2_attitudes_collapsed$Attitude
      #   , X = otm2_unconstrained_model_matrix
      #   , fixed = rscales
      #   , iterations = otm2_n_mcmc_samples_sensitivity
      #   , seed = 847984132
      # )

      # unconstrained_bf <- exp(unconstrained$bf - otm2_no_effect$bf)

      unconstrained_samples <- n_way_anova(
        y = otm2_attitudes_collapsed$Attitude
        , X = otm2_unconstrained_model_matrix
        , fixed = rscales
        , posterior = TRUE
        , iterations = otm2_n_mcmc_samples_sensitivity
        , seed = 847984132
      )
      colnames(unconstrained_samples)[1:ncol(otm2_unconstrained_model_matrix) + 1] <- colnames(otm2_unconstrained_model_matrix)

      a <- BayesFactor:::fixedFromRandomProjection(2) |> as.vector()

      unconstrained_samples <- unconstrained_samples |>
        as.data.frame() |>
        select(alpha, beta) |>
        mutate(
          a1 = a[1]
          , alpha            = a1 * alpha
          , beta             = a1 * beta
        ) |>
        as.matrix()

      same_direction_boost <- 4 * (
        (sum(
          unconstrained_samples[, "alpha"] > 0 &
          unconstrained_samples[, "beta"] > 0
        ) + 1) / (nrow(unconstrained_samples) + 2)
      )
      # same_direction_bf <- unconstrained_bf * same_direction_boost

      opposite_direction_boost <- 4 * (
        (sum(
          unconstrained_samples[, "alpha"] > 0 &
          unconstrained_samples[, "beta"] < 0
        ) + 1) / (nrow(unconstrained_samples) + 2)
      )
      # opposite_direction_bf <- unconstrained_bf * opposite_direction_boost

      data.frame(
        rating = sensitivity_rscales$rating
        , iat = sensitivity_rscales$iat
        # , no_effect = otm2_no_effect$bf
        # , unconstrained = unconstrained$bf
        # , unconstrained_bf = unconstrained_bf
        # , same_direction_boost = same_direction_boost
        # , opposite_direction_boost = opposite_direction_boost
        , bf_one_mind_two_minds = same_direction_boost / opposite_direction_boost
        , bf_one_mind_any_effect = same_direction_boost
      )
    }
    , packages = c("BayesFactor", "dplyr")
    , pattern = map(sensitivity_rscales)
  )
)
