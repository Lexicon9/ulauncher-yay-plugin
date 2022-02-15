# Arch Package Search for ULauncher
## Description
This extension enables searching for and installing packages for Arch Linux using the AUR helper of your choice (yay by default). Typing 'pkg (package name)' will show installation options. Selecting one of the options will copy the command to install it to the clipboard. 

This is a fork of a probably perfectly fine extension by Adam Tillou, but the requirement of aurman in the original is entirely arbitrary, and as noted in the aurman README https://github.com/polygamma/aurman#stopped-development-for-public-use yay is suggested over aurman. This fork adds settings to decide the helper you want to use.
## Requirements
You must have an AUR helper that uses pacman style -S and -Ss flags installed to enable searching for packages from the AUR. 
## Installation
Open ULauncher, and click the settings cog to open the settings menu. Navigate to the extensions tab, click add extension, and then paste the github link (below) into the field.  
https://github.com/holozene/ulauncher-aur-plugin
