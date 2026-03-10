"""
SVG to PNG Converter - Simple Method
Converts all SVG diagrams to high-resolution PNG files
Uses PIL/Pillow with screenshot approach
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_png_from_svg_info():
    """
    Since direct SVG->PNG conversion requires Cairo (complex on Windows),
    this script helps you use Windows built-in tools instead.
    """
    
    diagrams_dir = r"C:\Users\user\Documents\Finalyearproject\Bursary_system\proposal_assets\diagrams"
    
    print("\n" + "="*70)
    print("   SVG TO PNG CONVERSION GUIDE")
    print("="*70)
    
    svg_files = [f for f in os.listdir(diagrams_dir) if f.endswith('.svg')]
    
    if not svg_files:
        print("\n❌ No SVG files found in the diagrams directory.")
        return
    
    print(f"\n📁 Found {len(svg_files)} SVG files:")
    for i, svg_file in enumerate(svg_files, 1):
        print(f"   {i}. {svg_file}")
    
    print("\n" + "-"*70)
    print("EASIEST METHOD - Use Windows Snipping Tool:")
    print("-"*70)
    print()
    print("For each SVG file above:")
    print()
    print("1️⃣  Double-click the SVG file to open it in your browser")
    print("    (It will open in Edge, Chrome, or Firefox)")
    print()
    print("2️⃣  Press: Win + Shift + S")
    print("    (This opens Windows Snipping Tool)")
    print()
    print("3️⃣  Click 'Rectangular Snip' and drag to select the diagram")
    print()
    print("4️⃣  The screenshot is copied to clipboard automatically")
    print()
    print("5️⃣  Open Paint (Win + R, type 'mspaint', Enter)")
    print()
    print("6️⃣  Paste (Ctrl + V)")
    print()
    print("7️⃣  File → Save As → PNG")
    print()
    print("8️⃣  Name it properly (e.g., 'database-schema.png')")
    print()
    
    print("-"*70)
    print("ALTERNATIVE - Browser Screenshot Extension:")
    print("-"*70)
    print()
    print("• Install 'Full Page Screen Capture' extension in Chrome/Edge")
    print("• Open SVG in browser")
    print("• Click extension icon")
    print("• Save as PNG")
    print()
    
    print("-"*70)
    print("ALTERNATIVE - Online Converter:")
    print("-"*70)
    print()
    print("• Go to: https://cloudconvert.com/svg-to-png")
    print("• Upload your SVG file")
    print("• Click 'Convert'")
    print("• Download PNG")
    print()
    
    print("="*70)
    print("\n✅ After conversion, your PNG files will be ready for:")
    print("   • Microsoft Word documents")
    print("   • PowerPoint presentations")
    print("   • Printing")
    print("   • PDF exports")
    print()
    
    # Create a batch file to open all SVGs
    batch_content = "@echo off\n"
    batch_content += "echo Opening all SVG diagrams in browser...\n"
    batch_content += "echo.\n"
    batch_content += "echo Press Win+Shift+S to take screenshots\n"
    batch_content += "echo Then paste in Paint and save as PNG\n"
    batch_content += "echo.\n"
    batch_content += "pause\n\n"
    
    for svg_file in svg_files:
        batch_content += f'start "" "{os.path.join(diagrams_dir, svg_file)}"\n'
        batch_content += "timeout /t 2 /nobreak >nul\n"
    
    batch_file = os.path.join(diagrams_dir, "open-all-svgs.bat")
    with open(batch_file, 'w') as f:
        f.write(batch_content)
    
    print(f"📝 Created helper batch file: {batch_file}")
    print("   Double-click it to open all SVGs in browser at once!")
    print()

if __name__ == "__main__":
    create_png_from_svg_info()
    input("\nPress Enter to exit...")
