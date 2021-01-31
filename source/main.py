#!/usr/bin/env python
import os
if (os.path.dirname(__file__) != ''):
    os.chdir(os.path.dirname(__file__)) # change working directory to `/source`

import view
view.main() # start the program
