#!/usr/bin/python

class Eldopy:

  # digital true and false
  LOW = 0
  HIGH = 1

  # wireless true and false
  WTRUE = 136
  WFALSE = 142

  # pulselength is 300 micoseconds = 0.0003 seconds (300.0 / 1000000.0)
  PULSE_LENGTH_MICROSECONDS = 300

  # repeat transmission
  REPEAT = 10



  def __convertAB440CodeToBinary(self, code):
    digitalCode = ""
    for r in range(0, Eldopy.REPEAT):
      for c in range(0, 16):
        x = 128
        for i in range(1,9):

          if ((code[c] & x) > 0):
            digitalCode += str(Eldopy.HIGH)
          else:
            digitalCode += str(Eldopy.LOW)

          x = x >> 1

    return digitalCode



  def generateAB440BinaryCode(self, codeStr, activate):
    # validate code
    if len(codeStr) != 6:
      print("The code must be 6 characters long")
      return

    for i in range(0, 5):
      if codeStr[i] != '1' and codeStr[i] != '0':
        print("The code must be in this format: 10101A")
        return

    if not (ord(codeStr[5]) >= ord('A') and ord(codeStr[5]) <= ord('E')):
      print("The code must be in this format: 10101B")
      return

    # default code
    code = [142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 128, 0, 0, 0]

    # parse device-code
    for i in range(0, 5):
      if codeStr[i] == '1':
        code[i] = Eldopy.WTRUE
      else:
        code[i] = Eldopy.WFALSE

    # parse device-id (A - E)
    id = pow(2, ord(codeStr[5]) - 65)

    # set device-id
    x = 1
    for i in range(1,6):
      if ((id & x) > 0):
        code[4 + i] = Eldopy.WTRUE
      else:
        code[4 + i] = Eldopy.WFALSE
      x = x << 1

    # set status
    if activate:
      code[10] = Eldopy.WTRUE;
      code[11] = Eldopy.WFALSE;
    else:
      code[10] = Eldopy.WFALSE
      code[11] = Eldopy.WTRUE

    return self.__convertAB440CodeToBinary(code)



if __name__ == '__main__':
  import sys
  if len(sys.argv) == 4:
    from gpyio import GPyIO
    gpyioobj = GPyIO(int(sys.argv[1]))
    eldopy = Eldopy()
    gpyioobj.digitalWriteSequence(eldopy.generateAB440BinaryCode(sys.argv[2],(sys.argv[3] == 'True')), Eldopy.PULSE_LENGTH_MICROSECONDS)
  else:
    print("run this script with the following arguments:")
    print("./eldopy.py gpioNumber AB440CodeString OnOffBoolean")
    print("")
    print("example:")
    print("./eldopy.py 3 11011B True")
    print("this will switch on 11011B via GPIO Pin 3")
