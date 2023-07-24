# Import the base class
from ht16k33 import HT16K33
import time

class OttoMatrix(HT16K33):
    """
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
    is_sm_disp = False
    is_upside_down = False

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
        
    def isSmartDisplay(self, yes):
        self.is_sm_disp = yes

    def isUpsideDown(self, yes):
        self.is_upside_down = yes
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
        
        #Upside Down
        if self.is_upside_down:
            y = 7 - y
            x = 15 - x        
        
        #Otto Matrix
        oldY = y
        if x < 8:
            y = x
            x = 7 - oldY
        else:
            y = x - 8
            x = 15 - oldY
        #smart display matrix is upside down compared with otto
        if self.is_sm_disp:
            x = 15 -x
            y = 7 - y
        
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
        #smart display matrix is upside down compared with otto
        if self.is_sm_disp:
            x = 15 -x
            y = 7 - y

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
    def matrixClear(self):
        for y in range(8):
            for x in range(16):                
                self.matrixArray[y][x] = 0
                
    def matrixDraw(self):
        for y in range(8):
            for x in range(16):
                self.plot(x,y,self.matrixArray[y][x])
        self.draw()
                
    def clear(self):
        for y in range(8):
            for x in range(16):
                self.plot(x,y,0)
        self.draw()            
   
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
        self.matrixClear()
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
        self.matrixDraw()
        
    def matrixSurprise(self):
        print("surprise")
        self.matrixClear()
        self.matrixArray[0][7] = 1
        self.matrixArray[0][8] = 1
        self.matrixArray[1][5] = 1
        self.matrixArray[0][6] = 1
        self.matrixArray[0][9] = 1
        self.matrixArray[1][10] = 1
        self.matrixArray[2][4] = 1
        self.matrixArray[2][11] = 1
        self.matrixArray[3][4] = 1
        self.matrixArray[3][11] = 1
        self.matrixArray[4][4] = 1
        self.matrixArray[4][11] = 1
        self.matrixArray[5][4] = 1
        self.matrixArray[5][11] = 1
        self.matrixArray[6][5] = 1
        self.matrixArray[7][6] = 1
        self.matrixArray[7][9] = 1
        self.matrixArray[6][10] = 1
        self.matrixArray[7][7] = 1
        self.matrixArray[7][8] = 1
        self.matrixDraw()
     
    
    def matrixAngry(self):
        print("angry")
        self.matrixClear()
        self.matrixArray[7][5] = 1
        self.matrixArray[7][6] = 1
        self.matrixArray[7][7] = 1
        self.matrixArray[7][8] = 1
        self.matrixArray[7][9] = 1
        self.matrixArray[7][10] = 1
        self.matrixArray[6][3] = 1
        self.matrixArray[6][4] = 1
        self.matrixArray[6][6] = 1
        self.matrixArray[6][9] = 1
        self.matrixArray[6][11] = 1
        self.matrixArray[6][12] = 1
        self.matrixArray[5][2] = 1
        self.matrixArray[5][4] = 1
        self.matrixArray[5][6] = 1
        self.matrixArray[5][9] = 1
        self.matrixArray[5][11] = 1
        self.matrixArray[5][13] = 1
        self.matrixArray[4][1] = 1
        self.matrixArray[4][5] = 1
        self.matrixArray[4][10] = 1
        self.matrixArray[4][14] = 1
        self.matrixArray[3][1] = 1
        self.matrixArray[3][14] = 1
        self.matrixArray[2][1] = 1
        self.matrixArray[2][5] = 1
        self.matrixArray[2][6] = 1
        self.matrixArray[2][7] = 1
        self.matrixArray[2][8] = 1
        self.matrixArray[2][9] = 1
        self.matrixArray[2][10] = 1
        self.matrixArray[2][14] = 1
        self.matrixArray[1][1] = 1
        self.matrixArray[1][4] = 1
        self.matrixArray[1][11] = 1
        self.matrixArray[1][14] = 1
        self.matrixArray[0][2] = 1
        self.matrixArray[0][3] = 1
        self.matrixArray[0][12] = 1
        self.matrixArray[0][13] = 1
        self.matrixDraw()
        
         
    def matrixEyes(self):
        print("eyes")
        self.matrixClear()
        self.matrixArray[5][3] = 1
        self.matrixArray[5][4] = 1
        self.matrixArray[4][2] = 1
        #self.matrixArray[4][3] = 1
        #self.matrixArray[4][4] = 1
        self.matrixArray[4][5] = 1
        self.matrixArray[3][2] = 1
        #self.matrixArray[3][3] = 1
        #self.matrixArray[3][4] = 1
        self.matrixArray[3][5] = 1
        self.matrixArray[2][3] = 1
        self.matrixArray[2][4] = 1
        self.matrixArray[5][11] = 1
        self.matrixArray[5][12] = 1
        self.matrixArray[4][10] = 1
        #self.matrixArray[4][11] = 1
        #self.matrixArray[4][12] = 1
        self.matrixArray[4][13] = 1
        self.matrixArray[3][10] = 1
        #self.matrixArray[3][11] = 1
        #self.matrixArray[3][12] = 1
        self.matrixArray[3][13] = 1
        self.matrixArray[2][11] = 1
        self.matrixArray[2][12] = 1
        self.matrixDraw()
        
    def matrixEyesClose(self):
        print("eyes")
        self.matrixClear()
        self.matrixArray[3][2] = 1
        self.matrixArray[3][3] = 1
        self.matrixArray[3][4] = 1
        self.matrixArray[3][5] = 1
        self.matrixArray[3][10] = 1
        self.matrixArray[3][11] = 1
        self.matrixArray[3][12] = 1
        self.matrixArray[3][13] = 1
        self.matrixDraw()
    
    
    def matrixEyesLeft(self):
        print("eyes")
        self.matrixClear()
        self.matrixArray[5][4] = 1
        self.matrixArray[5][5] = 1
        self.matrixArray[4][3] = 1
        #self.matrixArray[4][4] = 1
        #self.matrixArray[4][5] = 1
        self.matrixArray[4][6] = 1
        self.matrixArray[3][3] = 1
        #self.matrixArray[3][4] = 1
        #self.matrixArray[3][5] = 1
        self.matrixArray[3][6] = 1
        self.matrixArray[2][4] = 1
        self.matrixArray[2][5] = 1
        self.matrixArray[5][12] = 1
        self.matrixArray[5][13] = 1
        self.matrixArray[4][11] = 1
        #self.matrixArray[4][12] = 1
        #self.matrixArray[4][13] = 1
        self.matrixArray[4][14] = 1
        self.matrixArray[3][11] = 1
        #self.matrixArray[3][12] = 1
        #self.matrixArray[3][13] = 1
        self.matrixArray[3][14] = 1
        self.matrixArray[2][12] = 1
        self.matrixArray[2][13] = 1
        self.matrixDraw()
        
    def matrixEyesLeftUp(self):
        print("eyes")
        self.matrixClear()
        self.matrixArray[6][4] = 1
        self.matrixArray[6][5] = 1
        self.matrixArray[5][3] = 1
        #self.matrixArray[5][4] = 1
        #self.matrixArray[5][5] = 1
        self.matrixArray[5][6] = 1
        self.matrixArray[4][3] = 1
        #self.matrixArray[4][4] = 1
        #self.matrixArray[4][5] = 1
        self.matrixArray[4][6] = 1
        self.matrixArray[3][4] = 1
        self.matrixArray[3][5] = 1
        self.matrixArray[6][12] = 1
        self.matrixArray[6][13] = 1
        self.matrixArray[4][11] = 1
        #self.matrixArray[4][12] = 1
        #self.matrixArray[4][13] = 1
        self.matrixArray[4][14] = 1
        self.matrixArray[5][11] = 1
        #self.matrixArray[5][12] = 1
        #self.matrixArray[5][13] = 1
        self.matrixArray[5][14] = 1
        self.matrixArray[3][12] = 1
        self.matrixArray[3][13] = 1
        self.matrixDraw()
    
    def matrixEyesLeftDown(self):
        print("eyes")
        self.matrixClear()
        self.matrixArray[4][4] = 1
        self.matrixArray[4][5] = 1
        self.matrixArray[3][3] = 1
        self.matrixArray[3][6] = 1
        self.matrixArray[2][3] = 1
        self.matrixArray[2][6] = 1
        self.matrixArray[1][4] = 1
        self.matrixArray[1][5] = 1
        self.matrixArray[4][12] = 1
        self.matrixArray[4][13] = 1
        self.matrixArray[3][11] = 1
        self.matrixArray[3][14] = 1
        self.matrixArray[2][11] = 1
        self.matrixArray[2][14] = 1
        self.matrixArray[1][12] = 1
        self.matrixArray[1][13] = 1
        self.matrixDraw()
        
    def matrix_left(self):
        for y in range(8):
            recall = self.matrixArray[y][0]
            for x in range(1,16):
                self.matrixArray[y][x-1] = self.matrixArray[y][x]

            self.matrixArray[y][15] = recall
        #self.clear()
        self.matrixDraw()


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

