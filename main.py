from mast.parser import RDParser
from mast.lexer import tokenize


def main():
    print("Mathematical Abstract Syntax Tree")
    mathematical_string = input("Input your mathematical equation or expression: ")
    tokens = tokenize(mathematical_string)
    print("Mathematical string after processing:")
    print(RDParser(tokens).parse())


if __name__ == "__main__":
    main()
