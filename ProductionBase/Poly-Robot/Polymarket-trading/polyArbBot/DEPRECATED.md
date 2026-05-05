# DEPRECATED

The vendored `polyApi/` and `py_clob_client/` directories in this folder are
**deprecated and scheduled for removal**.

## Reason
ADR-002 Phase 2 introduces a typed `DataProvider` protocol in
`src/poly_robot/data_provider.py` that wraps the existing
`LivePolymarketIngestionAdapter` and `HistoricalIngestionAdapter`.
Market-fetcher logic from `Polymarket-trading/main.py` is being absorbed
into `PolymarketLiveProvider`.

## Migration path
- Use `from poly_robot.data_provider import PolymarketHistoricalProvider` for replay fixtures.
- Use `from poly_robot.data_provider import PolymarketLiveProvider` for live market data.
- Do not add new code that imports from `polyArbBot/` or `py_clob_client/`.

## Timeline
- Sprint W23: DataProvider abstraction created, deprecation notice added.
- Sprint W24+: vendored directories removed once all references are migrated.
