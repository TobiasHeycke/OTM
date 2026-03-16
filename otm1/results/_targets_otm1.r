
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

otm1_path <- "./otm1/results"
raw_data_path <- file.path(otm1_path, "data_raw")
processed_data_path <- file.path(otm1_path, "data_processed")
codebook_path <- file.path(otm1_path, "codebooks")

list(
  # Read data --------------------------------------------------------------
  tar_target(otm1_n_mcmc_samples, 5e6)
  , tar_read_factory(
    x = "demo"
    , experiment = "otm1"
    , path = raw_data_path
    , pattern = "Demographics"
    , quote = "~" # Participants used " in their input
  )
  , tar_target(
    otm1_demo_codebook
    , otm1_demo |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Age = "Age in years (open response)"
        , Study = "Field of study (open response)"
        , Gender = "Gender (open response)"
        , Goal = "What do you think was the goal of the experiment? (open response)"
        , Comment = "Any further comments (open response)"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "data_raw/otm1_demo_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_read_factory(
    x = "eval"
    , experiment = "otm1"
    , path = raw_data_path
    , pattern = "Eval"
  )
  , tar_target(
    otm1_eval_codebook
    , otm1_eval |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Cologne, Ghent, Harvard)"
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
        file = file.path(!!codebook_path, "data_raw/otm1_eval_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_read_factory(
    x = "iat"
    , experiment = "otm1"
    , path = raw_data_path
    , pattern = "IAT"
  )
  , tar_target(
    otm1_iat_codebook
    , otm1_iat |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Cologne, Ghent, Harvard)"
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
        file = file.path(!!codebook_path, "data_raw/otm1_iat_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_read_factory(
    x = "mem"
    , experiment = "otm1"
    , path = raw_data_path
    , pattern = "MemTest"
  )
  , tar_target(
    otm1_mem_codebook
    , otm1_mem |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Cologne, Ghent, Harvard)"
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
        file = file.path(!!codebook_path, "data_raw/otm1_mem_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_target(
    otm1_log_paths
    , list.files(
      !!raw_data_path
      , pattern = "ScreenLog"
      , recursive = TRUE
      , full.names = TRUE
    )
    , deployment = "main"
  )
  , tar_target(
    otm1_log_files
    , otm1_log_paths
    , format = "file"
    , pattern = map(otm1_log_paths)
    , deployment = "main"
  )
  , tar_target(
    otm1_log
    , {
      logs <- lapply(
        otm1_log_files
        , \(x) as.numeric(strsplit(readLines(x), ", ")[[1]])
      ) |>
        setNames(basename(otm1_log_files))

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
  , tar_target(
    otm1_stimuls_translations_file
    , file.path(!!otm1_path, "IAT_word_translations.tab")
    , format = "file"
    , deployment = "main"
  )
  , tar_target(
    otm1_stimulus_translations
    , read.delim(otm1_stimuls_translations_file, header = FALSE)
    , deployment = "main"
  )

  # Process data -----------------------------------------------------------
  , tar_target(
    otm1_technical_failure
    , c("345", "347")
  )
  , tar_target(
    otm1_eval2
    , otm1_eval %>%
      mutate_at(vars(starts_with("Eval")), scale) %>%
      select(starts_with("Eval")) %>%
      rowwise() %>%
      do(data.frame(Eval = mean(unlist(.)))) %>% 
      bind_cols(otm1_eval, .) %>%
      mutate(
        ParticipantNumber = factor(ParticipantNumber)
        , Location = factor(Location)
        , ValenceBlock = ifelse(
          ValenceBlock == 1, "Positive-negative", "Negative-positive"
        ) %>% factor()
        , MeasureOrder = ifelse(
          MeasureOrder == 1, "Implicit-explicit", "Explicit-implicit"
        ) %>% factor()
        , Block = factor(Block)
      ) |>
      filter(!ParticipantNumber %in% otm1_technical_failure) |>
      droplevels()
    , packages = c("dplyr")
  )
  , tar_target(
    otm1_iat2
    , {
      german_iat_words <- match(otm1_iat$Stimulus, otm1_stimulus_translations$German)
      dutch_iat_words <- match(otm1_iat$Stimulus, otm1_stimulus_translations$Dutch)
      
      otm1_iat |>
        mutate(
          translatedStimulus = Stimulus
          , translatedStimulus = ifelse(
            !is.na(german_iat_words)
            , otm1_stimulus_translations$English[na.omit(german_iat_words)]
            , translatedStimulus
          )
          , translatedStimulus = ifelse(
            !is.na(dutch_iat_words)
            , otm1_stimulus_translations$English[na.omit(dutch_iat_words)]
            , translatedStimulus
          )
          , ParticipantNumber = factor(ParticipantNumber)
          , Location = factor(Location)
          , ValenceBlock = ifelse(
            ValenceBlock == 1, "Positive-negative", "Negative-positive"
          ) %>% factor()
          , MeasureOrder = ifelse(
            MeasureOrder == 1, "Implicit-explicit", "Explicit-implicit"
          ) %>% factor()
          , Block = factor(Block)
          , IATBlock = factor(paste0("Block", IATBlock))

          # Wolsiefer et al. (2017, p. 1198; doi: 10.3758/s13428-016-0779-0)
          , imageType = ifelse(
            Category == "Image"
            , ifelse(Type == "Bob", 1, -1)
            , 0
          )
          , wordType = ifelse(
            Category == "Text"
            , ifelse(Type == "neg", 1, -1)
            , 0
          )
        ) %>%
        dplyr::filter(IATBlock %in% c("Block34", "Block67")) %>%
        mutate(
          Correct = ifelse(Correct == "correct", 1, 0)
          , RT = ifelse(Correct == 1, RT, RTafterError)
          , cleanRT = ifelse(RT < 0.3, 0.3, RT)
          , cleanRT = ifelse(cleanRT > 3, 3, cleanRT)
          , logCleanRT = log(cleanRT)

          # Wolsiefer et al. (2017, p. 1198; doi: 10.3758/s13428-016-0779-0)
          # Combination 1: Combination 1 (Bob = negative) in Block 3 & 4
          # Combination 2: Combination 1 (Bob = negative) in Block 6 & 7
          , Congruent = ifelse(
            # Bob = negative
            (Combination == 1 & IATBlock == "Block34") |
            (Combination == 2 & IATBlock == "Block67")
            , "Bob & negative" # -1
            , "Bob & positive" # 1
          ) %>% factor(levels = c("Bob & negative", "Bob & positive"))
        ) |>
        filter(!ParticipantNumber %in% otm1_technical_failure) |>
        droplevels()
    }
    , packages = c("dplyr")
  )
  , tar_target(
    otm1_memory
    , {
      demo <- left_join(otm1_demo, otm1_log, by = "ParticipantNumber")
      
      left_join(otm1_mem, demo, by = "ParticipantNumber") |>
        mutate(
          ParticipantNumber = factor(ParticipantNumber)
          , Location = factor(Location)
          , ValenceBlock = ifelse(
            ValenceBlock == 1, "Positive-negative", "Negative-positive"
          ) %>% factor()
          , MeasureOrder = ifelse(
            MeasureOrder == 1, "Implicit-explicit", "Explicit-implicit"
          ) %>% factor()
          , Block = factor(Block)
          , Accuracy = NumbercorrectIdent / 20
          , Age = gsub("^\\D", "", Age)
          , Age = as.numeric(Age)
          , Gender = case_when(
            grepl("^(f|v|w)", Gender, ignore.case = TRUE) ~ "female"
            , grepl("^m", Gender, ignore.case = TRUE) ~ "male"
            , grepl("^(non|x)", Gender, ignore.case = TRUE) ~ "nonbinary"
          )
        ) |>
        filter(!ParticipantNumber %in% otm1_technical_failure) |>
        droplevels()
    }
    , packages = c("dplyr")
  )
  , tar_target(
    otm1_attitudes
    , {
      otm1_analysis_factors <- c("ParticipantNumber", "Location", "Block", "ValenceBlock")
  
      otm1_iat2 %>%
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
        select(c(all_of(otm1_analysis_factors), "IATscore")) %>%
        left_join(
          select(otm1_eval2, c(all_of(otm1_analysis_factors), "Eval"))
          , by = otm1_analysis_factors
        ) |>
        left_join(
          select(otm1_memory, ParticipantNumber, frameRate)
          , by = "ParticipantNumber"
        ) |>
        filter(!ParticipantNumber %in% otm1_technical_failure) |>
        droplevels()
    }
    , packages = c("dplyr", "tidyr")
  )
  , tar_target(
    otm1_attitudes_collapsed
    , {
      otm1_attitudes %>%
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
    otm1_attitudes_share
    , saveRDS(
      otm1_attitudes
      , file = file.path(!!processed_data_path, "otm1_attitudes.rds")
    )
    , format = "file"
    , deployment = "main"
  )
  , tar_target(
    otm1_attidudes_codebook
    , otm1_attitudes |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Cologne, Ghent, Harvard)"
        , Block = "Block of learning procedure (1 vs. 2)"
        , ValenceBlock = "Order of valence of behavior description (Positive-negative vs. Negative-positive)"
        , IATscore = "Mean difference of cleaned log-transformed RTs between congruent (Bob & negative words) and incongruent (Bob & positive words) blocks"
        , Eval = "Average of the z-standardized evaluative Likert-scale responses"
        , frameRate = "Frame rate [Hz]"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "otm1_attitudes_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_target(
    otm1_attitudes_collapsed_share
    , saveRDS(
      otm1_attitudes_collapsed
      , file = file.path(!!processed_data_path, "otm1_attitudes_collapsed.rds")
    )
    , format = "file"
    , deployment = "main"
  )
  , tar_target(
    otm1_attitudes_collapsed_codebook
    , otm1_attitudes_collapsed |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Cologne, Ghent, Harvard)"
        , Block = "Block of learning procedure recoded such that 1 represents the block with positive behavior description and 2 the block with negative behavior description (1 vs. 2)"
        , Measure = "Type of attitude measure (Eval vs. IATscore)"
        , Attitude = "Average of the z-standardized evaluative Likert-scale responses or mean difference of cleaned log-transformed RTs between congruent (Bob & negative words) and incongruent (Bob & positive words) blocks (each z-standardized within measure)"
        , frameRate = "Frame rate [Hz]"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "otm1_attitudes_collapsed_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )
  , tar_target(
    otm1_memory_share
    , saveRDS(
      otm1_memory
      , file = file.path(!!processed_data_path, "otm1_memory.rds")
    )
    , format = "file"
    , deployment = "main"
  )
  , tar_target(
    otm1_memory_codebook
    , otm1_memory |>
      label_variables(
        ParticipantNumber = "Unique participant ID"
        , Location = "Data collection site (Cologne, Ghent, Harvard)"
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
        , Accuracy = "Relative frequency of correct responses in recognition test for briefly flashed words (0-1)"
      ) |>
      simple_codebook(
        file = file.path(!!codebook_path, "otm1_memory_codebook.csv")
      )
    , format = "file"
    , packages = c("papaja")
    , deployment = "main"
  )

  # Bayesian replication analysis -----------------------------------------
  ## Contsturct model matrices
  , tar_target(
    otm1_unconstrained_model_matrix
    , {
      effect_matrix <- BayesFactor_design_matrix(
        y ~ Measure + Block + Location
        , data = otm1_attitudes_collapsed
        , whichRandom = "ParticipantNumber"
      ) |>
        as.matrix()

      random_intercpet_matrix <- BayesFactor:::oneDesignMatrix(
        trm = "ParticipantNumber"
        , data = otm1_attitudes_collapsed
        , dataTypes = c("ParticipantNumber" = "random")
      ) |>
        as.matrix()

      unconstrained_simple_effect_matrix <- effect_matrix |>
        as.matrix() |>
        as.data.frame() |>
        rename(
          eta1 = Location_redu_1
          , eta2 = Location_redu_2
          , measure = Measure_redu_1
          , block = Block_redu_1
        ) |>
        mutate(
          measure = measure < 0
          , alpha = block * measure # Simple block effect for attitude ratings
          , beta = block * !measure # Simple block effect for IAT scores
          , tau1 = alpha * eta1     # Location effect on simple block effect for attitude ratings
          , tau2 = alpha * eta2     # Location effect on simple block effect for attitude ratings
          , upsilon1 = beta * eta1  # Location effect on simple block effect for IAT scores
          , upsilon2 = beta * eta2  # Location effect on simple block effect for IAT scores
        ) |>
        dplyr::select(eta1, eta2, alpha, tau1, tau2, beta, upsilon1, upsilon2) |>
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
    otm1_no_lab_effect_model_matrix
    , otm1_unconstrained_model_matrix[, -which(colnames(otm1_unconstrained_model_matrix) %in% c("tau1", "tau2", "upsilon1", "upsilon2"))]
  )
  , tar_target(
    otm1_null_model_matrix
    , otm1_no_lab_effect_model_matrix[, -which(colnames(otm1_no_lab_effect_model_matrix) %in% c("alpha", "beta"))]
  )
  
  ## Fit models
  , tar_target(
    otm1_no_effect
    , n_way_anova(
      y = otm1_attitudes_collapsed$Attitude
      , X = otm1_null_model_matrix
      , iterations = otm1_n_mcmc_samples
      , seed = 847984132
    )
    , packages = c("BayesFactor")
  )
  , tar_target(
    otm1_unconstrained
    , n_way_anova(
      y = otm1_attitudes_collapsed$Attitude
      , X = otm1_unconstrained_model_matrix
      , iterations = otm1_n_mcmc_samples
      , seed = 847984132
    )
    , packages = c("BayesFactor")
  )
  , tar_target(
    otm1_no_lab_effect
    , n_way_anova(
      y = otm1_attitudes_collapsed$Attitude
      , X = otm1_no_lab_effect_model_matrix
      , iterations = otm1_n_mcmc_samples
      , seed = 847984132
    )
    , packages = c("BayesFactor")
  )
  , tar_target(
    otm1_unconstrained_samples_raw
    , {
      samples <- n_way_anova(
        y = otm1_attitudes_collapsed$Attitude
        , X = otm1_unconstrained_model_matrix
        , posterior = TRUE
        , iterations = otm1_n_mcmc_samples / 2
        , seed = 847984132
      )
      colnames(samples)[1:ncol(otm1_unconstrained_model_matrix) + 1] <- colnames(otm1_unconstrained_model_matrix)

      samples
    }
    , packages = c("BayesFactor")
    , deployment = "main"
  )
  , tar_target(
    otm1_unconstrained_samples
    , {
      a <- BayesFactor:::fixedFromRandomProjection(2) |> as.vector()
      b <- BayesFactor:::fixedFromRandomProjection(3)

      otm1_unconstrained_samples_raw |>
        as.data.frame() |>
        mutate(
          a1 = a[1]
          , a2 = a[2]
          , b11 = b[1, 1]
          , b21 = b[2, 1]
          , b31 = b[3, 1]
          , b12 = b[1, 2]
          , b22 = b[2, 2]
          , b32 = b[3, 2]
        ) |>
        duckplyr::as_duckdb_tibble() |>
        select(alpha, beta, tau1:upsilon2, a1:b32) |>
        mutate(
          alpha_cologne   = a1 * (alpha + b11 * tau1 + b12 * tau2)
          , alpha_ghent   = a1 * (alpha + b21 * tau1 + b22 * tau2)
          , alpha_harvard = a1 * (alpha + b31 * tau1 + b32 * tau2)
          , alpha         = a1 * alpha
          , Eval_Cologne  = 2 * alpha_cologne
          , Eval_Ghent    = 2 * alpha_ghent
          , Eval_Harvard  = 2 * alpha_harvard
          , Eval_Overall  = 2 * alpha
          , beta_cologne  = a1 * (beta  + b11 * upsilon1 + b12 * upsilon2)
          , beta_ghent    = a1 * (beta  + b21 * upsilon1 + b22 * upsilon2)
          , beta_harvard  = a1 * (beta  + b31 * upsilon1 + b32 * upsilon2)
          , beta          = a1 * beta
          , IATscore_Cologne = 2 * beta_cologne
          , IATscore_Ghent   = 2 * beta_ghent
          , IATscore_Harvard = 2 * beta_harvard
          , IATscore_Overall = 2 * beta
        ) |>
        as.matrix()
    }
    , packages = c("BayesFactor", "dplyr", "duckplyr")
    , deployment = "main"
  )

  ## Posterior postdictions
  , tar_target(
    otm1_unconstrained_pp
    , {
      otm1_unconstrained_samples |>
        as.data.frame() |>
        duckplyr::as_duckdb_tibble() |>
        select(matches("Eval|IATscore")) |>
        mutate(iteration = row_number()) |>
        tidyr::pivot_longer(cols = matches("Eval|IATscore"), names_to = c("Measure", "Location"), values_to = "value", names_sep = "_") |>
        tidyr::spread(Measure, value)
    }
    , packages = c("dplyr", "tidyr", "duckplyr")
    , deployment = "main"
  )

  ## Sensitivity analysis for Bayesian replication analysis
  , tar_target(otm1_n_mcmc_samples_sensitivity, 5e5)
  , tar_target(
    sensitivity_rscales
    , expand.grid(
        rating = seq(sqrt(2)/2, 2, length.out = 3)
        , iat = seq(0.2, 1, length.out = 3)
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
    otm1_prior_sensitivity_analysis
    , {
      rscales <- c(
        eta = 0.5
        , alpha = unname(sensitivity_rscales$rating)
        , tau = 0.5
        , beta = unname(sensitivity_rscales$iat)
        , upsilon = 0.5
      )

      # unconstrained <- n_way_anova(
      #   y = otm1_attitudes_collapsed$Attitude
      #   , X = otm1_unconstrained_model_matrix
      #   , fixed = rscales
      #   , iterations = otm1_n_mcmc_samples_sensitivity
      #   , seed = 847984132
      # )

      # unconstrained_bf <- exp(unconstrained$bf - otm1_no_effect$bf)

      unconstrained_samples <- n_way_anova(
        y = otm1_attitudes_collapsed$Attitude
        , X = otm1_unconstrained_model_matrix
        , fixed = rscales
        , posterior = TRUE
        , iterations = otm1_n_mcmc_samples_sensitivity
        , seed = 847984132
      )
      colnames(unconstrained_samples)[1:ncol(otm1_unconstrained_model_matrix) + 1] <- colnames(otm1_unconstrained_model_matrix)

      a <- BayesFactor:::fixedFromRandomProjection(2) |> as.vector()

      unconstrained_samples <- unconstrained_samples |>
        as.data.frame() |>
        select(alpha, beta) |>
        mutate(
          a1 = a[1]
          , alpha  = a1 * alpha
          , beta = a1 * beta
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
        # , no_effect = otm1_no_effect$bf
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

  ## Linear mixed model for IAT scores
  , tar_target(
    otm1_iat2_lme
    , {
      lme_error_exclusion <- otm1_iat2 %>%
        group_by(ParticipantNumber) %>%
        summarize(Correct = mean(Correct), fast_rate = mean(RT < 0.3)) %>%
        filter(Correct < 0.5 & fast_rate > 0.1) %>%
        pull(ParticipantNumber)

      if(length(lme_error_exclusion) > 0) {
        otm1_iat2_excl <- otm1_iat2 %>%
          filter(!ParticipantNumber %in% otm1_lme_exclusion)
      } else {
        otm1_iat2_excl <- otm1_iat2
      }

      otm1_iat2_excl %>%
        # Wolsiefer et al. (2017, p. 1196; doi: 10.3758/s13428-016-0779-0)
        filter(RT > 0.4 & RT < 10) %>%
        # Wolsiefer et al. (2017, p. 1198; doi: 10.3758/s13428-016-0779-0)
        group_by(ParticipantNumber, Block) %>%
        mutate(RTD = RT / sd(RT)) %>%
        ungroup
    }
    , packages = c("dplyr")
  )
  , tar_target(
    otm1_iat_lmer
    , {
      # Wolsiefer et al. (2017, Erratum; doi: 10.3758/s13428-017-0897-3)
      otm1_iat_lmer_formula <- RTD ~ Congruent * Block * ValenceBlock *
        (Category + wordType + imageType) +
        (Congruent * Block | ParticipantNumber) +
        (Congruent * Block * ValenceBlock | translatedStimulus)

      lmerTest::lmer(
        otm1_iat_lmer_formula
        , data = otm1_iat2_lme
        , control = lmerControl(
          optCtrl = list(maxfun = 10 * 143^2)
          , optimizer = "bobyqa"
        )
      )
    }
    , packages = c("lme4", "lmerTest")
    , deployment = "main"
  )
  # , tar_target(
  #   otm1_iat_lmer_allfit
  #   , {
  #     lme4::allFit(
  #       otm1_iat_lmer
  #       , data = otm1_iat2_lme
  #       , maxfun = 10 * 143^2
  #       , parallel = "snow"
  #       , ncpus = 6L
  #     )
  #   }
  #   , packages = c("lme4")
  #   , deployment = "main"
  # )

  # Render report ---------------------------------------------------------
  , tar_render(
    otm1_analysis
    , path = "./otm1/results/analysis1.Rmd"
    , deployment = "main"
    , quiet = TRUE
  )
)
