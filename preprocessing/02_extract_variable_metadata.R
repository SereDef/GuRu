# here::here() # proj dir "GuRu"

library(dplyr)
# library(haven)
# library(purrr)

last_datawiki_scrape <- (list.files('assets', pattern = 'datawiki_scrape_', 
                                   full.names = TRUE) |> sort(decreasing = TRUE)
                         )[1] |> read.csv()

# TODO: compare with earlier lists and only parse files that are new 

new_files <- last_datawiki_scrape$file_name

# TODO: implement file name cleaning / validator

# e.g. too many files, duplicates [for now keep onlyone, then decide to keep one or resolve]
table(new_files)[table(new_files) > 1]

# file extensions should be removed from the names in principle 
table(tools::file_ext(new_files))

# e.g clean up leftover file extensions
strip_extension <- function(v) sub("\\.[^.]*$", "", v)

new_files <- strip_extension(unique(new_files))

cli::cli_alert_info('{length(new_files)} files to parse')

# File storage (assumed up to date)
file_storage <- "\\\\store/department/genr/isi-store/DATAMANAGEMENT/Datamanagement/Datasets/DATA_WIKI/Files/"

all_files <- list.files(file_storage, recursive = TRUE, full.names = TRUE)

# Find the location of files that are in the list of new_files to parse
matches <- sapply(new_files,  function(f) {
  m0 <- all_files[strip_extension(basename(all_files)) == f] 
  # drop any matching documentation, only tabular data kept
  m0_ext <- tolower(tools::file_ext(m0))
  m0[!m0_ext %in% c('pdf', 'doc', 'docx', 'txt', 'sps')]}, 
  USE.NAMES = TRUE)

counts <- lengths(matches)

not_found <- new_files[counts == 0]
found_once <- matches[counts == 1]
found_many <- matches[counts > 1]

# TODO: handle them later 
cli::cli_alert_danger('{length(not_found)} / {length(new_files)} files not found')
cli::cli_alert_danger('{length(found_many)} / {length(new_files)} files have too many matches')

cli::cli_alert_info('{length(found_once)} / {length(new_files)} files have exactly one match.')

table(tools::file_ext(found_once))

# TODO: handle other file formats, for now focus on sav (majority)
files_to_read <- found_once[tools::file_ext(found_once) == 'sav']

# === Extract info from files ==================================================

# Summarise one vector as a single string
summarise_var <- function(x, max_levels = 10, n_examples = 3) {
  x <- x[!is.na(x)]
  if (length(x) == 0) return("All missing? check!")
  
  # Categorical: factors, or anything with few distinct values
  if (is.factor(x) || n_distinct(x) < max_levels) {
    tab <- table(x)
    extra <- ""
    if (length(tab) > max_levels) {          # many-level factors: show the top ones
      extra <- sprintf("; ... (+%d more levels)", length(tab) - max_levels)
      tab <- sort(tab, decreasing = TRUE)[seq_len(max_levels)]
    }
    return(paste0("[", paste0(names(tab), ": ", tab, collapse = "]["), "]", extra))
  }
  
  # Continuous numbers and dates/datetimes
  if (is.numeric(x)) {
    s <- c(quantile(x, c(0, .25, .5, .75, 1), names = FALSE), mean(x), sd(x))
    s <- if (is.numeric(x)) formatC(s, digits = 4, format = "g") else format(s)
    return(paste0(c("min", "1stQ", "median", "3rdQ", "max", "mean", "sd"), ": ", s,
                  collapse = "; "))
  }
  # Dates / datetimes: type = 1 picks observed values, no arithmetic needed
  if (inherits(x, c("Date", "POSIXt"))) {
    s <- c(quantile(x, c(0, 1, 0.5), type = 1, names = FALSE))
    return(paste0(c("from", "to", "median"), ": ", format(s), collapse = "; "))
  }
  
  # High-cardinality character
  u <- unique(x)
  sprintf("%d unique values", length(u))
          # ; e.g. %s", 
          # paste0('"', head(u, n_examples), '"', collapse = ", "))
}

# One file -> one row per variable
describe_sav <- function(path, ...) {
  raw <- haven::read_sav(path)
  df  <- raw |>
    haven::as_factor() |> # value labels to factor levels
    mutate(across(where(is.character), haven::zap_empty))  # SPSS "" to NA
  
  tibble(
    variable = names(df),
    label    = purrr::map_chr(raw, \(x) attr(x, "label", exact = TRUE) %||% NA_character_),
    type     = purrr::map_chr(df, \(x) class(x)[1]),
    n        = purrr::map_int(df, \(x) sum(!is.na(x))),
    summary  = purrr::map_chr(df, summarise_var, ...)
  )
}

# Don't let single files break everything 
safe_describe <- purrr::safely(describe_sav)

res <- purrr::map(files_to_read, safe_describe, .progress = TRUE)
errors <- purrr::map(res, "error") |> purrr::compact()
result <- purrr::map(res, "result") |> purrr::list_rbind(names_to = "file")

# === Group by unique variables ================================================

# Distinct non-empty values joined with " || ".
# With ignore_formatting = TRUE, values differing only in case/punctuation/spacing
# count as the same (the first spelling is kept).
collapse_distinct <- function(x, sep = " || ", ignore_formatting = FALSE) {
  x <- trimws(x)
  x <- x[!is.na(x) & x != ""]
  key <- if (ignore_formatting) trimws(gsub("[^[:alnum:]]+", " ", tolower(x))) else x
  x <- x[!duplicated(key)]
  if (length(x) == 0) NA_character_ else paste(x, collapse = sep)
}

by_variable <- result |>
  summarise(
    .by = variable,
    label   = collapse_distinct(label, ignore_formatting = TRUE),
    type    = collapse_distinct(type),
    n       = if (min(n) == max(n)) as.character(min(n)) else paste0(min(n), "-", max(n)),
    summary = collapse_distinct(summary),
    files   = paste(unique(file), collapse = "; "),
    n_files = n_distinct(file)
  ) |>
  arrange(desc(n_files))

library(arrow)

arrow::write_parquet(
  by_variable,
  sink = sprintf("assets/variable_metadata_%s.parquet", format(Sys.Date(), "%Y%m%d")),
)

# # --- helpers variable variability ------------------------------------------
# 
# # Labels: ignore case, punctuation and extra whitespace when comparing
# norm_label <- function(x) {
#   x |> tolower() |> gsub(pattern = "[^[:alnum:]]+", replacement = " ") |> trimws()
# }
# 
# # Categorical summaries: drop the counts so only the level names are compared
# # "[boy: 512][girl: 498]" -> "[boy][girl]"
# summary_shape <- function(s) {
#   s |>
#     sub(pattern = "; \\.\\.\\. \\(\\+\\d+ more levels\\)$", replacement = "") |>
#     gsub(pattern = ": (<5|\\d+)\\]", replacement = "]")
# }
# 
# # Pull one statistic (e.g. the median) out of a numeric summary string
# get_stat <- function(s, stat) {
#   suppressWarnings(as.numeric(sub(paste0(".*\\b", stat, ": ([^;]+).*"), "\\1", s)))
# }
# 
# # Relative spread of medians across files: 0 = identical, 0.5 = differ by half
# rel_spread <- function(m) {
#   m <- m[!is.na(m)]
#   if (length(m) < 2) return(NA_real_)
#   if (max(abs(m)) == 0) return(0)
#   diff(range(m)) / max(abs(m))
# }
# 
# # Show up to a few distinct variants, then count the rest
# collapse_some <- function(x, max_show = 3, sep = " || ") {
#   u <- unique(x[!is.na(x)])
#   if (length(u) == 0) return(NA_character_)
#   out <- paste(head(u, max_show), collapse = sep)
#   if (length(u) > max_show) out <- sprintf("%s (+%d more variants)", out, length(u) - max_show)
#   out
# }
# 
# # --- one row per variable --------------------------------------------------
# 
# by_variable <- result |>
#   mutate(
#     label_norm = norm_label(label),
#     shape      = summary_shape(summary),
#     median_num = get_stat(summary, "median")
#   ) |>
#   summarise(
#     .by = variable,
#     # agreement counts first (before the columns below overwrite label/type/n/summary)
#     n_files       = n_distinct(file),
#     n_labels      = n_distinct(label_norm, na.rm = TRUE),
#     n_types       = n_distinct(type),
#     n_summaries   = n_distinct(summary),
#     n_shapes      = n_distinct(shape),
#     median_spread = rel_spread(median_num),
#     # combined values
#     files   = if (n_files > 100) sprintf("# in %d files", n_files)
#     else paste(unique(file), collapse = "; "),
#     label   = collapse_some(label),
#     type    = collapse_some(type),
#     n       = if (min(n) == max(n)) as.character(min(n)) else paste0(min(n), "-", max(n)),
#     summary = collapse_some(summary)
#   ) |>
#   mutate(
#     flag_type    = n_types > 1,
#     flag_label   = n_labels > 1,
#     flag_summary = n_shapes > 1 &
#       !grepl("Date|POSIX", type) &
#       (is.na(median_spread) | median_spread > 0.25),
#     issues = paste0(if_else(flag_type,    "type; ",    ""),
#                     if_else(flag_label,   "label; ",   ""),
#                     if_else(flag_summary, "summary; ", "")) |>
#       sub(pattern = "; $", replacement = "") |>
#       na_if("")
#   ) |>
#   arrange(is.na(issues), desc(n_files))
# 
# count(by_variable, issues, sort = TRUE)
# # Save it 
# 
# 'assets'