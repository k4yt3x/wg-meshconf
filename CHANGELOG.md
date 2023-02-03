# Changelog

## 2.5.1 (February 2, 2023)

- Update the project to use PEP 518 and PEP 621

## 2.2.0 (January 26, 2021)

- Implemented private/public key generation using native Python code
  - Consequentially, this program no longer depends on an external `wg` binary

## 2.1.0 (January 13, 2021)

- Reorganized code and made available on PyPI

## 2.0.0 (November 15, 2020)

Version 2.0.0 is a complete rewrite of this software. The whole software is completely re-designed from scratch. Previous versions had a lot of problems:

- Non-modular design
- Not scalable
- Command line arguments are not compliant with Unix conventions
- The interactive terminal requires the user to respond to all questions
- Profiles have to be saved and loaded manually
- The `readline` package does not work on Windows
- I was a worse coder in general two years ago

These problems are all addressed in version 2.0.0. Below are some other noteworthy changes.

- Handed argument parsing to Python's `argparse` library
- Added tabled peer information output
- Added more supported attributes

## 1.3.0 (August 10, 2019)

- Complete rebuild of project code structure
- Changed Peer object read and write method
  - Now using `peer.__dict__` instead of receiving values in object constructor
- Added new wg-quick fields
  - AllowedIPs
  - Table
  - PreUp
  - PostUp
  - PreDown
  - PostDown
- Peer configuration now separated into basic and advanced configurations

## 1.2.0 (May 16, 2019)

- You can now set Aliases and Descriptions for peers.
- Profiles can now be saved and loaded in JSON format.

## 1.1.7 (Feburary 20, 2019)

- Public address can now be either FQDN or IP address, as requested by @KipourosV
