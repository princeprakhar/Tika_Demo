import re
import uuid


class DBASOPFormatter:
    def __init__(self, source):
        self.source = source

    def _is_section(self, text):
        """
        Detect section headers like:
        1. Introduction
        2. Database Information
        """
        return bool(re.match(r'^\d+\.\s+[A-Z][A-Za-z\s\-]+$', text))

    def _is_procedure_step(self, text):
        """
        Detect procedure steps like:
        1. Open the database
        2. Run the command
        """
        return bool(re.match(r'^\d+\.\s+.+', text))

    def chunk(self, tika_doc):
        """
        Convert Tika parsed document into structured chunks
        """
        content = tika_doc.get("content", "")

        if not content:
            return []

        lines = [l.strip() for l in content.split("\n") if l.strip()]

        chunks = []
        current_section = None

        for line in lines:

            # Detect section
            if self._is_section(line):
                current_section = line

                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "type": "section",
                    "content": line,
                    "metadata": {
                        "section": current_section,
                        "source": self.source
                    }
                })
                continue

            # Detect procedure step
            if self._is_procedure_step(line):
                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "type": "procedure_step",
                    "content": line,
                    "metadata": {
                        "section": current_section,
                        "source": self.source
                    }
                })
                continue

            # Normal paragraph
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "type": "paragraph",
                "content": line,
                "metadata": {
                    "section": current_section,
                    "source": self.source
                }
            })

        return chunks
