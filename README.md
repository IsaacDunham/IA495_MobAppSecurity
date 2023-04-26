# IA495_MobAppSecurity
This is the GitHub for the IA 495 mobile app security testing automation project. Instructions are available upon request. Tests should be evaluated against the OWASP hacking playground app available here: https://github.com/OWASP/MASTG-Hacking-Playground/

The `tests` directory in this repo includes test code for custom-created searches that are not able to be found in the MASTG-Hacking-Playground app.

This project is intended to be used in conjunction with other tools as an extension, and does not replace or embed into these other tools.
Project is primarily designed to be compatible with and shares some architectural design (e.g., JSON schema, best_practices YAML design) with Ajin Abraham's _mobsfscan_, available at https://github.com/MobSF/mobsfscan.

## Usage Instructions
After cloning the repository, run `chmod +x` on `install.sh.` Then use `./install.sh` from the repo directory to install pre-requisite files and change Python script execution permissions. DO NOT use `sudo ./install.sh`. After the tool is installed, use `./kickstart.py` against a mobile app source code directory to perform the scan. 

## Platform Support
At this time, this configuration is only supported on fresh Ubuntu 18.04.6 LTS (Bionic Beaver) installations.