from io import BytesIO

from transforms.definitions import ShellcodeDefinition

def _split_lines(hex_bytes, definition:ShellcodeDefinition):
    if definition.bytes_per_line == 0:
        line_length = len(hex_bytes)
    else:
        line_length = definition.bytes_per_line
    
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

def _format_lines_ng(raw_lines:list, definition:ShellcodeDefinition):
    lines = list();

    for line_number, raw_line in enumerate(raw_lines):
        # raw_line = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\xff'

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


def transform_shellcode(shellcode:BytesIO, definition:ShellcodeDefinition):
    raw_lines = _split_lines(shellcode, definition)

    lines = _format_lines_ng(raw_lines, definition)
    
    # Replace the output format with the lines
    output = definition.output_format.replace("~~LINES~~", lines)
    # Add in the byte count
    output = output.replace("~~BYTE_COUNT~~", str(len(shellcode)))

    return output