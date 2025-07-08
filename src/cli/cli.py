class Parser:
    def __init__(self) -> None:
        self.running : bool = True
        return None
    
    def run(self) -> None:
        intro_statement = '' \
        'Starting Wiki-Graph command-line-interface.\n' \
        'Please start by using \'help\' to familiarize yourself with the available commands.' \
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
                    continue

                case "read":
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
                
        exit_statement = 'Successfully exited.'

        print(exit_statement)
                    

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


    
def main() -> int:
    return 0

if __name__ == "__main__":
    main()