from datastructures.graph.graph import Graph
from custom_io.filehelper import FileHelper
from logic.graphbuilder import GraphBuilder
import os


class Parser:
    def __init__(self) -> None:
        self.running : bool = True
        self.graphs: dict[str, Graph] = {}
        self.filehelper : FileHelper = FileHelper(os.getcwd())
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

                case "circles":
                    continue

                case "traverse":
                    continue

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
            self.filehelper.write_graph_to_file(graph, name, False)
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
        
        options_positions = [idx for idx, user_option in enumerate(user_options) if user_option[0] == "-"]
        options_positions.append(len(user_options))

        for idx in range(len(options_positions) - 1):
            
            current_pos = options_positions[idx]
            next_pos = options_positions[idx + 1]

            chunk = user_options[current_pos:next_pos]

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
        'traverse: Get further information about an active graph.\n' \
        'circles: Detect circular links in an active graph.\n' \
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

        for name, graph in self.graphs.items():
            if verbose_option:
                graph_line = f'{name}, Density: {graph.get_density}'

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
            'Mandatory Options:\n' \
            ' -f [filename] : specify the filename to read from, only selecting from the currently selected directory\n\n' \
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
            'Files can only be found in the currently selected directory.\n' \
            'For further help, use \"-h\"'

            print(failure_statement)
            return None

        if not self.__warn_options(invalid_user_options):
            return None
        
        verbose_option = "-v" in valid_user_options.keys()

        filename_option = valid_user_options.get("-f")
        assert filename_option
        file_name = filename_option[0]

        read_graph = self.filehelper.read_graph_from_file(file_name, verbose_option) 
        
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
        
        graph_option_set = "-g" in valid_user_options.keys()
        if not graph_option_set:
            failure_statement = '' \
            'The option \"-g\" is manditory and was not set.\n' \
            'Please use \"-g [graph_name]\" to select a graph to save'

            print(failure_statement)
            return None
        
        if not self.__warn_options(invalid_user_options):
            return None
        
        wrapped_graph_name = valid_user_options.get("-g")
        assert wrapped_graph_name
        graph_name = wrapped_graph_name[0]

        graph_exists = graph_name in self.graphs.keys()
        if not graph_exists:
            failure_statement = '' \
            f'Given the graph name: {graph_name}\n' \
            'This is not the name of any active graph.\n' \
            'Please give the name of an active graph'

            print(failure_statement)
            return None

        graph_to_save = self.graphs.get(graph_name)
        assert graph_to_save

        verbose = "-v" in valid_user_options
        custom_file_name = "-n" in valid_user_options

        if custom_file_name:
            wrapped_file_name = valid_user_options.get("-n")
            assert wrapped_file_name
            file_name = wrapped_file_name[0]
        else:
            file_name = f"{graph_name}.txt"
        
        try:
            self.filehelper.write_graph_to_file(graph_to_save, file_name, verbose)
        except Exception as e:
            failure_statement = '' \
            'Saving graph to file failed.\n' \
            'Please refer to the error message for further information\n'
            
            print(failure_statement + str(e))

        return None
    
    def __build(self, options:list[str]|None) -> None:
        available_options = {"-h" : 0, "-v" : 0, "-s" : 1, "-d" : 1, "-r" : 1, "q" : 1}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)

        if "-h" in valid_user_options.keys():
            help_statement = '' \
            'This command is used to build an active graph from the name of an article.\n' \
            'Mandatory Options:\n' \
            ' -r [articlename] : The name of the wikipedia article that you want to use as a root for the graph\n' \
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \
            ' -v : verbose logging to get further information about the graph saving\n' \
            ' -s [num] : the amount of articles to be included. (Default is 500)' \
            ' -d [num] : the maximal depth or distance to the original article that should be included. (Default is 10)'

            print(help_statement)
            return None
        
        root_given = "-r" in valid_user_options.keys()
        if not root_given:
            failure_statement = '' \
            'No root for graph building given. Can\'t start building graph without a starting point.\n' \
            'Aborting graph building.'

            print(failure_statement)
            return None
        
        if not self.__warn_options(invalid_user_options):
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

        verbose = "-v" in valid_user_options.keys()

        if verbose:
            arguments_statement = '' \
            'Starting graph building:\n' \
            f'Root: {graph_root}\n' \
            f'Max graph size: {graph_size}\n' \
            f'Max graph depth: {graph_depth}\n' \
            'Queue type: '
            
            queue_type_name = 'normal queue' if queue_type == "n" else 'priority queue'
            arguments_statement += queue_type_name

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
        custom_size_used = "-s" in valid_user_options.keys()
        if custom_size_used:
            user_size_option = valid_user_options.get("-s")
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
    

def main() -> int:
    return 0


if __name__ == "__main__":
    main()