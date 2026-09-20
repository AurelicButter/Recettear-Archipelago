from pymem import Pymem

processName = "recettear"

class RecettearProcess(Pymem):
    """
    A helper class to provide standard interactions around the Recettear game process
    """

    def __init__(self) -> None:
        super().__init__(process_name=processName)

    def read_bytes(self, location, byte_amt) -> int:
        """
        Reads a byte value from a memory address

        :param location: The memory address of the value
        :param byte_amt: The length of bytes to read from, starting with the given location.
        """
        return super().read_bytes(location, byte_amt)

    def read_int(self, location, byte_amt) -> int:
        """
        Reads an integer value from a memory address

        :param location: The memory address of the value
        :param byte_amt: The length of bytes to read from, starting with the given location.
        """
        return int.from_bytes(super().read_bytes(location, byte_amt), byteorder='little')
    
    def write_int(self, location, byte_amt, value: int) -> None:
        """
        Writes an integer to a memory address

        :param location: The memory address to write to
        :param byte_amt: The length of bytes to write into, starting with the given location
        :param value: The value to update the location with (ie: 1, 128, etc...)
        """
        super().write_bytes(location, value.to_bytes(byte_amt, byteorder='little'), byte_amt)