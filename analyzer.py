import google.generativeai as genai
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
import os
import time

genai.configure(api_key="AIzaSyAE17QWexTpHQcYfuMPPvlKjvp2LacqumY")

def analyze_question_image(image_path):
    img = Image.open(image_path)
    
    analysis_prompt = """Analyze this test question image carefully.

**Identify:**
1. The question text
2. Whether a graph/diagram is present or missing
3. The answer choices (if any)
4. What's wrong with the question (missing graph, incorrect diagram, wrong answer choices, etc.)

**CRITICAL - Verify Geometric/Mathematical Accuracy of Diagrams:**
If a diagram is present, you MUST verify that it is geometrically and mathematically correct:
- If the question says a shape is "inscribed" in another, ALL vertices of the inner shape must touch the outer shape. If even one vertex does not touch, the diagram is INCORRECT and must be regenerated.
- If the question says shapes are "concentric", they must share the same center.
- If the question mentions specific measurements, angles, or proportions, verify they are visually accurate.
- If the diagram exists but is geometrically wrong, set issue_type to include "incorrect_diagram" and set requires_diagram_generation to true.
- A diagram can be BOTH geometrically incorrect AND have wrong answer choices - report ALL issues.

**Response Format (JSON only):**
{
    "question_text": "extracted question",
    "answer_provided": "the given answer or answer choices",
    "issue_type": "missing_graph|incorrect_graph|incorrect_answers|incorrect_diagram|no_issues (use + to combine, e.g. incorrect_diagram+incorrect_answers)",
    "current_state": "description of what's currently shown, including any geometric inaccuracies",
    "what_should_be_shown": "detailed description of the geometrically correct visual and correct answers",
    "requires_graph_generation": true/false,
    "requires_diagram_generation": true/false,
    "requires_answer_correction": true/false,
    "graph_specifications": {
        "type": "polynomial_curve|geometry_diagram|bar_chart|line_graph|pie_chart|scatter|other",
        "details": "specific details needed to recreate the CORRECT version",
        "key_points": ["list", "of", "important", "features"],
        "labels": {"x": "label", "y": "label"},
        "data_points": "specific coordinates or values if applicable"
    },
    "correct_answers": ["list", "of", "correct", "answer", "choices"] or "single answer"
}

IMPORTANT: If a diagram exists but is geometrically inaccurate (e.g., a square that is supposed to be inscribed in a circle but its corners don't all touch the circle), you MUST set requires_diagram_generation to true so a correct diagram is generated.

Respond with ONLY valid JSON."""

    model = genai.GenerativeModel('gemini-2.5-flash')
    
    for attempt in range(3):
        try:
            response = model.generate_content([analysis_prompt, img])
            break
        except Exception as e:
            if '429' in str(e) and attempt < 2:
                wait_time = (attempt + 1) * 15
                print(f"  Rate limited, waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                raise
    
    analysis_text = response.text.strip()
    if "```json" in analysis_text:
        analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
    elif "```" in analysis_text:
        analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
    
    return json.loads(analysis_text)

def generate_visual_correction(analysis, output_path):
    
    code_generation_prompt = f"""Generate Python code to create the correct visual for this question.

**Question:** {analysis['question_text']}
**What should be shown:** {analysis['what_should_be_shown']}
**Specifications:** {json.dumps(analysis['graph_specifications'], indent=2)}

**Requirements:**
1. Use matplotlib for mathematical graphs or geometry diagrams
2. For geometry problems, use matplotlib patches and shapes
3. High quality (DPI=300)
4. Professional styling with clear labels
5. Save to '{output_path}'
6. Code should be in a function called create_visual()
7. Include all necessary imports within the function
8. Make it publication-quality with proper fonts and colors

**For polynomial curves:**
- Plot smooth curves with numpy
- Mark key points clearly
- Show grid and axes
- Label intercepts and critical points

**For geometry diagrams:**
- Use matplotlib patches (Circle, Rectangle, Polygon)
- Show measurements and labels clearly
- Use appropriate colors and shading
- Maintain correct proportions
- Use equal aspect ratio (ax.set_aspect('equal')) so circles look circular and squares look square

**CRITICAL - Geometric Accuracy for "Inscribed" Shapes:**
- "Square inscribed in a circle" means ALL 4 vertices of the square must lie exactly ON the circle.
- The diagonal of the square equals the diameter of the circle.
- Compute coordinates mathematically: if side = s, then diagonal = s*sqrt(2), radius = s*sqrt(2)/2.
- Center both shapes at the same point. Place square vertices at angles 45, 135, 225, 315 degrees on the circle.
- The shaded region between circle and square should use fill_between or path operations to shade ONLY the area inside the circle but outside the square.
- DO NOT just place a Rectangle inside a Circle without computing whether the vertices actually touch the circle.

Provide ONLY the Python code, no explanations."""

    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Retry logic for rate limits
    for attempt in range(3):
        try:
            response = model.generate_content(code_generation_prompt)
            break
        except Exception as e:
            if '429' in str(e) and attempt < 2:
                wait_time = (attempt + 1) * 15
                print(f"  Rate limited, waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                raise
    
    code = response.text.strip()
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    return code

def create_complete_question_image(analysis, visual_path, output_path):
    
    fig = plt.figure(figsize=(10, 12))
    
    question_ax = plt.subplot2grid((3, 1), (0, 0))
    question_ax.axis('off')
    
    from textwrap import wrap
    wrapped_text = "\n".join(wrap(analysis['question_text'], width=80))
    question_ax.text(0.5, 0.5, wrapped_text, 
                     ha='center', va='center', 
                     fontsize=12, weight='bold')
    
    visual_ax = plt.subplot2grid((3, 1), (1, 0))
    if os.path.exists(visual_path):
        img = plt.imread(visual_path)
        visual_ax.imshow(img)
    visual_ax.axis('off')
    
    answer_ax = plt.subplot2grid((3, 1), (2, 0))
    answer_ax.axis('off')
    
    if isinstance(analysis.get('correct_answers'), list):
        answers_text = "\n\n".join([f"{chr(65+i)}. {ans}" 
                                    for i, ans in enumerate(analysis['correct_answers'])])
    else:
        answers_text = f"ANSWER\n\n{analysis.get('correct_answers', '')}"
    
    answer_ax.text(0.1, 0.9, answers_text, 
                   ha='left', va='top', fontsize=11,
                   family='monospace')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()

def process_question_image(image_path, output_dir="corrected_questions"):    
    os.makedirs(output_dir, exist_ok=True)
    
    basename = os.path.splitext(os.path.basename(image_path))[0]
    
    print(f"\n{'='*70}")
    print(f"Processing: {image_path}")
    print('='*70)
    
    print("Step 1: Analyzing question...")
    try:
        analysis = analyze_question_image(image_path)
    except Exception as e:
        print(f"✗ Error analyzing image: {e}")
        return None
    
    print(f"Issue Type: {analysis['issue_type']}")
    print(f"Current State: {analysis['current_state']}")
    print(f"Should Show: {analysis['what_should_be_shown']}")
    
    analysis_path = os.path.join(output_dir, f"{basename}_analysis.json")
    with open(analysis_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    issue_type = analysis.get('issue_type', '')
    needs_visual = (
        analysis.get('requires_graph_generation') or 
        analysis.get('requires_diagram_generation') or
        'incorrect_diagram' in issue_type or
        'incorrect_graph' in issue_type or
        'missing_graph' in issue_type
    )
    
    if needs_visual:
        if 'diagram' in issue_type:
            analysis['requires_diagram_generation'] = True
        if 'graph' in issue_type:
            analysis['requires_graph_generation'] = True
            
        print("\nStep 2: Generating corrected visual...")
        
        visual_output = os.path.join(output_dir, f"{basename}_visual.png")
        try:
            code = generate_visual_correction(analysis, visual_output)
            
            code_path = os.path.join(output_dir, f"{basename}_code.py")
            with open(code_path, 'w') as f:
                f.write(code)
            print(f"Code saved to: {code_path}")
            
            namespace = {
                'plt': plt, 
                'np': np, 
                'patches': patches,
                'matplotlib': plt.matplotlib
            }
            exec(code, namespace)
            if 'create_visual' in namespace:
                namespace['create_visual']()
            print(f"Visual created: {visual_output}")
        except Exception as e:
            print(f"Error creating visual: {e}")
            print("Continuing without visual generation...")
    
    print("\nStep 3: Creating complete question image...")
    final_output = os.path.join(output_dir, f"{basename}_corrected.png")
    
    visual_path = os.path.join(output_dir, f"{basename}_visual.png") \
                  if needs_visual and \
                     os.path.exists(os.path.join(output_dir, f"{basename}_visual.png")) \
                  else image_path
    
    try:
        create_complete_question_image(analysis, visual_path, final_output)
        print(f"Complete question saved: {final_output}")
    except Exception as e:
        print(f"Error creating final image: {e}")
        return None
    
    return {
        "original": image_path,
        "analysis": analysis_path,
        "corrected": final_output,
        "issue_type": analysis['issue_type']
    }

def batch_process_questions(image_paths, output_dir="corrected_questions"):
    results = []
    
    for i, image_path in enumerate(image_paths, 1):
        print(f"\n{'#'*70}")
        print(f"PROCESSING QUESTION {i}/{len(image_paths)}")
        print('#'*70)
        
        result = process_question_image(image_path, output_dir)
        if result:
            results.append(result)
    
    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print("SUMMARY")
    print('='*70)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {os.path.basename(result['original'])}")
        print(f"   Issue: {result['issue_type']}")
        print(f"   Corrected: {result['corrected']}")
    
    return results

if __name__ == "__main__":
    import glob
    
    test_dir = "test_images"
    output_dir = "corrected_questions"
    
    image_extensions = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp")
    all_images = []
    for ext in image_extensions:
        all_images.extend(glob.glob(os.path.join(test_dir, ext)))
    all_images.sort()
    
    question_images = []
    for img_path in all_images:
        basename = os.path.splitext(os.path.basename(img_path))[0]
        corrected_path = os.path.join(output_dir, f"{basename}_corrected.png")
        if os.path.exists(corrected_path):
            print(f"⏭ Skipping {os.path.basename(img_path)} (correction already exists)")
        else:
            question_images.append(img_path)
    
    if not question_images:
        print("\n All images already have corrections!")
    else:
        print(f"\n {len(question_images)} image(s) to process "
              f"({len(all_images) - len(question_images)} already corrected)")
        results = batch_process_questions(question_images, output_dir)
        print("\n All questions processed!")
        print("Check the 'corrected_questions' folder for outputs")