from pathlib import Path
import re
import yaml

track_folder = Path("/Users/studio/Public/home/_tracks")

for md_file in track_folder.glob("*.md"):
    content = md_file.read_text()
    lines = content.splitlines()
    new_lines = []
    mood_updated = False

    for line in lines:
        if line.strip().lower().startswith("mood:"):
            # Extract list from mood: [ ... ]
            match = re.match(r"mood:\s*\[(.*)\]", line.strip(), re.IGNORECASE)
            if match:
                items = [m.strip() for m in match.group(1).split(",")]
                cleaned = [m for m in items if m.lower() != "nan" and m != ""]
                new_line = f"mood: [{', '.join(cleaned)}]" if cleaned else "mood: []"
                new_lines.append(new_line)
                mood_updated = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    md_file.write_text("\n".join(new_lines))
    if mood_updated:
        print(f"✅ Cleaned: {md_file.name}")
