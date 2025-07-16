# Quick Project Setup Reference

**Copy this checklist for every new project**

## 🚀 **5-Minute Setup**

### **1. Initialize Project**
```bash
mkdir project-name && cd project-name
git init
git config --global user.name "YourUsername"
git config --global user.email "your.email@example.com"
```

### **2. Create Essential Files**
- [ ] `README.md` (use template from PROJECT_ORGANIZATION_TEMPLATE.md)
- [ ] `.gitignore` (copy from template)
- [ ] `requirements.txt` (if applicable)

### **3. File Naming Quick Rules**
- **Scripts**: `<action>_<object>.py` → `analyze_data.py`, `download_files.py`
- **Data**: `<source>_<description>_<date>.csv` → `sales_data_q1_2024.csv`
- **Results**: `<type>_<subject>_version.csv` → `summary_customer_analysis_final.csv`

### **4. First Commit**
```bash
git add .
git commit -m "Initial commit: [Brief project description]"
```

### **5. Connect to GitHub**
```bash
git branch -M main
git remote add origin https://github.com/username/repo-name.git
git push -u origin main
```

## 📋 **README Template (Minimal)**
```markdown
# Project Name
Brief description and purpose.

## Files
- `script.py` - What it does
- `data.csv` - Data source

## Usage
1. Run `python3 script.py`
2. Check `output/` folder

## Data Sources
- **Source**: Where from
- **License**: Usage rights
```

## 🔄 **Development Workflow**
1. Make changes
2. `git add .`
3. `git commit -m "type: description"`
4. `git push`

## ✅ **Before Sharing Checklist**
- [ ] README explains everything
- [ ] File names are clear
- [ ] Data sources documented
- [ ] Code has comments
- [ ] No sensitive info committed 