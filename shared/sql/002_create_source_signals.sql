-- ============================================================================
-- Schema: Market Research Lab
-- Migration: 002_create_source_signals.sql
-- Date: 2026-05-11
-- Description: Table for storing alternative data source signals. Any source
--              that is not OHLCV-structured (Treasury yields, prediction
--              market probabilities, sentiment scores, etc.) lands here in a
--              standardized long format.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Table: source_signals
-- Standardized long-format storage for alternative data signals.
-- One row per (source_name, signal_name, date).
--
-- Design rationale:
--   - Long format (not wide) means new sources/signals never require schema
--     changes -- they are just new rows with new signal_name values.
--   - The metadata JSONB column stores source-specific context (raw values,
--     additional dimensions, provenance) without polluting the core columns.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS source_signals (
    source_name   TEXT             NOT NULL,
    signal_name   TEXT             NOT NULL,
    date          DATE             NOT NULL,
    value         DOUBLE PRECISION,
    metadata      JSONB,
    fetched_at    TIMESTAMPTZ      NOT NULL DEFAULT now(),
    PRIMARY KEY (source_name, signal_name, date)
);

-- Index for queries that filter by source and signal across all dates
CREATE INDEX IF NOT EXISTS idx_source_signals_lookup
    ON source_signals (source_name, signal_name);