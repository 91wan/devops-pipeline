import re
import os

readme_path = "README.md"
narrative_path = "docs/RELEASE_NARRATIVE.md"

if not os.path.exists(readme_path):
    with open(readme_path, "w") as f:
        f.write("# DevOps Pipeline (V8 Architecture)\n\n## 💡 架构师轶事\n\n## 🔧 Installation\n...")

if os.path.exists(narrative_path):
    with open(narrative_path, "r") as f: narrative = f.read()
    with open(readme_path, "r") as f: readme = f.read()

    # Simple injection logic
    new_readme = re.sub(r'## 💡 架构师轶事.*?(?=##|$)', f'## 💡 架构师轶事\n\n{narrative}\n\n', readme, flags=re.DOTALL)
    if new_readme == readme and '💡 架构师轶事' not in readme:
        new_readme += f'\n\n## 💡 架构师轶事\n\n{narrative}'
    
    with open(readme_path, "w") as f: f.write(new_readme)
