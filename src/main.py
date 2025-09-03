from custom_io.cli.cli import Parser

def main() -> int:
    parser = Parser()
    parser.run()
    return 0


if __name__ == "__main__":
    main()