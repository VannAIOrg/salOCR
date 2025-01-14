# Changelog

# [released on 14th Jan 2025]

# Added
- **Parallel Processing:** Introduced parallel processing in `main_parallel.py` using the `joblib` library.
  - Added `from joblib import Parallel, delayed` to facilitate parallel execution.
  - Replaced the sequential PDF processing loop with parallel execution using `Parallel` and `delayed`.

# Modified
- **`process_pdf` Function:**
  - Modified the function call within the `main` method to use `Parallel` for processing multiple PDFs concurrently.
  
- **`main` Function:**
  - Updated the processing of PDF files to handle them in parallel, reducing the overall execution time for large datasets.

# Removed
- Progress bar (`tqdm`) was excluded from `main_parallel.py` since it does not align with parallelized operations.
