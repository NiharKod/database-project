# Database Schema

## Relational Schema Format

This project uses 3 tables:

- `gpus`
- `benchmark_suites`
- `benchmark_results`

## `gpus`

- `gpu_id` `INTEGER` primary key
- `name` `STRING` not null
- `manufacturer` `STRING` not null
- `vram_gb` `INTEGER` not null
- `base_clock_mhz` `INTEGER` not null
- `boost_clock_mhz` `INTEGER` not null
- `release_year` `INTEGER` not null
- `msrp` `FLOAT` nullable

## `benchmark_suites`

- `suite_id` `INTEGER` primary key
- `name` `STRING` not null
- `version` `STRING` nullable
- `type` `STRING` not null

## `benchmark_results`

- `result_id` `INTEGER` primary key
- `gpu_id` `INTEGER` foreign key -> `gpus.gpu_id`
- `suite_id` `INTEGER` foreign key -> `benchmark_suites.suite_id`
- `score` `INTEGER` nullable
- `fps_avg` `FLOAT` nullable
- `fps_min` `FLOAT` nullable
- `temp_max_c` `FLOAT` nullable
- `power_draw_watts` `FLOAT` nullable
- `resolution` `STRING` not null
- `date_tested` `DATE` not null
- `notes` `TEXT` nullable

## Relationships

- One `GPU` can have many `BenchmarkResult` rows.
- One `BenchmarkSuite` can have many `BenchmarkResult` rows.
- Each `BenchmarkResult` belongs to one `GPU` and one `BenchmarkSuite`.

## Indexes

- `ix_gpus_manufacturer` on `gpus(manufacturer)`
  - Supports the Benchmark Report manufacturer dropdown and manufacturer filter.
- `ix_results_report_filters` on `benchmark_results(gpu_id, suite_id, resolution, date_tested)`
  - Supports the Benchmark Report filters for GPU, benchmark suite, resolution, and date range.
- `ix_results_date_tested` on `benchmark_results(date_tested)`
  - Supports the Benchmark Results page ordering by newest test date.
