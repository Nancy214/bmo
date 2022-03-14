# Package

version       = "0.1.0"
author        = "Dilawar Singh <dilawar@subcom.tech>"
description   = "BMO does all automation at SubCom"
license       = "AGPL-3.0-only"
backend       = "c"

srcDir        = "src"

installExt    = @["nim"]
bin           = @["bmo"]

# Dependencies
requires "nim >= 1.6"
requires "fusion"
requires "cligen"
