from graph.graph import Graph
from filehelper import FileHelper
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

            prompt = input("")
            if not prompt:
                self.__default()
                continue
            fragments = prompt.split(" ")
            command = fragments[0]
            options = fragments[1:] if len(fragments) > 1 else None
            
            match command:
                case "help":
                    self.__help()
                    
                case "view":
                    self.__view(options)
                    continue

                case "read":
                    self.__read(options)
                    continue

                case "save":
                    self.__save(options)
                    continue

                case "build":
                    continue

                case "circles":
                    continue

                case "traverse":
                    continue

                case "exit":
                    self.running = False
            
                case _:
                    self.__default(command)
            print('\n')
        saving_statement = '' \
        '----------------------------------------\n' \
        'Saving all active graphs before quitting'
        print(saving_statement)
        amount = len(self.graphs)
        saved = 0
        for name, graph in self.graphs.items():
            self.filehelper.write_graph_to_file(graph, name)
            print('Successfully saved graph' + name + '.')
        
            


        exit_statement = '' \
        '---------------------\n' \
        'Successfully exited.'

        print(exit_statement)
                    
    def __parse_options(self, user_options:list[str], valid_options:dict[str, int]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        valid_user_options = {}
        invalid_user_options = {}

        options_positions = [idx for idx, user_option in enumerate(user_options) if user_option[0] == "-"]
        options_positions.append(len(user_options))

        for idx in range(len(options_positions) - 1):
            
            current = options_positions[idx]
            next = options_positions[idx + 1]

            chunk = user_options[current:next]

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
        '----------------------------------------------------------------------\n' \
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
            
    def __default(self, command:str = None) -> None:
        if command is None:
            default_statement = '' \
            'Please enter any command. Refer to the help command for a list of available commands.'
        else:
            default_statement = '' \
            f'Command \'{command}\' is not recognized,\n' \
            'please refer to the help command for a list of available commands.'

        print(default_statement)
        return None

    def __view(self, options: list[str]) -> None:
        available_options = {"-h" : 0, "-v" : 0}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)
        if "-h" in valid_user_options.keys():
            help_statement = '' \
            'This command is used to view all active graphs that can be used in other commands.\n' \
            'Available Options:\n' \
            ' -h : help option, to display further information. Disables functionality (Currently used)\n' \
            ' -v : verbose output to get further information about the active graphs'

            print(help_statement)

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
    
    def __read(self, options:list[str]) -> None:
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

        if not "-f" in valid_user_options.keys():
            failure_statement = '' \
            'Cannot read graph, cause of missing valid file name to read graph from.\n' \
            'Please use \"-f [filename]\" to select a file.\n' \
            'Files can only be found in the currently selected directory.\n' \
            'For further help, use \"-h\"'

            print(failure_statement)
            return None

        verbose_option = "-v" in valid_user_options.keys()

        file_name = valid_user_options.get("-f")
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
    
    def __save(self, options:list[str]) -> None:
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
            '  -n [filename] : a custom file name for the graph textfile. Default is \"[rootname-size]\"'

            print(help_statement)
            return None
        
        graph_option_set = "-g" in valid_user_options.keys()
        if not graph_option_set:
            failure_statement = '' \
            'The option \"-g\" is manditory and was not set.\n' \
            'Please use \"-g [graph_name]\" to select a graph to save'

            print(failure_statement)
            return None
        
        graph_name = valid_user_options.get("-g")

        graph_exists = graph_name in self.graphs.keys()
        if not graph_exists:
            failure_statement = '' \
            f'Given the graph name: {graph_name}\n' \
            'This is not the name of any active graph.\n' \
            'Please give the name of an active graph'

            print(failure_statement)
            return None

        graph_to_save = self.graphs.get(graph_name)

        verbose_option = "-v" in valid_user_options
        custom_file_name = "-n" in valid_user_options

        if custom_file_name:
            file_name = valid_user_options.get("-n")
        else:
            file_name = f"{graph_name}.txt"
        try:
            self.filehelper.write_graph_to_file(graph_to_save, file_name, verbose_option)
        except Exception as e:
            failure_statement = '' \
            'Saving graph to file failed.\n' \
            'Please refer to the error message for further information\n'
            
            print(failure_statement + str(e))

        return None
    

def main() -> int:
    return 0

if __name__ == "__main__":
    main()