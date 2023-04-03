# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Fixes
  * Expect that the "resultCode" may be missing in the response

### Changed
  * `PaymentInfo` now encapsulates the whole response including `resultCode` and `resultMessage`

### Added
  * `PaymentInfo.raise_for_result_code` method. Works similar as `requests.raise_for_status`
  * `PaymentInfo.ok` property


## [0.2.0] - 2023-04-02

### Added
  * `/payment/close`
  * Validation for the Cart size
  * Enum for payment statuses
  * Support for different RSA key access strategies


## [0.1.0] - 2023-04-02

### Added
  * Basic working version
