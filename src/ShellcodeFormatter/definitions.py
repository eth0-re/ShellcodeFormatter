class ShellcodeDefinition:

    def __init__(self, name, output_format, byte_format, byte_separator, bytes_per_line:int, line_format, first_line_format=None, last_line_format=None):
        self.name = name
        self.output_format = output_format
        self.byte_format = byte_format
        self.byte_separator = byte_separator
        self.bytes_per_line = bytes_per_line
        self.line_format = line_format
        self.first_line_format = first_line_format
        self.last_line_format = last_line_format

class ShellcodeDefinitions:

    def get_definition(name):
        return definitions[name]
    
    def list_definitions():
        return definitions.keys()


definitions = {
    "csharp": ShellcodeDefinition(
        name="csharp",
        output_format="byte[] buf = new byte[ ~~BYTE_COUNT~~ ] { \n~~LINES~~};",
        byte_format="0xff",
        byte_separator=",",
        bytes_per_line=16,
        line_format="~~BYTES~~,\n",
        last_line_format="~~BYTES~~\n"
    ),
    "powershell": ShellcodeDefinition(
        name="powershell",
        output_format="[Byte[]] $buf = ~~LINES~~",
        byte_format="0xff",
        byte_separator=",",
        bytes_per_line=0,
        line_format="~~BYTES~~"
    ),
    "python": ShellcodeDefinition(
        name="python",
        output_format="buf = b''\n~~LINES~~",
        byte_format="\\xff",
        byte_separator="",
        bytes_per_line=16,
        line_format="buf += b'~~BYTES~~'\n"
    ),
    "vba": ShellcodeDefinition(
        name="vba",
        output_format="Dim buf as Variant\n~~LINES~~",
        byte_format="255",
        byte_separator=", ",
        bytes_per_line=16,
        first_line_format="buf = Array(~~BYTES~~)\n",
        line_format='buf = Split(Join(buf, ",") & "," & Join(Array(~~BYTES~~), ","), ",")\n'
    ),
    "java": ShellcodeDefinition(
        name="java",
        output_format="byte[] buf = new byte[]\n{\n~~LINES~~\n};",
        byte_format="(byte) 0xff",
        byte_separator=",",
        bytes_per_line=8,
        line_format="\t~~BYTES~~,\n",
        last_line_format="\t~~BYTES~~"
    ),
    "c": ShellcodeDefinition(
        name="c",
        output_format="unsigned char buf[] = \n~~LINES~~;",
        byte_format="\\xff",
        byte_separator="",
        bytes_per_line=16,
        line_format="\"~~BYTES~~\"\n",
        last_line_format="\"~~BYTES~~\""
    ),
    "bash": ShellcodeDefinition(
        name="bash",
        output_format="export buf=\\\n~~LINES~~",
        byte_format="\\xff",
        byte_separator="",
        bytes_per_line=16,
        line_format="$'~~BYTES~~'\\\n",
        last_line_format="$'~~BYTES~~'"
    ),
    "ruby": ShellcodeDefinition(
        name="ruby",
        output_format="buf = \n~~LINES~~",
        byte_format="\\xff",
        byte_separator="",
        bytes_per_line=16,
        line_format="\"~~BYTES~~\" +\n",
        last_line_format="\"~~BYTES~~\"\n"
    ),
    "perl": ShellcodeDefinition(
        name="perl",
        output_format="my $buf = \n~~LINES~~",
        byte_format="\\xff",
        byte_separator="",
        bytes_per_line=16,
        line_format="\"~~BYTES~~\" .\n",
        last_line_format="\"~~BYTES~~\"\n"
    ),
    "go": ShellcodeDefinition(
        name="go",
        output_format="buf := []byte{\n~~LINES~~}",
        byte_format="0xff",
        byte_separator=",",
        bytes_per_line=16,
        line_format="\t~~BYTES~~,\n",
        last_line_format="\t~~BYTES~~"
    ),
    "rust": ShellcodeDefinition(
        name="rust",
        output_format="let buf = [\n~~LINES~~];",
        byte_format="0xff",
        byte_separator=",",
        bytes_per_line=16,
        line_format="\t~~BYTES~~,\n",
        last_line_format="\t~~BYTES~~"
    ),
}