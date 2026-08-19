"""
Generate graph.png visualization of the LangGraph topology.

Uses LangGraph's draw_mermaid_png() or mermaid.ink rendering service,
falling back to a high-res diagram generation.
"""

import sys
import os
import io
import base64
import urllib.request

# Ensure UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph.builder import build_graph


def main():
    graph = build_graph()
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")

    # 1. Try LangGraph built-in draw_mermaid_png
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        with open(output_path, "wb") as f:
            f.write(png_data)
        print(f"✅ graph.png created successfully via LangGraph draw_mermaid_png: {output_path}")
        return
    except Exception as e:
        print(f"Notice: draw_mermaid_png native call: {e}")

    # 2. Try fetching from mermaid.ink API using Mermaid graph definition
    try:
        mermaid_code = graph.get_graph().draw_mermaid()
        # Save .mmd file as well
        with open("graph.mmd", "w", encoding="utf-8") as f:
            f.write(mermaid_code)

        encoded_mermaid = base64.b64encode(mermaid_code.encode("utf-8")).decode("ascii")
        url = f"https://mermaid.ink/img/{encoded_mermaid}"
        
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            png_bytes = response.read()
            with open(output_path, "wb") as f:
                f.write(png_bytes)
        print(f"✅ graph.png created successfully via Mermaid.ink: {output_path}")
        return
    except Exception as e:
        print(f"Notice: mermaid.ink fetch: {e}")

    # 3. If online services unavailable, create clean PIL diagram
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGBA", (1000, 750), (250, 250, 252, 255))
        draw = ImageDraw.Draw(img)

        # Draw Title
        draw.text((320, 25), "Travel Assistant — LangGraph Topology", fill=(30, 41, 59, 255))

        # Define node boxes
        nodes = {
            "START": (420, 70, 580, 110, "#4f46e5", "#ffffff"),
            "parse_input": (380, 150, 620, 200, "#3b82f6", "#ffffff"),
            "check_knowledge": (360, 240, 640, 290, "#f59e0b", "#ffffff"),
            "vectorstore_retrieve": (180, 340, 440, 390, "#10b981", "#ffffff"),
            "web_search": (560, 340, 820, 390, "#06b6d4", "#ffffff"),
            "fetch_weather": (260, 440, 480, 490, "#8b5cf6", "#ffffff"),
            "fetch_images": (520, 440, 740, 490, "#ec4899", "#ffffff"),
            "aggregate_response": (360, 540, 640, 590, "#10b981", "#ffffff"),
            "END": (440, 640, 560, 680, "#64748b", "#ffffff"),
        }

        for name, (x1, y1, x2, y2, bg, fg) in nodes.items():
            draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=bg, outline=(200, 200, 200), width=2)
            draw.text(((x1 + x2) // 2 - len(name) * 4, (y1 + y2) // 2 - 8), name, fill=fg)

        # Draw lines
        def line(p1, p2):
            draw.line([p1, p2], fill=(100, 116, 139, 255), width=2)

        line((500, 110), (500, 150))
        line((500, 200), (500, 240))
        # Conditional edge
        line((430, 290), (310, 340))
        line((570, 290), (690, 340))
        # Fan out
        line((310, 390), (370, 440))
        line((310, 390), (630, 440))
        line((690, 390), (370, 440))
        line((690, 390), (630, 440))
        # Fan in
        line((370, 490), (450, 540))
        line((630, 490), (550, 540))
        # End
        line((500, 590), (500, 640))

        img.save(output_path)
        print(f"✅ graph.png created successfully via PIL renderer: {output_path}")
    except Exception as e:
        print(f"❌ Error creating graph.png: {e}")


if __name__ == "__main__":
    main()
