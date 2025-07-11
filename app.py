from flask import Flask, request, jsonify
from agent_blog_creator import generate_blog, generate_image_prompts, humanize_content, insert_images_into_blog
from markdown_builder import build_markdown
from google_upload import upload_to_google_doc

app = Flask(__name__)
DOC_ID = "1qXvYNfCQxgAV7iXAprcJe4kg0YBFY8VqeOiwCR-IM2w" # "1gQ6RWV0LevvnpU8cevTMl0SAB-pajSoz-PihV-LiRlk"   https://docs.google.com/document/d/1qXvYNfCQxgAV7iXAprcJe4kg0YBFY8VqeOiwCR-IM2w/edit?tab=t.0

@app.route("/", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Please provide a blog topic."}), 400

    try:
        print(f"📝 Topic received: {topic}")

        blog = generate_blog(topic)
        prompts = generate_image_prompts(topic)
        humanized = humanize_content(blog)
        blog_with_prompts = insert_images_into_blog(humanized, prompts)
        md = build_markdown(blog_with_prompts, prompts)  # now only one argument

        upload_to_google_doc(md, DOC_ID)

        print("✅ Blog uploaded to Google Docs successfully.")
        return jsonify({"status": "Blog uploaded!", "topic": topic})

    except Exception as e:
        print("❌ Server error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
