# Change Log
All notable changes will be documented in this file.

##2021-05-16
The Branch light will serve as a lightweight version for the original bot. Only functionality for the Telegram Bot. 
Changes:
- restructered into classes
- added randomizer to time
- fixed bug with Johnson and Johnson Vaccine (exception thrown because no 2nd date exists)

## 2021-04-04
### Added
- Ability to search for Vermittlungscodes base on a given age. Currently, quite often you can only get a Vermittlungscode if you're older than 60, because the Impfzentrum only has AstraZeneca and no other vaccine.

## 2021-03-29
### Fixed
- Avoid exception when Wartungsarbeiten are happening
## 2021-03-28
### Added
- Ability to send Telegram notifications. Up to now, no different recipients possible for each dataset, only one recipient for everything
- Introduced CHANGELOG
- Play alarm sound when appointment is found
### Changed
- Wait 10s between each dataset in order to avoid getting lots of `HTTP 429: Too Many Requests`
- Extend logging a bit to include Vermittlungscodes, timestamps and URLs in the log
### Fixed
- JSON import UTF-8 character handling


## 2021-03-26
### Added
- Checker is now able to notify you when you can request a Vermittlungscode
- Ability to compare any dataset to a given `min_date` to find only appointments after a given date