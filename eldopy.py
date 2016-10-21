#!/usr/bin/python

from time import sleep

class Eldopy:

  # gpio true and false
  LOW = 0
  HIGH = 1

  # wireless true and false
  WTRUE = 136
  WFALSE = 142

  # pulselenght is 300 micoseconds = 0.0003 seconds (300.0 / 1000000.0)
  PULSE_LENGTH = 0.0003

  # repeat transmission
  REPEAT = 10



  def __init__(self,gpio):
    self.gpio = gpio

    try:
      file1 = open("/sys/class/gpio/export","w")
      file1.write(str(self.gpio))
      file1.close()
    except:
      #print("export failed")
      pass

    try:
      file2 = open("/sys/class/gpio/gpio" + str(self.gpio) + "/direction","w")
      file2.write("out")
      file2.close()
    except:
      #print("direction failed")
      pass

    self.digitalWrite(self.LOW)



  def digitalWrite(self, value):
    filehandle = open("/sys/class/gpio/gpio" + str(self.gpio) + "/value","w")
    filehandle.write(str(value))
    try:
      filehandle.close()
    except:
      print("filehandle coudn't be closed")


  def sendEther(self, code):
    filehandle = open("/sys/class/gpio/gpio" + str(self.gpio) + "/value","w")
    for r in range(0, self.REPEAT):
      for c in range(0, 16):
        x = 128
        for i in range(1,9):

          if ((code[c] & x) > 0):
            self.digitalWrite(self.HIGH)
          else:
            self.digitalWrite(self.LOW)

          sleep(self.PULSE_LENGTH)
          x = x >> 1



  def send433Mhz(self, codeStr, activate):
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
        code[i] = self.WTRUE
      else:
        code[i] = self.WFALSE

    # parse device-id (A - E)
    id = pow(2, ord(codeStr[5]) - 65)

    # set device-id
    x = 1
    for i in range(1,6):
      if ((id & x) > 0):
        code[4 + i] = self.WTRUE
      else:
        code[4 + i] = self.WFALSE
      x = x << 1

    # set status
    if activate:
      code[10] = self.WTRUE;
      code[11] = self.WFALSE;
    else:
      code[10] = self.WFALSE
      code[11] = self.WTRUE

    self.sendEther(code)


if __name__ == '__main__':
  import sys
  if len(sys.argv) == 4:
    eldo = Eldopy(int(sys.argv[1]))
    eldo.send433Mhz(sys.argv[2],(sys.argv[3] == 'True'))
  else:
    print("run this script with the following arguments:")
    print("./eldopy.py gpioNumber AB440CodeString OnOffBoolean")
    print("")
    print("example:")
    print("./eldopy.py 3 11011B True")
    print("this will switch on 11011B via GPIO Pin 3")
