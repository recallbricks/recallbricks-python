# Changelog

All notable changes to the RecallBricks Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.1] - 2024-12-14

### Fixed
- Fixed `recall()` method using incorrect HTTP method (GET instead of POST)
- `recall()` now properly calls POST /api/v1/memories/recall endpoint with JSON body
- Updated `organized` parameter to send boolean `true` instead of string `"true"`

## [1.5.0] - 2024-12-13

### Added
- Initial release with full API support
- Memory operations: save, learn, recall, search, get, delete, update
- Service token authentication for server-to-server access
- Relationship methods: get_relationships, get_graph_context
- Predictive features: predict_memories, suggest_memories
- Analytics: get_learning_metrics, get_patterns, search_weighted
- Automatic retry with exponential backoff
- Input sanitization and validation
