from io import BytesIO
import binascii

from transforms.definitions import ShellcodeDefinition

def _split_lines(hex_bytes, definition:ShellcodeDefinition):
    if definition.bytes_per_line == 0:
        line_length = len(hex_bytes)
    else:
        line_length = definition.bytes_per_line * 2
    
    raw_lines:list = [hex_bytes[i:i+line_length] for i in range(0, len(hex_bytes), line_length)]

    return raw_lines

def _format_lines(raw_lines:list, definition:ShellcodeDefinition):
    lines = list();

    for line_number, raw_line in enumerate(raw_lines):
        # Convert the hex bytes into the byte format
        if definition.byte_format == "0xff":
            # Convert the hex bytes into 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
            bytes = [f"0x{raw_line[i:i+2].decode('ascii')}" for i in range(0, len(raw_line), 2)]
            # Join the bytes with the byte separator
            line = definition.byte_separator.join(bytes)

        elif definition.byte_format == "\\xff":
            # Convert the hex bytes into \x0a, \x0b, \x0c, \x0d, \x0e, \x0f
            bytes = [f"\\x{raw_line[i:i+2].decode('ascii')}" for i in range(0, len(raw_line), 2)]
            # Join the bytes with the byte separator
            line = definition.byte_separator.join(bytes)

        elif definition.byte_format == "255":
            # Convert the hex bytes into dec 255 with leading zeros
            bytes = [f"{int(raw_line[i:i+2].decode('ascii'), 16):03}" for i in range(0, len(raw_line), 2)]
            
            # Join the bytes with the byte separator
            line = definition.byte_separator.join(bytes)

        # Replace the line format with the line
        if line_number == 0 and definition.first_line_format is not None:
            lines.append(definition.first_line_format.replace("~~BYTES~~", line))
        else:
            lines.append(definition.line_format.replace("~~BYTES~~", line))

    # Combne the lines into a single string
    lines = "".join(lines)
    return lines



def transform_shellcode(shellcode:BytesIO, definition:ShellcodeDefinition):
    # First transform the raw bytes into hex
    hex_bytes = binascii.hexlify(shellcode)

    raw_lines = _split_lines(hex_bytes, definition)

    lines = _format_lines(raw_lines, definition)
    
    # Replace the output format with the lines
    output = definition.output_format.replace("~~LINES~~", lines)
    # Add in the byte count
    output = output.replace("~~BYTE_COUNT~~", str(len(shellcode)))

    return output