from networkx import edges
from datastructures.graph.graph import Graph
from datastructures.graph.node import Node
from datastructures.graph.edge import Edge
from datastructures.cycles.circle_manager import CircleManager
from datastructures.cycles.cycle import Cycle

from custom_io.filehelper import FileHelper
from custom_io.visualizer.visualizer import Visualizer
from custom_io.visualizer.fancy_visualizer import FancyVisualizer

from logic.graphbuilder import GraphBuilder

import os
import re


class Parser:
    def __init__(self) -> None:
        self.running : bool = True
        self.graphs: dict[str, Graph] = {}
        self.filehelper : FileHelper = FileHelper()
        return None
    
    def run(self) -> None:
        intro_statement = '' \
        '-------------------------------------------\n' \
        'Starting Wiki-Graph command-line-interface.\n' \
        'Please start by using \'help\' to familiarize yourself with the available commands.\n' \
        'made by Fae Körper.'

        print(intro_statement)

        while(self.running):
            prompt = input('-------------------------------------------\n')
            print('')
            if not prompt:
                self.__default(None)
                continue
            fragments = prompt.split(" ")
            command = fragments[0]
            options = fragments[1:] if len(fragments) > 1 else None
            
            match command:
                case "help":
                    self.__help()
                    
                case "view":
                    self.__view(options)

                case "read":
                    self.__read(options)

                case "save":
                    self.__save(options)

                case "build":
                    self.__build(options)

                case "cycles":
                    self.__cycles(options)

                case "traverse":
                    self.__traverse(options)
                    

                case "visualize":
                    self.__visualize(options)

                case "exit":
                    self.running = False
            
                case _:
                    self.__default(command)
        saving_statement = '' \
        '----------------------------------------\n' \
        'Saving all active graphs before quitting'

        print(saving_statement)

        amount = len(self.graphs)
        saved = 0

        for name, graph in self.graphs.items():
            file_name = name + ".txt"
            self.filehelper.write_graph_to_file(graph, file_name, False)
            saved += 1
            print('Successfully saved graph' + name + f'. Done {(float(saved)/amount):.2%}')

        exit_statement = '' \
        '---------------------\n' \
        'Successfully exited.'

        print(exit_statement)
                    
    def __parse_options(self, user_options:list[str]|None, valid_options:dict[str, int]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        valid_user_options = {}
        invalid_user_options = {}

        if user_options == None or len(user_options) == 0:
            return (valid_user_options, invalid_user_options)
        
        trimmed_user_options = [user_option.replace(" ", "") for user_option in user_options]
        filtered_user_options = [user_option for user_option in trimmed_user_options if (len(user_option) > 0 )]

        options_positions = [idx for idx, user_option in enumerate(filtered_user_options) if user_option[0] == "-"]
        options_positions.append(len(filtered_user_options))

        for idx in range(len(options_positions) - 1):
            
            current_pos = options_positions[idx]
            next_pos = options_positions[idx + 1]

            chunk = filtered_user_options[current_pos:next_pos]

            option = chunk.pop(0)
            arguments = chunk
            
            if option not in valid_options.keys():
                invalid_user_options[option] = arguments
                continue
                
            if len(arguments) != valid_options[option]:
                invalid_user_options[option] = arguments
                continue

            valid_user_options[option] = arguments

        return (valid_user_options, invalid_user_options)
        
    def __help(self) -> None:
        help_statement = '' \
        'The is a command line interface created by Fae Körper for FMI-BI0058.\n' \
        'The project aims to collect and visualize information about wikipedia articles.\n' \
        'Each Command has an \'-h\' option to further specify use and available options.\n' \
        'Command list:\n' \
        'help: Displays a help message to explain use (The current command).\n' \
        'view: List the currently active graphs.\n' \
        'read: Read a saved graph file into memory to use it.\n' \
        'save: Save an active graph into a file.\n' \
        'build: Create a new active graph.\n' \
        'visualize: Create a visualization of an active graph\n' \
        'traverse: Get further information about an active graph.\n' \
        'cycles: Detect circular links in an active graph.\n' \
        'exit: Exit this programm.'

        print(help_statement)
        return None
            
    def __default(self, command:str | None) -> None:
        if command is None:
            default_statement = '' \
            'Please enter any command. Refer to the \"help\" command for a list of available commands.'
        else:
            default_statement = '' \
            f'Command \'{command}\' is not recognized,\n' \
            'please refer to the \"help\" command for a list of available commands.'

        print(default_statement)
        return None

    def __view(self, options:list[str]|None) -> None:
        available_options = {"-h" : 0, "-v" : 0}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)

        if not self.__warn_options(invalid_user_options):
            return None
        
        if "-h" in valid_user_options.keys():
            help_statement = '' \
            'This command is used to view all active graphs that can be used in other commands.\n' \
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \
            ' -v : verbose output to get further information about the active graphs'

            print(help_statement)
            return None

        verbose_option = "-v" in valid_user_options.keys()
        
        graph_amount = len(self.graphs)

        if graph_amount == 0:
            no_graphs_statement = '' \
            'No active graphs exist. Please build graphs or read them from file to use this command.'

            print(no_graphs_statement)
            return None

        intro_statement = '' \
        f'Listing all {graph_amount} active graphs:'

        print(intro_statement)

        for (name, graph) in self.graphs.items():
            if verbose_option:
                graph_line = f'- {name}, Density: {graph.get_density():.2f}'

            else:
                graph_line = f'- {name}'
            
            print(graph_line)
            
        return None
    
    def __read(self, options:list[str]|None) -> None:
        available_options = {"-h" : 0, "-v" : 0, "-f" : 1}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)

        if "-h" in valid_user_options.keys():
            help_statement = ''\
            'This command is used to read graphs from textfiles created by this CLI for further use.\n' \
            'Files are only found in the \"txtfiles\" folder inside the project folder\n\n' \
            'Mandatory Options:\n' \
            ' -f [filename] : specify the filename to read from, only selecting from the txtfiles directory\n\n' \
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \
            ' -v : verbose logging to get further information about the graph reading'

            print(help_statement)
            return None

        file_name_given = "-f" in valid_user_options.keys()
        if not file_name_given:
            failure_statement = '' \
            'Cannot read graph, cause of missing valid file name to read graph from.\n' \
            'Please use \"-f [filename]\" to select a file.\n' \
            'Files can only be found in the txtfiles folder in this project.\n' \
            'For further help, use \"-h\"'

            print(failure_statement)
            return None

        if not self.__warn_options(invalid_user_options):
            return None
        
        verbose = "-v" in valid_user_options.keys()

        filename_option = valid_user_options.get("-f")
        assert filename_option
        file_name = filename_option[0]

        read_graph = self.filehelper.read_graph_from_file(file_name, verbose) 
        
        if read_graph == None:
            failure_statement = '' \
            'Could not read graph. This can have multiple reasons:\n' \
            'The file not existing, the file not being in a readable text format or the file not containing a valid graph.\n' \
            'Please refer to above errors, use \"-v\" to get a hint in the verbose output or check the file itself.'

            print(failure_statement)
            return None

        root_name = read_graph.get_root()
        graph_size = read_graph.get_node_count()
        
        key = f"{root_name}-{graph_size}"
        self.graphs[key] = read_graph

        success_statement = '' \
        'Successfully read graph and added it to the available graphs.'

        print(success_statement)
        return None
    
    def __save(self, options:list[str]|None) -> None:
        available_options = {"-h" : 0, "-v" : 0, "-g" : 1, "-n" : 1}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)

        if "-h" in valid_user_options.keys():
            help_statement = ''\
            'This command is used to save an active graph into a text file.\n' \
            'Mandatory Options:\n' \
            ' -g [graphname] : The name of the graph that you want to save\n' \
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \
            ' -v : verbose logging to get further information about the graph saving\n' \
            ' -n [filename] : a custom file name for the graph textfile. Default is \"[rootname-size]\"'

            print(help_statement)
            return None
        
        graph = self.__check_graph_option(valid_user_options)
        if not graph:
            return None
        
        root_name = graph.get_root()

        if not self.__warn_options(invalid_user_options):
            return None

        verbose = "-v" in valid_user_options
        custom_file_name = "-n" in valid_user_options

        if custom_file_name:
            wrapped_file_name = valid_user_options.get("-n")
            assert wrapped_file_name
            file_name = wrapped_file_name[0]
        else:
            file_name = f"{root_name}-{len(graph.get_nodes())}.txt"
        
        try:
            self.filehelper.write_graph_to_file(graph, file_name, verbose)

            success_statement = '' \
            'Done writing to file to [projectfolder]\\txtfiles\\'
        
            if verbose:
                success_statement += f'\nLocated at {os.getcwd() + '\\txtfiles\\'+ file_name}'
        
            print(success_statement)

        except Exception as e:
            failure_statement = '' \
            'Saving graph to file failed.\n' \
            'Please refer to the error message for further information\n'
            
            print(failure_statement + str(e))
            return None

        return None
    
    def __build(self, options:list[str]|None) -> None:
        available_options = {"-h" : 0, "-v" : 0, "-k" : 1, "-d" : 1, "-r" : 1, "-q" : 1}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)

        if "-h" in valid_user_options.keys():
            help_statement = '' \
            'This command is used to build an active graph from the name of an article.\n' \
            'Mandatory Options:\n' \
            ' -r [articlename] : The name of the wikipedia article that you want to use as a root for the graph\n' \
            ' -q [n|p] : The type of queue to select the next article (n) normal queue or (p) priority queue\n' \
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \
            ' -v : verbose logging to get further information about the graph saving\n' \
            ' -k [num] : the amount of articles to be included. (Default is 500)\n' \
            ' -d [num] : the maximal depth or distance to the original article that should be included. (Default is 10)'

            print(help_statement)
            return None
        
        root_given = "-r" in valid_user_options.keys()
        if not root_given:
            failure_statement = '' \
            'No root for graph building given. Can\'t start building graph without a starting point.\n' \
            'Please give a root by using \'-r [root] \'\n' \
            'Aborting graph building.'

            print(failure_statement)
            return None

        graph_root_option = valid_user_options.get("-r")
        assert graph_root_option
        graph_root = graph_root_option[0]

        graph_size = self.__get_graph_size(valid_user_options)
        if graph_size == -1:
            return None
        
        graph_depth = self.__get_graph_depth(valid_user_options)
        if graph_depth == -1:
            return None
        
        queue_type_given = "-q" in valid_user_options.keys()
        if not queue_type_given:
            failure_statement = '' \
            'No queue type given. Can\'t start building graph without a queue type.\n' \
            'Please specify a queue type by using \"-q [n|p]\" to either use a (n) normal queue or a (p) priority queue\n' \
            'Aborting graph building.'

            print(failure_statement)
            return None
        
        queue_type_wrapped = valid_user_options.get("-q")
        assert queue_type_wrapped
        queue_type = queue_type_wrapped[0]

        if queue_type not in ["n", "p"]:
            failure_statement = '' \
            f'Given queue type \"{queue_type}\" is not in the supported types:\n' \
            '\"n\": normal queue\n' \
            '\"p\": priority queue\n' \
            'Aborting graphbuilding'

            print(failure_statement)
            return None

        if not self.__warn_options(invalid_user_options):
            return None
        
        verbose = "-v" in valid_user_options.keys()

        if verbose:
            arguments_statement = '' \
            'Starting graph building:\n' \
            f'Root: {graph_root}\n' \
            f'Max graph size: {graph_size}\n' \
            f'Max graph depth: {graph_depth}\n' \
            'Queue type: '
            
            queue_type_name = 'normal' if queue_type == "n" else 'priority'
            arguments_statement += queue_type_name + ' queue\n'

            print(arguments_statement)

        builder = GraphBuilder(graph_size, graph_depth)
        
        graph = builder.build_graph_from_article(graph_root, queue_type, verbose)

        if graph == None:
            building_failed_statement = '' \
            'Graph building failed. Please see above error messages for more information'

            print(building_failed_statement)
            return None
        
        graph_name = f"{graph_root}-{graph_size}"
        self.graphs[graph_name] = graph

        success_statement = '' \
        'Successfully added graph which is now available for other commands using the name:\n' \
        f'{graph_name}\n'

        print(success_statement)
        return None
    
    def __get_graph_size(self, valid_user_options:dict[str, list[str]]) -> int:
        custom_size_used = "-k" in valid_user_options.keys()
        if custom_size_used:
            user_size_option = valid_user_options.get("-k")
            assert user_size_option
            user_size = user_size_option[0]

            valid_custom_size = user_size.isdigit() and user_size != "0"

            if valid_custom_size:
                graph_size = int(user_size)
            else:
                fallback_statement = '' \
                f'Given custom size \"{user_size}\" is not a positive integer bigger than 0. Aborting graph building.'

                print(fallback_statement)
                graph_size = -1
        else:
            graph_size = 500
        
        return graph_size

    def __get_graph_depth(self, valid_user_options:dict[str, list[str]]) -> int:
        custom_depth_used = "-d" in valid_user_options.keys()
        if custom_depth_used:
            user_depth_option = valid_user_options.get("-d")
            assert user_depth_option
            user_depth = user_depth_option[0]
            valid_custom_depth = user_depth.isdigit() and user_depth != "0"
            
            if valid_custom_depth:
                graph_depth = int(user_depth)
            else:
                fallback_statement = '' \
                f'Given custom depth \"{user_depth}\" is not a positive integer bigger than 0. Aborting graph building.'

                print(fallback_statement)
                graph_depth = -1
        else:
            graph_depth = 10

        return graph_depth
    
    def __warn_options(self, invalid_user_options:dict[str, list[str]]) -> bool:
        
        if not invalid_user_options:
            return True

        warning_statement = '' \
        'Found invalid options:'

        print(warning_statement)

        for option, arguments in invalid_user_options.items():
            option_line = f"\"{option}\""

            if arguments:
                option_line += " ".join(arguments)

            print(option_line)

        user_answer = input("Please select if you still want to continue with the command (Y/N):")

        if user_answer.upper() != "Y":
            print("Aborting command execution")
            return False
        
        else:
            print("Continuing command execution")
            return True
    
    def __visualize(self, options:list[str]|None) -> None:
        available_options = {"-h" : 0, "-v" : 0, "-g" : 1, "-t" : 1}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)

        if "-h" in valid_user_options.keys():
            help_statement = '' \
            'This command is used to create a visualization of an active graphs either interactive or as an image\n' \
            'Mandatory Options:\n' \
            ' -g [graphname] : the name of an active graph that should be visualized\n' \
            ' -t [s|d] : the type of visualization (s) static or (d) dynamic. Warning: dynamic for larger graphs may take very long.\n' \
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \
            ' -v : verbose output to get further information about the active graphs'

            print(help_statement)
            return None
        
        if "-t" not in valid_user_options.keys():
            failure_statement = '' \
            'No visualization type given. Can\'t continue\n' \
            'Please supply a type of visualization, either (s) static or (d) dynmaic\n' \
            'Using: \"-t [s|d]\"'

            print(failure_statement)
            return None

        if not self.__warn_options(invalid_user_options):
            return None         

        graph = self.__check_graph_option(valid_user_options)
        if not graph:
            return None

        wrapped_visualization_type = valid_user_options.get("-t")
        assert wrapped_visualization_type
        visualization_type = wrapped_visualization_type[0]

        if visualization_type not in ["s", "d"]:
            failure_statement = '' \
            f'Provided visualizdation type \"{visualization_type}\" is not [s|d]\n' \
            'Can\'t continue visualization'

            print(failure_statement)
            return None
        
        assert visualization_type in ["s", "d"]

        verbose = "-v" in valid_user_options.keys()

        match visualization_type:
            case "s":
                self.__static_visualization(graph, verbose)

            case "d":
                self.__dynamic_visualization(graph, verbose)

        return None
    
    def __static_visualization(self, graph:Graph, verbose:bool) -> None:
        visualizer = Visualizer()
        image_size, dpi = self.__get_static_vis_options()

        disected_file_position = os.path.realpath(__file__).split("\\")
        project_folder = "\\".join(disected_file_position[:len(disected_file_position) - 4])
        images_folder_path = project_folder + "\\images\\"

        visualizer.save_image_from_graph(graph, images_folder_path, image_size, dpi, verbose)

        return None
    
    def __get_static_vis_options(self) -> tuple[tuple[int, int], int]:
        explanation_statement = '' \
        'Please enter either a triplet of image width, image height and resolution (dpi) or accept default by skipping\n' \
        'Default: 150,90,100\n' \
        'Warning: image file size scales multiplicative with both width values and the resolution'

        print(explanation_statement)

        user_response = input()

        default_img_size = (150, 90)
        default_dpi = 100


        if len(user_response.replace(" ", "")) == 0:
            return default_img_size, default_dpi

        user_values = user_response.split(",")

        if len(user_values) != 3:
            warning_statement = '' \
            f'Got user input: \"{user_response}\"' \
            'But couldn\'t seperate into three numbers\n' \
            'Using default values'

            print(warning_statement)
            return default_img_size, default_dpi
        
        values = []
        
        for user_value in user_values:
            if not user_value.isnumeric():
                warning_statement = '' \
                f'Got user input: \"{user_response}\"' \
                f'And part \"{user_value}\" can not be interpreted as a number\n' \
                'Using default values'

                print(warning_statement)
                return default_img_size, default_dpi
            
            value = int(user_value)

            if value <= 0 or value > 100000:
                warning_statement = '' \
                'Values are only permitted between 0 and 100000\n' \
                f'Provided value: {value} falls outside that\n' \
                'Using default values'

                print(warning_statement)
                return default_img_size, default_dpi
            values.append(value)

        img_size = values[0], values[1]
        dpi = values[2]

        return img_size, dpi

    def __dynamic_visualization(self, graph:Graph, verbose:bool) -> None:

        settings = self.__get_dynamic_vis_options()

        dyn_visualizer = FancyVisualizer(settings)

        dyn_visualizer.generate_browser_graph(graph, verbose)
        
        return None
    
    def __get_dynamic_vis_options(self) -> dict[str, str]:
        explanation_statement = '' \
        'Please select settings for the creation of the interactive graph:' 

        print(explanation_statement)

        settings = {}
        
        user_width, user_height = self.__get_dyn_vis_size()
        settings["width"] = user_width
        settings["height"] = user_height

        user_bg_color = self.__get_dyn_vis_bgcolor()
        settings["bgcolor"] = user_bg_color

        user_node_color = self.__get_dyn_vis_nodecolor()
        settings["nodecolor"] = user_node_color

        return settings

    def __get_dyn_vis_nodecolor(self) -> str:
        nodecoloring_statement = '' \
        'Please enter a color hexcode for the nodes or skip to accept the default\n' \
        'Default is: 97c2fc (light blue)\n'

        user_node_color = input(nodecoloring_statement)

        if len(user_node_color.replace(" ", "")) == 0:
            return "#97c2fc"
        
        valid_hex = "^(?:[0-9a-fA-F]{2}){3}$"
        match = re.search(valid_hex, user_node_color
                          )
        if not match:
            warning_statement = '' \
            f'Given color: \"{user_node_color}\" is not a valid hex color code.\n' \
            'Using default'
            print(warning_statement)
            return "#97c2fc"

        report_statement = '' \
        'Recieved node color:\n' \
        f'#{user_node_color}'
        print(report_statement)
        return f"#{user_node_color}"

    def __get_dyn_vis_bgcolor(self) -> str:
        bgcoloring_statement = '' \
        'Please enter a color hexcode for the background or skip to accept the default\n' \
        'Default is: 00052E (dark blue)\n'

        user_bg_color = input(bgcoloring_statement)

        if len(user_bg_color.replace(" ", "")) == 0:
            return "#00052E"
        
        valid_hex = "^(?:[0-9a-fA-F]{2}){3}$"
        match = re.search(valid_hex, user_bg_color)

        if not match:
            warning_statement = '' \
            f'Given color: \"{user_bg_color}\" is not a valid hex color code.\n' \
            'Using default'

            print(warning_statement)
            return "#00052E"
            
        report_statement = '' \
        'Recieved background color:\n' \
        f'#{user_bg_color}'

        print(report_statement)
        return f"#{user_bg_color}"

    def __get_dyn_vis_size(self) -> tuple[str, str]:
        sizing_statment = '' \
        'Please enter a tuple of pixel amount to specify the width and heigth or skip to accept default\n' \
        'Valid values are integers between 100 and 10.000\n' \
        'Default is: 1500,1500\n'

        user_size = input(sizing_statment)

        if len(user_size.replace(" ", "")) == 0:
            return "1500px", "1500px"

        split = user_size.split(",")
        
        if len(split) != 2:
            warning_statement = '' \
            f'Given size {user_size} is not in the format: \"width,height\".\n' \
            'Using default size'

            print(warning_statement)
            return "1500px", "1500px"
        
        user_width = split[0]
        user_heigth = split[1]

        user_width_valid = user_width.isnumeric() and int(user_width) >= 100 and int(user_width) <= 10000
        user_heigth_valid = user_heigth.isnumeric() and int(user_heigth) >= 100 and int(user_heigth) <= 10000
        
        if not (user_width_valid and user_heigth_valid):
            warning_statement = '' \
            f'Given size {user_heigth},{user_width} are not valid values.\n' \
            'Only integers between 100 and 10.000 are accepted.\n' \
            'Using default size'

            print(warning_statement)
            return "1500px", "1500px"

        report_statement = '' \
        'Recieved size:\n' \
        f'width = {user_width}, heigth = {user_heigth}'
        
        print(report_statement)
        return f"{user_width}px", f"{user_heigth}px"
    
    def __traverse(self, options:list[str]|None) -> None:
        available_options = {"-h" : 0, "-g" : 1}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)

        if "-h" in valid_user_options.keys():
            help_statement = ''\
            'This command is used to get further information about an active graph.\n' \
            'Mandatory Options:\n' \
            ' -g [graphname] : The name of the graph that you want to traverse\n' \
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \

            print(help_statement)
            return None
        
        graph = self.__check_graph_option(valid_user_options)
        if not graph:
            return None
        
        if not self.__warn_options(invalid_user_options):
            return None
        
        root_name = graph.get_root()
        root_id = graph.get_node_id_from_name(root_name)
        assert root_id

        current_node = graph.get_node_from_id(root_id)
        assert current_node

        self.__run_traverse(graph, root_name, root_id, current_node)
            
        return None

    def __run_traverse(self, graph:Graph, root_name:str, root_id:int, current_node:Node):

        while True:
            report_statement = '' \
            f'Currently focused on the node: {current_node.get_name()} ({current_node.get_id()})\n' \
            'Please select your next action:\n' \
            '   (1) get further node information\n' \
            '   (2) get information about special nodes\n' \
            '   (3) change the currently focused node\n' \
            '   (4) end graph traversal\n'
            
            user_choice = input(report_statement)
            
            if user_choice not in ["1", "2", "3", "4"]:
                warning_statement = '' \
                f'Given input \"{user_choice}\" is not one of the three options (1, 2, 3 or 4)'

                print(warning_statement)
                continue

            match user_choice:
                case "1":
                    self.__get_further_info(graph, current_node)

                case "2":
                    highest_in = graph.get_node_with_highest_in()
                    highest_out = graph.get_node_with_highest_out()

                    report_statement = '' \
                    f'Graph root: {root_name} ({root_id})\n' \
                    f'Highest_incoming: {highest_in.get_name()} ({highest_in.get_id()}) with {len(highest_in.get_incoming())} incoming\n' \
                    f'Highest outgoing: {highest_out.get_name()} ({highest_out.get_id()}) with {len(highest_in.get_outgoing())} incoming'

                    print(report_statement)

                case "3":
                    new_focus = self.__change_focus(graph)
                    
                    if new_focus:
                        current_node = new_focus

                case "4":
                    report_statement = '' \
                    'Ending graph traversal'

                    print(report_statement)
                    break

    def __get_further_info(self, graph:Graph, current_node:Node) -> None:
        node_name = current_node.get_name()
        node_id = current_node.get_id()
        node_depth = current_node.get_depth()

        incoming = current_node.get_incoming()
        outgoing = current_node.get_outgoing()

        keywords = current_node.get_keywords()
        report_statement = '' \
                    f'Node {node_name} ({node_id})\n' \
                    f'found at a distance of {node_depth} to the root of the graph.\n' \
                    f'{len(incoming + outgoing)} neighbours found ({len(incoming)} incoming and {len(outgoing)} outgoing)\n' \
                    f'Important keywords:'
                    
        print(report_statement)

        for keyword in keywords:
            print(f' - {keyword}')

        report_statement = '' \
                    'To view found neighbours please select (in) incoming or (out) outgoing or skip to skip\n'

        user_action = input(report_statement)

        match user_action:
            case "in":
                self.__get_incoming_information(graph, incoming)

            case "out":
                self.__get_outgoing_information(graph, outgoing)    

            case _:
                if user_action != "":
                    warning_statement = '' \
                                f'Found user input \"{user_action}\" to not match [in|out].\n' \
                                'Skipping'

                    print(warning_statement)

        return None

    def __get_outgoing_information(self, graph:Graph, edges:list[Edge]) ->  None:
        report_statement = '' \
        'Outgoing neighbours:'

        print(report_statement)

        neighbour_ids = [neighbour.get_end_id() for neighbour in edges]
        neighbours = [graph.get_node_from_id(id) for id in neighbour_ids]
        filtered_neighbours = [neighbour for neighbour in neighbours if neighbour]

        line_string = ''
        for neighbour in filtered_neighbours:
            neighbour_string = f"{neighbour.get_name()} ({neighbour.get_id()}), "

            if len(line_string) + len(neighbour_string) < 80:
                line_string += neighbour_string

            else:
                print(line_string)
                line_string = neighbour_string

        print(line_string)

        return None
    
    def __get_incoming_information(self, graph:Graph, edges:list[Edge]) ->  None:
        report_statement = '' \
        'Incoming neighbours:'

        print(report_statement)

        neighbour_ids = [neighbour.get_start_id() for neighbour in edges]
        neighbours = [graph.get_node_from_id(id) for id in neighbour_ids]
        filtered_neighbours = [neighbour for neighbour in neighbours if neighbour]

        line_string = ''
        for neighbour in filtered_neighbours:
            neighbour_string = f"{neighbour.get_name()} ({neighbour.get_id()}), "

            if len(line_string) + len(neighbour_string) < 80:
                line_string += neighbour_string

            else:
                print(line_string)
                line_string = neighbour_string

        print(line_string)

        return None

    def __change_focus(self, graph:Graph) -> Node | None:
        report_statement = '' \
        'Changing focus to a new node.\n' \
        'Please enter the id of the node you want to switch to:\n'

        user_reponse = input(report_statement)

        if not user_reponse.isnumeric():
            warning_statement = '' \
            f'Given id \"{user_reponse}\" is not a number and can therefore not be a id.\n' \
            'Not changing node focus'

            print(warning_statement)
            return None

        user_given_id = int(user_reponse)

        node = graph.get_node_from_id(user_given_id)

        if not node:
            warning_statement = '' \
            f'Given id \"{user_given_id}\" is not a valid id for the active graph.\n' \
            'Not changing node focus'

            print(warning_statement)
            return None
        
        return node
    
    def __cycles(self, options:list[str]|None) -> None:
        available_options = {"-h" : 0, "-g" : 1, "-t" : 1, "-v" : 0, "-m" : 1}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)

        if "-h" in valid_user_options.keys():
            help_statement = ''\
            'This command is used to find cycles in an active graph.\n' \
            'Mandatory Options:\n' \
            ' -g [graphname] : The name of the graph that you want to traverse\n' \
            ' -t [d|u] : If the cycles should be (d) directed or (u) undirected\n'
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \
            ' -v : verbose output to get further information\n' \
            ' -m [num] : maximum cycle size to search for (Values over 1000 may take longer)\n\n' \
            'Warning: Very big graphs may take longer to find cycles and undirected cycles take significatnly longer to find' 

            print(help_statement)
            return None
        
        graph = self.__check_graph_option(valid_user_options)
        if not graph:
            return None

        cycle_type_set = "-t" in valid_user_options.keys()
        if not cycle_type_set:
            failure_statement =  '' \
            'The option \"-t\" is manditory and was not set.\n' \
            'Please use \"-t [d|u]\" to select a cycle type to search for.'

            print(failure_statement)
            return None
        
        wrapped_cycle_type = valid_user_options.get("-t")
        assert wrapped_cycle_type
        cycle_type = wrapped_cycle_type[0]

        if cycle_type not in ["d", "u"]:
            failure_statement = '' \
            f'Given the cycle type: {cycle_type}\n' \
            'This is neither "d" nor "u" and therefore invalid.\n' \
            'Please only use (d) directed or (u) undirected.'
            
            print(failure_statement)
            return None
        
        if not self.__warn_options(invalid_user_options):
            return None
        
        verbose = "-v" in valid_user_options.keys()

        max_cycle_size_given = "-m" in valid_user_options.keys()

        if max_cycle_size_given:
            wrapped_cycle_size = valid_user_options.get("-m")
            assert wrapped_cycle_size
            max_cycle_size = wrapped_cycle_size[0]

            if not max_cycle_size.isnumeric():
                failure_statement = '' \
                ''

                print(failure_statement)
                return None
            
            max_cycle_size = int(max_cycle_size)

            if max_cycle_size < 3 or max_cycle_size > 10000:
                failure_statement = '' \
                ''

                print(failure_statement)
                return None
        else:
            max_cycle_size = None

        circle_manager = CircleManager()

        match cycle_type:
            case "d":
                cycles = circle_manager.get_directed_cycles(graph, verbose, max_cycle_size)

            case "u":
                cycles = circle_manager.get_undirected_cycles(graph, verbose, max_cycle_size)

            case _:
                #Unreachable but SonarQube throws a hissy fit without
                cycles = set()

        
        self.__do_stuff_with_cycles(graph, cycles)

        return None
    
    def __do_stuff_with_cycles(self, graph:Graph, cycles:set[Cycle]) -> None:
        
        report_statement =  '' \
        f'Found {len(cycles)} cycles\n' \
        'Saving to file (see txtfiles)'

        fixed_cycles = list(cycles)
        print(report_statement)
        self.filehelper.write_cycles_to_file(graph, fixed_cycles)

        report_statement = '' \
        'Select circles for visualization by ID (See file) or skip to skip'

        print(report_statement)

        while True:
            user_reponse = input()
            
            if not user_reponse:
                break

            if not user_reponse.isnumeric():
                warning_statement = '' \
                f'Given response \"{user_reponse}\" is not a number but also not empty to skip.\n' \
                'Please give ID or skip'

                print(warning_statement)
                continue

            user_id = int(user_reponse)

            if user_id < 0 or user_id > len(fixed_cycles) - 1:
                warning_statement = '' \
                f'Given ID \"{user_id}\" falls outside of the permitted values [0, {len(fixed_cycles) - 1}].\n' \
                'Please select a valid ID or skip'

                print(warning_statement)
                continue

            selected_cycle = fixed_cycles[user_id]

            self.__visualize_cycle(graph, selected_cycle, user_id)

        return None 

    def __visualize_cycle(self, graph:Graph, cycle:Cycle, id:int) -> None:
        settings = {
            "width" : "1500px",
            "height" : "1500px",
            "bgcolor" : "#00052E",
            "nodecolor" : "#97c2fc"
        }

        fancy_vis = FancyVisualizer(settings)

        cycle_path = cycle.get_path()

        nodes = [graph.get_node_from_id(id) for id in cycle_path]
        filtered_nodes = [node for node in nodes if node]

        root_name = filtered_nodes[0].get_name()

        edges = [Edge(cycle_path[idx], cycle_path[idx + 1]) for idx in range(len(cycle_path) - 1)]
        edges.append(Edge(cycle_path[-1], cycle_path[0]))   

        converted_cycle = Graph(root_name, set(filtered_nodes), set(edges))

        fancy_vis.generate_cycle_graph(converted_cycle, id)
        return None

    def __check_graph_option(self, valid_user_options:dict[str, list[str]]) -> Graph|None:

        graph_option_set = "-g" in valid_user_options.keys()

        if not graph_option_set:
            failure_statement = '' \
            'The option \"-g\" is manditory and was not set.\n' \
            'Please use \"-g [graph_name]\" to select a graph to save'

            print(failure_statement)
            return None
        
        wrapped_graph_name = valid_user_options.get("-g")
        assert wrapped_graph_name
        graph_name = wrapped_graph_name[0]

        graph_exists = graph_name in self.graphs.keys()
        if not graph_exists:
            failure_statement = '' \
            f'Given the graph name: {graph_name}\n' \
            'This is not the name of any active graph.\n' \
            'Please give the name of an active graph.\n' \
            'View these by using the \"view\" command'

            print(failure_statement)
            return None
        
        graph = self.graphs.get(graph_name)

        return graph
    

def main() -> int:
    return 0


if __name__ == "__main__":
    main()