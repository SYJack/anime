import array

class BitMap(object):
    """
    BitMap class
    """
    BITMASK= [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
    BIT_CNT = [bin(i).count("1") for i in range(256)]

    def __init__(self, maxnum=0):
        """
        Create a BitMap
        """
        nbytes = int((maxnum + 7) / 8)
        self.bitmap = array.array('B', [0 for i in range(nbytes)])

    def set(self, pos):
        """
        Set the value of bit@pos to 1
        """
        self.bitmap[int(pos / 8)] |= self.BITMASK[pos % 8]

    def test(self, pos):
        """
        Return bit value
        """
        return (self.bitmap[int(pos / 8)] & self.BITMASK[pos % 8]) != 0