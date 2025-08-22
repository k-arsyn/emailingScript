import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time
from math import ceil

# SMTP configuration for Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587
#Sender mail 
sender_email = "placement@iiitt.ac.in"
password = "capg qusx rdzg jzyc"

# Email content
subject = "Invitation to participate in Training and Placement Drive at IIIT Tiruchirappalli"

body_template = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background-color:#fff;font-family:'Segoe UI',sans-serif;color:#333;">

<!-- Main container -->
<div style="max-width:700px;margin:0 auto;background:#fff;padding:20px;">

  <h2 style="font-size:20px;color:#2c3e50;margin-bottom:12px;">Greetings from IIIT Tiruchirappalli!</h2>

  <p style="line-height:1.6;font-size:14px; color:#000000;">
    Dear HR team at {company},<br>
  </p>
    
  <p style="line-height:1.6;font-size:14px; color:#000000;">
    We are pleased to invite your esteemed organization for our <strong>Placements & Internship Drive 2026</strong>. Our students are rigorously trained in:
  </p>

  <ul style="font-size:14px;line-height:1.6;">
    <li>Artificial Intelligence & Machine Learning</li>
    <li>Full-stack Software Development</li>
    <li>Robotics & Embedded Systems</li>
    <li>VLSI and Chip Design</li>
  </ul>

  <p style="line-height:1.6;font-size:14px; margin-bottom: 20px;">
    To have better insight of our talent pool, please find below an overview of the academic programs 
    that shape our student's expertise along with the distribution of students across each stream.
  </p>

  <!-- Program Structure -->
  <div class="project-section" style="margin-bottom: 24px;">
    <h3 style="color:#2c3e50;">Program Structure at IIIT Trichy</h3>
    <ul style="margin-top:10px;">
      <li><strong>B.Tech (Bachelor of Technology)</strong>
        <ul>
          <li>Computer Science and Engineering</li>
          <li>Electronics and Communication Engineering</li>
        </ul>
      </li>
      <li style="margin-top:10px;"><strong>M.Tech (Master of Technology)</strong>
        <ul>
          <li>M.Tech in Computer Science and Engineering (2 Years)</li>
          <li>M.Tech in VLSI Systems (2 Years)</li>
        </ul>
      </li>
    </ul>
  </div>

  <!-- Student Distribution Header -->
  <div style="border:2px solid #2c3e50;padding:8px 16px;border-radius:8px;background:#ecf0f1;width:fit-content;margin:20px auto;">
    <h3 style="margin:0; font-size:18px; color:#2c3e50;">Student Distribution – Program-wise</h3>
  </div>

  <!-- Charts -->
  <div style="text-align: center; margin-top: 20px;">
    <div style="display:flex;justify-content:center;gap:100px;flex-wrap:wrap;">
      <!-- Chart 1 -->
      <div style="text-align:center;">
        <h4 style="margin:0;font-size:14px;color:#2c3e50;">Placement Batch 2026</h4>
        <img src="cid:chart1" alt="Placement Batch 2026" width="200" style="display:block;margin:auto;">
        <div style="font-size:12px;margin-top:8px;">
          <span style="color:#2ecc71;">■ B.Tech CSE – 66 students</span><br>
          <span style="color:#3498db;">■ B.Tech ECE – 58 students</span><br>
          <span style="color:#8e44ad;">■ M.Tech CSE – 5 students</span><br>
          <span style="color:#f39c12;">■ M.Tech ECE – 3 students</span>
        </div>
      </div>
      <!-- Chart 2 -->
      <div style="text-align:center;">
        <h4 style="margin:0;font-size:14px;color:#2c3e50;">Pre-final Year</h4>
        <img src="cid:chart2" alt="Pre-final Year" width="200" style="display:block;margin:auto;">
        <div style="font-size:12px;margin-top:8px;">
          <span style="color:#2ecc71;">■ CSE – 66 students</span><br>
          <span style="color:#3498db;">■ ECE – 53 students</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Note -->
  <div style="background:#eaf6ff;padding:8px;margin:16px auto;font-size:13px;border-left:4px solid #3498db;max-width:600px;">
    <strong>NOTE : Pre-Final Year Students – Open for Summer Internships</strong>
  </div>

  <!-- Gender Distribution -->
  <div style="border:2px solid #2c3e50;padding:8px 16px;border-radius:8px;background:#f0f0f0;width:fit-content;margin:20px auto;">
    <h3 style="margin:0;font-size:18px;color:#2c3e50;">Gender Distribution – Year & Program-wise</h3>
  </div>

  <div style="max-width:600px;margin:auto;">
    <!-- Repeat block for each -->
    <div style="margin-bottom:8px;font-size:13px;">
      <strong>BTech CSE 4th Year</strong>
      <div style="display:flex;">
        <div style="background:#3498db;color:white;padding:4px;width:36%;text-align:right;">43</div>
        <div style="background:#dd4472;color:white;padding:4px;width:19%;text-align:left;">23</div>
      </div>
    </div>
    <div style="margin-bottom:8px;font-size:13px;">
      <strong>BTech ECE 4th Year</strong>
      <div style="display:flex;">
        <div style="background:#3498db;color:white;padding:4px;width:30%;text-align:right;">36</div>
        <div style="background:#dd4472;color:white;padding:4px;width:18%;text-align:left;">22</div>
      </div>
    </div>
    <div style="margin-bottom:8px;font-size:13px;">
      <strong>BTech CSE 3rd Year</strong>
      <div style="display:flex;">
        <div style="background:#3498db;color:white;padding:4px;width:37%;text-align:right;">44</div>
        <div style="background:#dd4472;color:white;padding:4px;width:18%;text-align:left;">22</div>
      </div>
    </div>
    <div style="margin-bottom:8px;font-size:13px;">
      <strong>BTech ECE 3rd Year</strong>
      <div style="display:flex;">
        <div style="background:#3498db;color:white;padding:4px;width:31%;text-align:right;">37</div>
        <div style="background:#dd4472;color:white;padding:4px;width:13%;text-align:left;">16</div>
      </div>
    </div>
    <div style="margin-bottom:8px;font-size:13px;">
      <strong>M.Tech CSE</strong>
      <div style="display:flex;">
        <div style="background:#3498db;color:white;padding:4px;width:4%;text-align:right;">4</div>
        <div style="background:#dd4472;color:white;padding:4px;width:1%;text-align:left;">1</div>
      </div>
    </div><div style="margin-bottom:8px;font-size:13px;">
      <strong>M.Tech VLSI</strong>
      <div style="display:flex;">
        <div style="background:#3498db;color:white;padding:4px;width:2%;text-align:right;">2</div>
        <div style="background:#dd4472;color:white;padding:4px;width:1%;text-align:left;">1</div>
      </div>
    </div>
  </div>
  </div>

  <div style="text-align:center;margin-top:10px;font-size:12px;">
    <span style="color:#3498db;">■ Boys</span> &nbsp;
    <span style="color:#dd4472;">■ Girls</span>
  </div>

  <!-- Student Achievements -->
  <div style="border:2px solid #2c3e50;padding:8px 16px;border-radius:8px;background:#f0f0f0;width:fit-content;margin:20px auto;">
    <h3 style="margin:0;font-size:18px;color:#2c3e50;">Student Achievements</h3>
  </div>

  <div style="max-width:800px;margin:0 auto;padding:16px 24px;border:1px solid #bdc3c7;border-radius:10px;background:#f8f8f8;font-size:14px;line-height:1.6;color:#2c3e50;">
    <ul style="padding-left: 20px;">
      <li><strong>National winners</strong> at prestigious events like <em>Smart India Hackathon</em> and <em>Odoo Mindbend Hackathon</em>.</li>
      <li><strong>Finalists</strong> at <em>ICPC</em>, <em>Google Cloud Study Jams</em>, and other national-level coding competitions.</li>
      <li><strong>Alumni placed</strong> at top global firms including <em>Goldman Sachs</em>, <em>VISA</em>, <em>FedEx</em>, <em>Qualcomm</em>, <em>JUSPAY</em>, <em>Ola</em>, <em>Rakuten</em>, <em>Costco</em>, <em>Nvidia</em>, <em>Amazon</em> and <em>Walmart</em>.</li>
    </ul>
  </div>

  <!-- Closing -->
  <p style="font-size:14px;line-height:1.5;margin-top:20px;">
    We hope to cultivate a lasting partnership grounded in shared values and mutual growth.<br>
    Also find the attached Placement Brochure, Placement Participation Form and Internship Details Form.<br>
    Explore more at <a href="http://placement.iiitt.ac.in/">placement.iiitt.ac.in</a>
  </p>

  <!-- PDF Attachments -->
  <div style="margin-top:15px;">
    <div style="background:#fff;border:1px solid #ccc;padding:10px;border-radius:5px;margin-bottom:8px;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/PDF_file_icon.svg/32px-PDF_file_icon.svg.png" 
     alt="PDF" width="18" style="vertical-align:middle;margin-right:8px;">
      <a href="https://drive.google.com/file/d/1wgxoEoybz5WdtKIBUOGMbvvk2es74fMm/view?usp=drive_link" style="text-decoration:none;color:#2c3e50;">'26 Placement Participation Form – IIITT.pdf</a>
    </div>
    <div style="background:#fff;border:1px solid #ccc;padding:10px;border-radius:5px;margin-bottom:8px;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/PDF_file_icon.svg/32px-PDF_file_icon.svg.png" 
     alt="PDF" width="18" style="vertical-align:middle;margin-right:8px;">
      <a href="https://drive.google.com/file/d/19pQGfE8O9GCckGtYESTBCR0q0SHahFBN/view?usp=sharing" style="text-decoration:none;color:#2c3e50;">'26 Internship Details Form – IIITT.pdf</a>
    </div>
    <div style="background:#fff;border:1px solid #ccc;padding:10px;border-radius:5px;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/PDF_file_icon.svg/32px-PDF_file_icon.svg.png" 
     alt="PDF" width="18" style="vertical-align:middle;margin-right:8px;">
      <a href="https://drive.google.com/file/d/11DGk6_0y5MYZwF4tkuEZyO8p6lA1MdkH/view?usp=drive_link" style="text-decoration:none;color:#2c3e50;">IIITT – Placement Brochure.pdf</a>
    </div>
  </div>

  <p style="line-height:1.6;font-size:14px; color:#000000;">
    For any further details reach out to our student co-ordinator<br>
    {spoc_name}<br>
    Mobile: {spoc_mobile}
  </p>

  <!-- Footer -->
  <div style="font-size:12px;color:#777;margin-top:15px;">
    Warm regards,<br>
    <strong>Placement Team, IIIT Trichy</strong><br>
    📍 Sethurapatti, Tiruchirappalli, Tamil Nadu<br>
    ✉️ <a href="mailto:placement@iiitt.ac.in">placement@iiitt.ac.in</a> | ☎️ +91-7696265939
  </div>
</div>
</body>
</html>

"""

# Load HR list from Excel
df_companies = pd.read_excel("list.xlsx")
df_spocs = pd.read_excel("SpocDetails.xlsx")

# Drop duplicates by email
df_companies = df_companies.drop_duplicates(subset="E - mail")

num_companies = len(df_companies)
num_spocs = len(df_spocs)
base_count = num_companies // num_spocs
remainder = num_companies % num_spocs

# Assign companies to SPOCs
spoc_assignments = []
company_index = 0
for i, (_, spoc_row) in enumerate(df_spocs.iterrows()):
    count_for_this_spoc = base_count + (1 if i >= num_spocs - remainder else 0)
    assigned_companies = df_companies.iloc[company_index:company_index + count_for_this_spoc]
    company_index += count_for_this_spoc
    for _, comp_row in assigned_companies.iterrows():
        spoc_assignments.append({
            "Company": comp_row["Company"],
            "E - mail": comp_row["E - mail"],
            "SPOC Name": spoc_row["SPOC Name"],
            "Mobile No.": spoc_row["Mobile No."]
        })

df_final = pd.DataFrame(spoc_assignments)


# Config for throttling
batch_size = 100
pause_interval = 200  # seconds

# Connect to SMTP server
smtp = smtplib.SMTP(smtp_server, smtp_port)
smtp.starttls()
smtp.login(sender_email, password)

for idx, row in df_final.iterrows():
    recipient_email = row["E - mail"]
    company = row["Company"]
    spoc_name = row["SPOC Name"]
    spoc_mobile = row["Mobile No."]

    if pd.isna(recipient_email) or pd.isna(company):
        continue

    # Personalize message
    body = body_template.format(company=company,spoc_name=spoc_name, spoc_mobile=spoc_mobile)

    # Prepare message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    # Attach HTML body
    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(body, "html"))

    # Attach first chart
    with open("chart1.png", "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<chart1>")
        img.add_header("Content-Disposition", "inline", filename="chart1.png")
        msg.attach(img)

    # Attach second chart
    with open("chart2.png", "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<chart2>")
        img.add_header("Content-Disposition", "inline", filename="chart2.png")
        msg.attach(img)

    try:
        print(f"Sending to {recipient_email} ({company}) via {spoc_name} ({spoc_mobile})")
        smtp.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print(f"❌ Error sending to {recipient_email}: {e}")

    # Pause after every `batch_size` emails
    if (idx + 1) % batch_size == 0:
        print(f"🕒 Pausing for {pause_interval} seconds after {idx + 1} emails...")
        smtp.quit()
        time.sleep(pause_interval)
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(sender_email, password)

smtp.quit()
print("✅ All emails sent successfully.")
