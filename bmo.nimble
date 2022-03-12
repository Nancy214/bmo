# Package

version       = "0.1.0"
author        = "Dilawar Singh"
description   = "BMO does all automation at SubCom"
license       = "AGPL-3.0-only"

srcDir        = "src"

installExt    = @["nim"]
bin           = @["bmo"]

# Dependencies
requires "nim >= 1.4"
requires "fusion"
requires "itertools"

backend = "cpp"
