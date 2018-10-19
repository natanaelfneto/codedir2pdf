# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Released]
### 0.0.4 - 2018-03-16
#### Changed
- fixed pdf output location variable

#### Added
- basic functions: {
    - command for search pdf files and move then to destination
}

### 0.0.3 - 2018-03-16
#### Changed
- added try/except to pisa pdf line
- removed useless spcaes on code

## [Unreleased]
### 0.0.2 - 2018-03-16
#### Changed
- bug fixes on lexes
- bug fixes on output pdf folder
- bug fixes on pdf content for no supported languages
- added more undesired standard directories and file formats to .codeignore file

#### Added
- lexers and formatter for supported languages
- added standar output pdf for non supported languages
- added ignore procedure for not desired file formats
- recursively looping to move pdf files to output location

### 0.0.1 - 2018-03-16
#### Added
- project folder structure
- system supported: {
	- linux/centos7,
    - linux/ubuntu16
    - windows10/wsl
    - windows10/powershell5+
}
- basic functions: {
	- help message output
    - input folder for search files and convert to pdf at /pdf_output folder
    - version ouput
}

### 0.0.0 - 2018-03-15
#### Added
- project created