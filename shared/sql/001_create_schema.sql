-- ============================================================================
-- Schema: Market Research Lab
-- Migration: 001_create_schema.sql
-- Date: 2026-05-09
-- Description: Initial schema for OHLCV market data and derived volatility
--              metrics.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Table: market_data
-- Stores raw daily OHLCV data for any tradeable asset.
-- One row per (ticker, date).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS market_data (
    ticker          TEXT             NOT NULL,
    date            DATE             NOT NULL,
    open            DOUBLE PRECISION,
    high            DOUBLE PRECISION,
    low             DOUBLE PRECISION,
    close           DOUBLE PRECISION,
    adjusted_close  DOUBLE PRECISION,
    volume          DOUBLE PRECISION,
    source          TEXT             NOT NULL,
    fetched_at      TIMESTAMPTZ      NOT NULL DEFAULT now(),
    PRIMARY KEY (ticker, date)
);

-- Index for queries that filter by ticker only (e.g. "all SPY history")
CREATE INDEX IF NOT EXISTS idx_market_data_ticker
    ON market_data (ticker);


-- ----------------------------------------------------------------------------
-- Table: volatility_metrics
-- Stores derived volatility values, separated from raw market data so that
-- methodology can evolve without modifying the source records.
-- One row per (ticker, date, metric_name).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS volatility_metrics (
    ticker        TEXT             NOT NULL,
    date          DATE             NOT NULL,
    metric_name   TEXT             NOT NULL,
    value         DOUBLE PRECISION,
    computed_at   TIMESTAMPTZ      NOT NULL DEFAULT now(),
    PRIMARY KEY (ticker, date, metric_name)
);