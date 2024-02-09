import reg_to_nfa as converter
import sys

path = "output/"
useJson = 0

'''
จัดทำโดย
    นาย กิตติกานต์ มากผล 6410450087
    นาย นิสิต นะมิตร 6410451148
    นาย พีรสิษฐ์ พลอยอร่าม 6410451237
    นาย ศิวกร ภาสว่าง 6410451423
    ข้อ 1
'''

if __name__ == "__main__":

    size_argv = len(sys.argv)
    for index in range(1, size_argv):
       if sys.argv[index] == "--out" or sys.argv[index] == "-o":
           useJson = 1

    regex = input()                         # Input Regular Expression
    print(f"\nRecieve: {regex}")
    print("NFA define by:")
    convert = converter.convertRegex(regex)
    converter.createNfa(convert)            # Create NFA Tree

    filename = "NFA_" +str(regex) + ".json"
    path = path + filename   # Path Filename

    if useJson:
        converter.saveToJson(path)
        print(f"NFA Json Name [{filename}] has been save.")
    converter.showNfaTable()