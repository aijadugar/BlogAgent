import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_CLIENT = os.getenv("OPENAI_CLIENT")

client = OpenAI(base_url='https://api.a4f.co/v1', api_key=OPENAI_CLIENT)

def call_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="provider-2/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return True, response.choices[0].message.content
    except Exception as e:
        print("❌ GPT API Error:", str(e))
        if hasattr(e, "response") and e.response is not None:
            try:
                print("→ API response text:", e.response.text)
            except:
                pass
        return False, str(e)

def generate_blog(topic):
    blog_prompt = f"""
You are a skilled content writer for a popular lifestyle and wellness blog. Write a long-form, SEO-optimized blog article (~1000–1200 words) about "{topic}" in a professional and engaging tone.

Structure:
- A compelling title
- A 2–3 paragraph introduction
- 4 to 6 H2 sections (numbered and titled)
- Bullet points and examples when needed
- A motivational and thoughtful conclusion

Keep tone natural, helpful, and easy to scan. Include H2 headings with clear formatting.
"""

    success, result = call_gpt(blog_prompt)
    if not success:
        print("❌ GPT API Error:", result)
        return result
    return result

def generate_image_prompts(topic):
    prompt = f"""
Generate 3 unique AI image prompts for the blog titled "{topic}" for use with a generative image API.

Return 3 descriptive lines only, no labels or numbers.
Each line should be:
- Clear and specific
- Descriptive for AI to visualize
- Relevant to key sections of the blog
"""
    success, result = call_gpt(prompt)
    if not success:
        print("❌ Image prompt generation failed:", result)
        return []

    lines = [line.strip() for line in result.strip().split("\n") if line.strip()]
    
    # ✅ Print each prompt clearly in the terminal
    # print("🎨 Image Prompts:")
    # for i, line in enumerate(lines[:3], start=1):
    #     print(f"{i}. {line}")

    return lines[:3]

def insert_images_into_blog(blog_content, prompts):
    """Insert image prompts as markdown after each H2 section."""
    lines = blog_content.split("\n")
    result_lines = []
    prompt_index = 0

    for line in lines:
        result_lines.append(line)
        if line.strip().startswith("##") and prompt_index < len(prompts):
            prompt_text = prompts[prompt_index]
            result_lines.append(f"\n> 📸 *Prompt for AI Image Generation:* `{prompt_text}`\n")
            prompt_index += 1

    return "\n".join(result_lines)

def humanize_content(raw_content):
    edit_prompt = f"""
You're a human blog editor. Polish the following blog post for tone, flow, clarity, and engagement.

Goals:
- Make it feel natural, friendly, and professional
- Improve transitions and readability
- Maintain the structure and core message
- Keep SEO best practices in mind

Content:
{raw_content}
"""
    success, result = call_gpt(edit_prompt)
    if not success:
        print("❌ Humanization failed:", result)
        return raw_content
    return result
