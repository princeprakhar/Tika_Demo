import json
from formatter import DBASOPFormatter


TIKA_FILE = "../tika_output.json"
SOURCE_FILE = "../sample.pdf"
OUTPUT_FILE = "labelstudio_tasks.json"


def load_tika():
    with open(TIKA_FILE, "r") as f:
        return json.load(f)


def convert_to_labelstudio(chunks):
    tasks = []

    for chunk in chunks:
        content = chunk.get("content")

        if isinstance(content, list):
            content = " | ".join(content)

        task = {
            "data": {
                "text": content,
                "chunk_id": chunk.get("chunk_id"),
                "chunk_type": chunk.get("type"),
                "section": chunk.get("metadata", {}).get("section"),
                "source": chunk.get("metadata", {}).get("source")
            }
        }

        tasks.append(task)

    return tasks


def main():

    # Load Tika JSON
    data = load_tika()

    # Tika document
    tika_doc = data[0] if isinstance(data, list) else data

    # Run formatter
    formatter = DBASOPFormatter(SOURCE_FILE)
    chunks = formatter.chunk(tika_doc)

    print("Total chunks:", len(chunks))

    # Convert to Label Studio format
    tasks = convert_to_labelstudio(chunks)

    # Save tasks
    with open(OUTPUT_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

    print("Label Studio tasks saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()