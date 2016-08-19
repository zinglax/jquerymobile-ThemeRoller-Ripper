import json, os, shutil
import jinja2
from pprint import pprint as pretty

# GLOBALS
working_dir = working_directory = os.path.dirname(os.path.realpath(__file__))
json_dir = os.path.join(working_directory, "json")
colorgen_theme_dir = os.path.join(working_directory, "colorgen-Theme")
colorgen_json = os.path.join(json_dir, 'the_colorgen_theme.json')
temp_theme_dir = os.path.join(colorgen_theme_dir, '.temp')

theme_name = "colorgentwo-Theme"
colorgentwo_theme_dir = os.path.join(working_directory, theme_name)
colorgentwo_json = os.path.join(json_dir, 'colorgen2.json')
temp_themetwo_dir = os.path.join(colorgentwo_theme_dir, '.temp')


class Jinjenv(jinja2.Environment):
    ''' Jinja2 Environment Override '''
    def __init__(self, **kwargs):
        # self.jinja2.Environment.__init__(self, **kwargs)

        # Current Working Directory of Flask Generator
        self.working_directory = os.path.dirname(os.path.realpath(__file__))

        # Templates directory
        self.templates_directory = "/home/dylan/Desktop/GITHUBS/jquerymobile-ThemeRoller-Ripper/colorgentwo-Theme/.temp/jquery-mobile-theme-134122-0/themes/"



        # Jinja
        self.templateLoader = jinja2.FileSystemLoader(searchpath=self.templates_directory)
        self.templateEnv = jinja2.Environment( loader=self.templateLoader )


def get_jinja_fields_and_colors(json_file=colorgen_json ):
    ''' Gets all fields from a theme json file for the A swatch'''
    # Reading in theme json data
    with open(json_file) as data_file:
        jqmt_rip = json.load(data_file)
        pretty(jqmt_rip) # Print out of json

        field_colors = {} # Dictionary of unique colors and names
        for k,v in jqmt_rip['themes'][0]['global'].items():
            field_colors["global_" + k] = v
        for k,v in jqmt_rip['themes'][0]['a'].items():
            for k2,v2 in v.items():
                field_colors['a_' + k + "_" + k2] = v2
        return field_colors


def get_css_file_dict(directory=colorgen_theme_dir):
    ''' Gets a list of all the css files recursively in a directory'''
    css_file_dict = {}
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".css"):
                css_file_dict[f] = root

    return css_file_dict


def color_replace(input_dir, output_dir=temp_theme_dir):
    ''' Replaces all instances of color with tag in a given direcory of .css files'''

    # Removes Old Output Directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Copy input to ouput
    shutil.copytree(input_dir, output_dir)

    existing_css_files = get_css_file_dict(output_dir)

    # Gets css files in the output directory
    css_files = get_css_file_dict(output_dir)

    # # Removes temp Output Directory so a new one can be generated
    # if os.path.exists(output_dir):
        # shutil.rmtree(output_dir)

    print(css_files)
    print(existing_css_files) # , os.path.join(existing_css_files[k], k)

    for tag,color in get_jinja_fields_and_colors(json_file=colorgentwo_json).items():
        #pretty((tag, color))
        for k,v in css_files.items():
            pretty((k,v))
            css_color_replace(color, "{{ " + tag + " }}", v, k)
            # css_color_replace_jinja(color, "{{ "+ tag + " }}", v, k)


def css_color_replace_jinja(color, tag, css_filepath, css_filename):

    print(color)
    print (tag)


    # TEMP FILE
    new_filename = "temp-" + css_filename
    new_filename_path = css_filepath.replace(css_filename, new_filename)

    # CSS THEME TEMPLATES
    templates_directory = os.path.join(working_directory, "templates")

    templateLoader = jinja2.FileSystemLoader(searchpath=templates_directory)
    # Jinja Environment (can be used for "Custom Tests" for checking
    # template variables)
    templateEnv = Jinjenv(loader=templateLoader,
                          variable_start_string=color[:3],
                          variable_end_string=color[4:],
                          block_end_string="~*~",
                          block_start_string="~*~",
                          comment_start_string="~~~",
                          comment_end_string= "~~~"
                          )

    # FILTERS (Add them here)
    # templateEnv.filters['template_os_path_join'] = template_os_path_join

    with open(new_filename_path, "wb") as fh:

        renderedoutput = templateEnv.get_template("colorgentwo.css.jinja").render(
            {color[3]:tag})
        fh.write(renderedoutput)
        pretty(renderedoutput)


def css_color_replace(color, tag, css_filepath, css_filename):
    new_filename = "temp-" + css_filename
    new_filename_path = css_filepath.replace(css_filename, new_filename)
    #print(new_filename_path)
    # Replace of color with tag
    #os.makedirs(css_filepath, exist_ok=True)
    #print(css_filename, css_filepath)
    new_file = os.path.join(new_filename_path, new_filename)
    existing_file = os.path.join(css_filepath, css_filename)
    with open(new_file, mode='w+') as fout:
        with open(existing_file, mode="r") as fin:
            for line in fin:
                if color in line:
                    # print(line[:-1], color, tag)
                    print(line.replace(color, tag))
                fout.write(line.replace(color, tag))

    # Rename of new Temp file back to the original
    shutil.copy(new_file, existing_file)

    # Cleans up Temp file
    os.remove(new_file)


if __name__ == "__main__":
    #pretty(get_jinja_fields_and_colors())
    #pretty(get_css_file_dict())

    # color_replace(colorgentwo_theme_dir, temp_themetwo_dir)

    #css_color_replace_jinja("#c1272d", "a_header_footer_bar_TS", css_filepath, css_filename)

    env = Jinjenv()
    output = env.templateEnv.get_template("colorgentwo.css").render(
        get_jinja_fields_and_colors(json_file=colorgentwo_json))
    print(output)