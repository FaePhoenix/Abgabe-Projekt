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
        if len(invalid_user_options) > 0:
            #do stuff
            pass
        if idk
        

        return None
    
    def __read(self, options:list[str]) -> None:
        available_options = {"-h" : 0, "-v" : 0, "-f" : 1}
        valid_user_options, invalid_user_options = self.__parse_options(options, available_options)


        # Assumes -f is set

        file_name = valid_user_options.get("-f")
        read_graph = self.filehelper.read_graph_from_file(file_name)

        self.graphs
        return None
    

def main() -> int:
    return 0

if __name__ == "__main__":
    main()