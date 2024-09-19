# made by leo

# Title: pyReport
# Autor: leonardo.avalos.montes@continental-corporation.com
# Position: Test Maintenance Technician
# Location: Continental Periferico - Guadalajara
# Date: 06/09/2024

import os
import sys

def resource_path(relative_path):
    if hasattr(sys, 'MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
