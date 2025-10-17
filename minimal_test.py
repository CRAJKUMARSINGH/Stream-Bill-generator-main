import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Set up Jinja2 environment with absolute path to templates directory
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
print(f"Template directory: {template_dir}")
env = Environment(loader=FileSystemLoader(template_dir), cache_size=0)

def test_template_loading():
    """Test if templates can be loaded successfully"""
    try:
        # Try to load all templates
        templates_to_test = [
            "first_page.html",
            "deviation_statement.html", 
            "extra_items.html",
            "last_page.html",
            "note_sheet.html"
        ]
        
        for template_name in templates_to_test:
            template = env.get_template(template_name)
            print(f"✓ Successfully loaded {template_name}")
            
        print("All templates loaded successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error loading templates: {e}")
        return False

if __name__ == "__main__":
    print("Testing template loading...")
    success = test_template_loading()
    if success:
        print("Template path fix is working correctly!")
    else:
        print("Template path fix needs adjustment.")