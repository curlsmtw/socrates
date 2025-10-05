class LineOverlapTextSplitter:
    """
    LineOverlapTextSplitter is a class for splitting text into line-based chunks.

    Attributes:
            lines_per_chunk (int): Number of lines to include in each chunk.
            overlap (int): Number of lines from the end of the previous chunk to
                    include at the start of the next chunk.

    Methods:
            split(text): Split the provided text into a list of line-based chunks.
    """

    def __init__(self, lines_per_chunk=5, overlap=2):
        self.lines_per_chunk = lines_per_chunk
        self.overlap = overlap

    def split(self, text):
        lines = text.splitlines()
        chunks = []
        start = 0
        while start < len(lines):
            end = start + self.lines_per_chunk
            chunk = lines[start:end]
            chunks.append("\n".join(chunk))
            next_start = end - self.overlap
            if next_start <= start:
                next_start = end
            start = next_start
        return chunks
