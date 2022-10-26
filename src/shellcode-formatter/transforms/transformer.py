from io import BytesIO
from transforms.definitions import ShellcodeDefinition

class Transformer:

    def __init__(self, definition:ShellcodeDefinition):
        self.definition = definition

    def transform_shellcode(self, shellcode:BytesIO) -> str:
        return transform_shellcode(shellcode, self.definition)



def _split_lines(bytes, definition:ShellcodeDefinition) -> list:
    """
    Splits the raw bytes of the shellcode into a list of lines to be processed
    against the definition
    """

    if definition.bytes_per_line == 0:
        line_length = len(bytes)
    else:
        line_length = definition.bytes_per_line
    
    raw_lines:list = [bytes[i:i+line_length] for i in range(0, len(bytes), line_length)]

    return raw_lines

def _format_lines(raw_lines:list, definition:ShellcodeDefinition) -> str:
    """
    Breaks each line down into a list of bytes, then formats the bytes into a string
    based on the definition. then joins the bytes to match the line format.

    Supported byte formats:
    - ff (hex lowercase)
    - FF (hex uppercase)
    - 255 (decimal)
    - 377 (octal)

    Any prefix or suffix will be left untouched, only the above characters will be replaced


    Returns a string of the formatted lines
    """
    lines = list();

    for line_number, raw_line in enumerate(raw_lines):

        if "ff" in definition.byte_format:
            # Lowercase hex format

            bytes = []
            for raw_byte in raw_line:
                # raw_byte = b'\x01'
                byte = definition.byte_format.replace("ff", f"{raw_byte:02x}")
                bytes.append(byte)
                
            line = definition.byte_separator.join(bytes)


        elif "FF" in definition.byte_format:
            # Uppercase hex format
            bytes = []
            for raw_byte in raw_line:
                # raw_byte = b'\x01'
                byte = definition.byte_format.replace("FF", f"{raw_byte:02X}")
                bytes.append(byte)
                
            line = definition.byte_separator.join(bytes)

        elif "255" in definition.byte_format:
            # Decimal format

            bytes = []
            for raw_byte in raw_line:
                # raw_byte = b'\x01'
                byte = definition.byte_format.replace("255", f"{raw_byte:03d}")
                bytes.append(byte)
                
            line = definition.byte_separator.join(bytes)

        elif "377" in definition.byte_format:
            # Octal format

            bytes = []
            for raw_byte in raw_line:
                # raw_byte = b'\x01'
                byte = definition.byte_format.replace("377", f"{raw_byte:03o}")
                bytes.append(byte)
                
            line = definition.byte_separator.join(bytes)

        else:
            raise Exception("Invalid byte format")


        if line_number == 0 and definition.first_line_format is not None:
            # First line
            lines.append(definition.first_line_format.replace("~~BYTES~~", line))
        elif line_number == len(raw_lines) - 1 and definition.last_line_format is not None:
            # Last line
            lines.append(definition.last_line_format.replace("~~BYTES~~", line))
        else:
            # All other lines
            lines.append(definition.line_format.replace("~~BYTES~~", line))

    # Combne the lines into a single string
    lines = "".join(lines)
    return lines


def transform_shellcode(shellcode:BytesIO, definition:ShellcodeDefinition) -> str:
    """
    Transforms a raw binary file into a string based on the provided definition
    """

    raw_lines = _split_lines(shellcode, definition)

    lines = _format_lines(raw_lines, definition)
    
    # Replace the output format with the lines
    output = definition.output_format.replace("~~LINES~~", lines)
    # Add in the byte count
    output = output.replace("~~BYTE_COUNT~~", str(len(shellcode)))

    return output