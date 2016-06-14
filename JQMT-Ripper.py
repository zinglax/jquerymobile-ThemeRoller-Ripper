import json, os, shutil
from pprint import pprint
import jinja2
from pprint import pprint as p

# GLOBALS
working_dir = working_directory = os.path.dirname(os.path.realpath(__file__))
json_dir = os.path.join(working_directory, "json")
colorgen_theme_dir = os.path.join(working_directory, "colorgen-Theme")
colorgen_json = os.path.join(json_dir, 'the_colorgen_theme.json')
temp_theme_dir = os.path.join(colorgen_theme_dir, '.temp')

def get_jinja_fields_and_colors(json_file=colorgen_json ):
    ''' Gets all fields from a theme json file for the A swatch'''
    # Reading in theme json data 
    with open(json_file) as data_file:    
        jqmt_rip = json.load(data_file)
        p(jqmt_rip) # Print out of json
        
        field_colors = {} # Dictionary of unique colors and names
        for k,v in jqmt_rip['themes'][0]['global'].iteritems():
            field_colors["global_" + k] = v        
        for k,v in jqmt_rip['themes'][0]['a'].iteritems():
            for k2,v2 in v.iteritems():
                field_colors['a_' + k + "_" + k2] = v2            
        return field_colors
    
    
def get_css_file_dict(directory=colorgen_theme_dir):
    ''' Gets a list of all the css files recursively in a directory'''
    css_file_dict = {}
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".css"):
                css_file_dict[f] = os.path.join(root,f)

    return css_file_dict


def color_replace(input_dir, output_dir=temp_theme_dir):
    ''' Replaces all instances of color with tag in a given direcory of .css files'''

    # Removes Old Output Directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Copy input to ouput
    shutil.copytree(input_dir, output_dir)

    # Gets css files in the output directory
    css_files = get_css_file_dict(output_dir)
    
    for tag,color in get_jinja_fields_and_colors().iteritems():
        print tag
        print color
        for k,v in css_files.iteritems():
            print k
            print v
            css_color_replace(color, "{{ "+ tag + " }}", v, k)
           
def css_color_replace(color, tag, css_filepath, css_filename):
    new_filename = "temp-" + css_filename        
    new_filename_path = css_filepath.replace(css_filename, new_filename)
    
    # Replace of color with tag
    with open(new_filename_path, mode='w') as fout:
        with open(css_filepath, mode="r") as fin:
            for line in fin:
                fout.write(line.replace(color, tag))
    
    # Rename of new Temp file back to the original
    shutil.copy(new_filename_path, css_filepath)
    
    # Cleans up Temp file
    os.remove(new_filename_path)    
       

if __name__ == "__main__":
    #p(get_jinja_fields_and_colors())
    #p(get_css_file_dict())
    
    color_replace(colorgen_theme_dir, temp_theme_dir)