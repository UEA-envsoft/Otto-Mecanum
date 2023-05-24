# Import the base class
from ht16k33 import HT16K33
import time

class OttoMatrix(HT16K33):
    """
    OttoMatrix micropython class for the Otto DIY 16x8 LED matrix
    Version:    0.0
    Author:     Alex Etchells (UEA-envsoft)
    License:    GNU GPL 3
    Copyright:  2023
    
    derived from: ht16k33matrixfeatherwing.py
            https://github.com/smittytone/HT16K33-Python/blob/main/ht16k33matrixfeatherwing.py
            Micro/Circuit Python class for the Adafruit 0.8-in 16x8 LED matrix FeatherWing.

            Version:    3.4.2
            Bus:        I2C
            Author:     Tony Smith (@smittytone)
            License:    MIT
            Copyright:  2023
    """

    # *********** CONSTANTS **********
    # ********** PRIVATE PROPERTIES **********

    width = 16
    height = 8
    is_inverse = False


    matrixArray = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    clearMatrix = matrixArray
    numSp = [[0],[0],[0],[0],[0],[0],[0],[0]]
    num0 = [[0,0,0],[0,0,0],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[0,0,0]]
    num1 = [[0,0,0],[0,0,0],[1,1,1],[0,1,0],[0,1,0],[1,1,0],[0,1,0],[0,0,0]]
    num2 = [[0,0,0],[0,0,0],[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1],[0,0,0]]
    num3 = [[0,0,0],[0,0,0],[1,1,1],[0,0,1],[0,1,1],[0,0,1],[1,1,1],[0,0,0]]
    num4 = [[0,0,0],[0,0,0],
            [0,0,1],
            [0,0,1],
            [1,1,1],
            [1,0,1],
            [1,0,0],
            [0,0,0]]
    num5 = [[0,0,0],[0,0,0],[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1],[0,0,0]]
    num6 = [[0,0,0],[0,0,0],[1,1,1],[1,0,1],[1,1,1],[1,0,0],[1,1,1],[0,0,0]]
    num7 = [[0,0,0],[0,0,0],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[1,1,1],[0,0,0]]
    num8 = [[0,0,0],[0,0,0],[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1],[0,0,0]]
    num9 = [[0,0,0],[0,0,0],[0,0,1],[0,0,1],[1,1,1],[1,0,1],[1,1,1],[0,0,0]]


    numbers = [num0,num1,num2,num3,num4,num5,num6,num7,num8,num9]
    output = []
    totCols = 0

    # *********** CONSTRUCTOR **********

    def __init__(self, i2c, i2c_address=0x70):
        self.buffer = bytearray(self.width * 2)
        super(OttoMatrix, self).__init__(i2c, i2c_address)

    # *********** PUBLIC METHODS **********

    def set_inverse(self):
        """
        Inverts the ink colour of the display

        Returns:
            The instance (self)
        """
        self.is_inverse = not self.is_inverse
        for i in range(self.width * 2):
            self.buffer[i] = (~ self.buffer[i]) & 0xFF
        return self

    def plot(self, x, y, ink=1, xor=False):
        """
        Plot a point on the matrix. (0,0) is bottom left as viewed.

        Args:
            x (integer)   X co-ordinate left to right
            y (integer)   Y co-ordinate bottom to top
            ink (integer) Pixel color: 1 = 'white', 0 = black. NOTE inverse video mode reverses this. Default: 1
            xor (bool)    Whether an underlying pixel already of color ink should be inverted. Default: False

        Returns:
            The instance (self)
        """
        # Bail on incorrect row numbers or character values
        assert (0 <= x < self.width) and (0 <= y < self.height), "ERROR - Invalid coordinate set in plot()"
        
        #Otto Matrix
        oldY = y
        if x < 8:
            y = x
            x = 7 - oldY
        else:
            y = x - 8
            x = 15 - oldY
        
        if ink not in (0, 1): ink = 1
        x2 = self._get_row(x)
        if ink == 1:
            if self.is_set(x ,y) and xor:
                self.buffer[x2] ^= (1 << y)
            else:
                if self.buffer[x2] & (1 << y) == 0: self.buffer[x2] |= (1 << y)
        else:
            if not self.is_set(x ,y) and xor:
                self.buffer[x2] ^= (1 << y)
            else:
                if self.buffer[x2] & (1 << y) != 0: self.buffer[x2] &= ~(1 << y)
        return self

    def is_set(self, x, y):
        """
        Indicate whether a pixel is set.

        Args:
            x (int) X co-ordinate left to right
            y (int) Y co-ordinate bottom to top

        Returns:
            Whether the
        """
        # Bail on incorrect row numbers or character values
        assert (0 <= x < self.width) and (0 <= y < self.height), "ERROR - Invalid coordinate set in is_set()"

        #Otto Matrix
        oldY = y
        if x < 8:
            y = x
            x = 7 - oldY
        else:
            y = x - 8
            x = 15 - oldY

        x = self._get_row(x)
        bit = (self.buffer[x] >> y) & 1
        return True if bit > 0 else False


    # ********** PRIVATE METHODS **********

    def _get_row(self, x):
        """
        Convert a column co-ordinate to its memory location
        in the FeatherWing, and return the location.
        An out-of-range value returns False
        """
        a = 1 + (x << 1)
        if x < 8: a += 15
        if a >= self.width * 2: return False
        return a

   # ************ OTTO MATRIX
   
   
    def matrixIp(self,addr):
        #our output is 4 cols for each number ending in a space and 7 for those ending with a dot
        #there are 3 dots so it is length -3 times 4 + 9
        #4 spaces at the end so make it plus 12
        self.totCols = (len(addr) - 3) * 4 + 12
        for i in range(8):
            row = []
            for j in range(self.totCols):
                row.append(0)
            self.output.append(row)
        col = 0
        i = 0
        doneDot = False
        for c in addr:
            if i > 0 and c != '.':
                if doneDot:
                    doneDot = False
                else:
                    #add a space
                    for y in range(8):
                        self.output[y][col] = 0
                    col +=1
            if c != '.':
                #add character
                for x in range(3):
                    for y in range(8):
                        self.output[y][col] = self.numbers[int(c)][y][x]
                    col+=1
            if  c == '.':
                #add a dot
                doneDot = True
                for x in range(4):
                    for y in range(8):
                        self.output[y][col] = 0
                    if x == 1 or x==2: self.output[4][col] = 1
                    col+=1
            i+=1
        #add a final spaces
        for x in range(4):
            for y in range(8):
                self.output[y][col] = 0
            col+=1
        self.marquee(self.totCols - 16)
         
    def matrixGrin(self):
        print("grin")
        self.matrixArray = self.clearMatrix
        self.matrixArray[6][1] = 1
        self.matrixArray[5][2] = 1
        self.matrixArray[4][3] = 1
        self.matrixArray[3][4] = 1
        self.matrixArray[2][5] = 1
        self.matrixArray[2][6] = 1
        self.matrixArray[2][7] = 1
        self.matrixArray[2][8] = 1
        self.matrixArray[2][9] = 1
        self.matrixArray[2][10] = 1
        self.matrixArray[3][11] = 1
        self.matrixArray[4][12] = 1
        self.matrixArray[5][13] = 1
        self.matrixArray[6][14] = 1
        self.clear()
        for y in range(8):
            for x in range(16):
                if self.matrixArray[y][x] == 1: self.plot(x,y,1)
        self.draw()
                
    def matrix_left(self):
        for y in range(8):
            recall = self.matrixArray[y][0]
            for x in range(1,16):
                self.matrixArray[y][x-1] = self.matrixArray[y][x]

            self.matrixArray[y][15] = recall
        self.clear()
        for y in range(8):
            for x in range(16):
                if self.matrixArray[y][x] == 1: self.plot(x,y,1)


    def marquee(self,moves):
        #draw first 16 columns
        self.clear()
        for y in range(8):
            for x in range(16):
                if self.output[y][x] == 1: self.plot(x,y,1)
        self.draw()
        time.sleep(0.5)
        #advance through the columns
        for m in range(moves):
            for y in range(8):
                recall = self.output[y][0]
                for x in range(1,self.totCols):
                    self.output[y][x-1] = self.output[y][x]

                self.output[y][self.totCols-1] = recall
            self.clear()
            for y in range(8):
                for x in range(16):
                    if self.output[y][x] == 1: self.plot(x,y,1)
            self.draw()
            time.sleep(0.5)