import os
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment with absolute path to templates directory
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
print(f"Template directory: {template_dir}")
env = Environment(loader=FileSystemLoader(template_dir), cache_size=0)

try:
    # Try to load a template
    template = env.get_template("first_page.html")
    print("✓ Successfully loaded first_page.html template")
    
    # Try to render it with minimal data
    html_content = template.render(data={"header": [], "items": [], "totals": {}})
    print("✓ Successfully rendered first_page.html template")
    
except Exception as e:
    print(f"✗ Error: {e}")