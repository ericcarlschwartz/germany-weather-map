# Gemini Project Instructions

This file contains foundational mandates for AI agents working on the `germany-weather-map` project. These instructions take absolute precedence over general defaults.

## Documentation Maintenance Mandate
- **Proactive Updates:** Whenever a new feature, CLI argument, or architectural change is implemented, you MUST update the `README.md` and any other relevant documentation immediately. Do not wait for a specific request from the user to do so.
- **Sync Validation:** Before concluding a task, verify that the `README.md` accurately reflects the current state of the application's features, installation steps, and usage examples.

## Engineering Standards
- **Testing Requirements:** Every code change must be accompanied by corresponding unit and/or integration tests.
- **Coverage Goal:** Maintain a minimum of 90% code coverage. Run `coverage report` after changes to ensure this threshold is met.
- **Logging over Printing:** Always use the standard `logging` module for status updates and error reporting. Reserved `print` for actual map output intended for the user.
- **Module Execution:** The application is designed to be run as a module (`python3 -m germany_weather_map.main`). Ensure all package-relative imports are maintained.

## Technical Context
- **API:** Uses Open-Meteo DWD ICON API.
- **Data Dir:** Project root contains `germany.json`, which is required for boundary calculations.
- **Dependencies:** Managed via `requirements.txt` and `pyproject.toml`.
