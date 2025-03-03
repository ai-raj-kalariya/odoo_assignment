# Changelog

## [18.0.0.0.0] - 2025-04-03

### Added
- Added comprehensive docstrings at model and function levels with return types and parameters
- changes in action_conform method in sale_order model
- Added method for schedule action

### Changed
- Optimized sale_order.py code for better performance
- Field and button names 
- Improved method handling for multi-record operations instead of self

### Technical
- Added type param and return value in function doc string
- Enhanced model-level doc string
- Version management in manifest file updated to 18.0.1.2.2

### Fixed
- Resolved single-record method issues for multi-record scenarios
- Dependency error from inventory module

### Code Quality
- Added comprehensive docstrings following Python standards
- Implemented proper model inheritance patterns
- Optimized code structure for better maintainability
