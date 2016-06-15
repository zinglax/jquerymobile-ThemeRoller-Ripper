# Ripper - ThemeGenerator
import os, jinja2, subprocess, shutil

class ThemeGenerator:

    def __init__(self, **kwargs):
        # Current Working Directory of Flask Generator
        self.working_directory = os.path.dirname(os.path.realpath(__file__))    
        
        self.themes_directory = os.path.join(self.working_directory, "themes")


