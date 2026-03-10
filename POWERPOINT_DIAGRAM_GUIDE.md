# SIMPLE POWERPOINT DIAGRAM GUIDE
## Build Your Architecture Diagram in PowerPoint (5 Minutes)

### STEP 1: Open PowerPoint Slide 5
- Insert -> Shapes -> Rectangle (Rounded Corners)

### STEP 2: Create the Boxes (Copy this layout)

**TOP ROW (Blue Boxes - User Interface Layer):**
1. Box 1: "Student Portal" - Fill: Blue (#0ea5e9)
2. Box 2: "Reports & Dashboard" - Fill: Blue (#0ea5e9)

**MIDDLE ROWS (Teal Boxes - Application Layer):**
3. Box 3: "Authentication" - Fill: Teal (#14b8a6)
4. Box 4: "Profile Management" - Fill: Teal (#14b8a6)
5. Box 5: "Bursary Application" - Fill: Teal (#14b8a6)
6. Box 6: "Review Module" - Fill: Teal (#14b8a6)
7. Box 7: "Admin Approval" - Fill: Teal (#14b8a6)
8. Box 8: "Notification Module" - Fill: Teal (#14b8a6)

**BOTTOM ROW (Data & Services):**
9. Box 9: "MySQL Database" - Fill: Orange (#f59e0b) - Use cylinder shape
10. Box 10: "Email Service (SMTP)" - Fill: Purple (#6366f1)
11. Box 11: "Decision & Disbursement" - Fill: Green (#22c55e)

### STEP 3: Arrange the Boxes

```
TOP:
[Student Portal]    [Reports & Dashboard]
         ↓                    ↓
MIDDLE:
[Authentication] → [Profile Management] → [Bursary Application]
                                                 ↓
                   [Review Module] → [Admin Approval]
                                          ↓
                                    [Notification Module]
                                          ↓
BOTTOM:
            [MySQL Database]    [Email Service]    [Disbursement]
```

### STEP 4: Add Arrows
- Insert -> Shapes -> Arrow (Block Arrow or Connector)
- Connect boxes following the flow:
  - Student Portal → Authentication → Profile → Application
  - Application → Review → Admin Approval
  - Application → Notification → Email Service
  - Admin Approval → Notification
  - All middle boxes point to MySQL Database

### STEP 5: Format for Projection
1. Select all boxes: Right-click → Format Shape
2. Text Options:
   - Font: Arial or Calibri
   - Size: 18-22 pt
   - Color: White text on dark boxes
   - Bold: Yes
3. Box Settings:
   - Border: 2-3 pt solid
   - Shadow: Slight outer shadow for depth

### STEP 6: Add Title Above Diagram
"System Architecture Overview"
Font size: 32-36 pt

### STEP 7: Add Legend Below Diagram
Small boxes showing:
- Blue = User Interface
- Teal = Application Modules  
- Orange = Database
- Purple = External Service
- Green = Output

---

## EVEN SIMPLER OPTION: Use SmartArt

1. Insert → SmartArt → Process → Choose "Basic Process" or "Vertical Process"
2. Add your text in each box
3. Right-click SmartArt → Change Colors → Choose colorful palette
4. Format → Change Shapes → Choose rounded rectangles
5. Resize to fit slide

---

## QUICKEST OPTION: Use PowerPoint Designer

1. Create a new slide
2. Type this text:
   ```
   System Flow:
   - Student Portal
   - Authentication
   - Bursary Application
   - Review & Approval
   - Database Storage
   - Email Notifications
   ```
3. PowerPoint will suggest design layouts automatically
4. Choose the flowchart design it suggests
5. Customize colors to match your theme

---

**RECOMMENDATION:** Use the SmartArt or PowerPoint Designer option - they're built-in and take 2 minutes!
