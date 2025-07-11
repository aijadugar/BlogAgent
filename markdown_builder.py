from datetime import datetime
import re

def image_block(prompt_text):
    if prompt_text:
        return f"![AI Image Prompt] {prompt_text}"
    return ""


def build_markdown(content, image_prompts):
    today = datetime.now().strftime("%B %d, %Y")

    title = extract_title(content)
    intro = extract_intro(content)
    sections = extract_sections(content)
    conclusion = extract_conclusion(content)

    markdown = f"""# {title}

**Published on {today}**  

{intro}

{image_block(image_prompts[0]) if len(image_prompts) > 0 else ''}

---

"""

    for i, section in enumerate(sections):
        markdown += f"## {section['title']}\n\n{section['body']}\n\n"
        if i + 1 < len(image_prompts):
            markdown += f"{image_block(image_prompts[i + 1])}\n\n"

    if conclusion:
        markdown += "---\n\n"
        markdown += f"## Conclusion\n\n{conclusion}\n\n"

    markdown += "---\n"
    markdown += "### 💬 **Let us know your thoughts!**\n"
    markdown += "If you enjoyed this post or have questions, drop us a message. More insights coming soon!\n"

    return markdown

def extract_title(content):
    # Extract first non-empty line and clean "Title:" if present
    for line in content.strip().split("\n"):
        if line.strip():
            return line.replace("Title:", "").strip()
    return "Blog Title"

def extract_intro(content):
    # Extract lines under "Introduction:" label until next section or empty line
    lines = content.strip().split("\n")
    intro_lines = []
    capture = False
    for line in lines:
        if re.match(r'^\s*Introduction[:\s]*$', line, re.I):
            capture = True
            continue
        if capture:
            if re.match(r'^\d+\.', line) or re.match(r'^[A-Z ]{3,}$', line) or not line.strip():
                break
            intro_lines.append(line.strip())
    return "\n\n".join(intro_lines) if intro_lines else ""

def extract_sections(content):
    lines = content.strip().split("\n")
    sections = []
    current = None
    for line in lines:
        if re.match(r'^\s*Conclusion[:\s]*$', line, re.I):
            break  # Stop if we reach the Conclusion block
        if re.match(r'^\d+\.\s+', line):
            if current:
                sections.append(current)
            parts = line.split('.', 1)
            title = parts[1].strip() if len(parts) > 1 else line.strip()
            current = {"title": title, "body": ""}
        elif current:
            current["body"] += line.strip() + "\n"
    if current:
        sections.append(current)

    for sec in sections:
        sec["body"] = sec["body"].strip()
    return sections


    # Clean up body trailing newlines
    for sec in sections:
        sec["body"] = sec["body"].strip()
    return sections

def extract_conclusion(content):
    # Extract lines under "Conclusion:" label
    lines = content.strip().split("\n")
    conclusion_lines = []
    capture = False
    for line in lines:
        if re.match(r'^\s*Conclusion[:\s]*$', line, re.I):
            capture = True
            continue
        if capture:
            if not line.strip():
                break
            conclusion_lines.append(line.strip())
    return "\n\n".join(conclusion_lines) if conclusion_lines else ""

