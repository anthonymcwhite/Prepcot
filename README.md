# 🧃 Prepcot — Apricot Data Assistant

**Prepcot** is a desktop GUI tool built with Python and PySide6 that helps human service organizations prepare Apricot data for import—cleanly, efficiently, and with style.

Whether you’re wrangling CSVs, mapping templates, or formatting exports, Prepcot gives you a slick and intuitive way to transform your data.

[![Watch The Demo](https://www.youtube.com/watch?v=A7dMdkGc61Y)]

---

## 🎯 Features

- ✅ **Drag-and-Drop or File Upload**
- 📋 **Smart Preview** — skips the first column and shows the first 5 columns × 10 rows
- 🧩 **Template Selector** — apply the right format for different programs
- 🗃️ **Activity Log** — track every import & output with timestamps
- 👓 **Output Viewer** — view saved files right in the app
- 🧹 **Clear Preview**, 🔁 **Revert Last Import**, and ❌ **Exit** buttons
- 🖤 Sleek **dark theme UI** with modern tabbed interface

---

## 💻 Getting Started

### 1. **Download the Code**

Clone or download this repo:

<tt>bash<br>
git clone https://github.com/anthonymcwhite/prepcot.git</tt>

2. Install Dependencies
Run this in your terminal or command prompt:

pip install -r requirements.txt

3. Run Prepcot
python main.py
Make sure all folders (templates, value_mappings, output_data, etc.) are in the same directory. You're off to the races

🛠️ Troubleshooting
❌ Error: No module named 'PySide6'
→ Run pip install -r requirements.txt
⚠️ Preview not showing properly?
→ Make sure you're uploading a valid .csv or .xlsx
→ Preview skips the first column, and shows only 5 columns × 10 rows
🗂 Output not saving?
→ Ensure the /output_data/ folder exists
→ Make sure the file isn’t open in another program
🎨 GUI glitches?
→ Confirm you're using Python 3.8+ with full PySide6 support
→ Some visuals depend on system theme support for dark palettes
<p>
📁 Directory Structure <br>
prepcot/<br>
├── main.py<br>
├── prepcot_gui/<br>
│   └── gui_main.py<br>
├── template_manager/<br>
│   └── template_loader.py<br>
├── data_mapper/<br>
│   └── formatter.py<br>
├── templates/<br>
├── value_mappings/<br>
├── output_data/<br>
├── logs/<br>
└── icons/<br>
</p>
🤝 Credits
Created with energy and intention by Tony, with build support from Microsoft Copilot.
Powered by community leadership and support from the Wilmington Alliance 💼

"You're not just formatting data—you're shaping impact."
— Prepcot Philosophy





