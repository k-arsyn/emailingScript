import smtplib

# import openpyxl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "thivya.pu.1112@gmail.com"
password = "vzlz doty chtm kipo"

batch_size = 100
pause_interval = 200

skip_first_row = False
# mail content
subject = "Invitation to conduct Training and Placement Drive at IIIT Tiruchirappalli"
body = """
<html>

<body>
    <div id="m_4766314667824339457m_1141515213813004951m_989401897241482182m_4826805108592420475m_-6043100329379199540m_1010140240428729838m_-1069575930772762628m_-4767455898096336807gmail-:18s"
        aria-label="Message Body" role="textbox" aria-multiline="true" style="direction:ltr;min-height:43px"
        aria-controls=":1be" aria-expanded="false">
        <p class="MsoNormal" style="margin:0cm 0cm 0.0001pt;text-align:justify;line-height:normal"><span
                style="background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
                <font face="arial, sans-serif">Dear Sir / Madam,</font>
            </span></p>
        <p class="MsoNormal" style="margin:0cm 0cm 0.0001pt;text-align:justify;line-height:normal">
            <font face="arial, sans-serif">&nbsp;</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 0.0001pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">Greetings!</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 0.0001pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">Hope you are safe and healthy.</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 0.0001pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">&nbsp;</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 0.0001pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif"><span style="letter-spacing:-0.15pt">W</span><span
                    style="color:rgb(51,51,51)">e would like to collaborate with your esteemed organization for
                    placements and internships.&nbsp;</span>Please find below a short write-up about our College and the
                current batch that would appear for placements.</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 0.0001pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">&nbsp;</font>
        </p>
        <p style="box-sizing:border-box;margin:0px 0px 10px;text-align:justify;color:rgb(51,51,51)">
            <font face="arial, sans-serif"><span style="box-sizing:border-box;font-weight:700">Indian Institute of
                    Information Technology Tiruchirappalli (IIITT)</span>, also known as&nbsp;<span
                    style="box-sizing:border-box;font-weight:700">IIIT Trichy</span>, is an&nbsp;<span
                    style="box-sizing:border-box;font-weight:700">Institute of National Importance</span>&nbsp;and one
                among the 20 IIITs proposed under&nbsp;<span style="box-sizing:border-box;font-weight:700">the
                    non-profit Public-Private Partnership (PPP) Model by MHRD</span>.&nbsp;<font
                    style="color:rgb(34,34,34)"><span style="color:rgb(51,51,51)">IIITT is an academic and research
                        institute fully funded by</span><span style="color:rgb(51,51,51)">&nbsp;the&nbsp;</span><span
                        style="color:rgb(51,51,51);box-sizing:border-box;font-weight:700">Government of
                        India</span><span style="color:rgb(51,51,51)">,</span><span
                        style="color:rgb(51,51,51)">&nbsp;the&nbsp;</span><span
                        style="color:rgb(51,51,51);box-sizing:border-box;font-weight:700">Government of Tamil
                        Nadu,</span><span style="color:rgb(51,51,51)">&nbsp;</span><span
                        style="color:rgb(51,51,51)">and</span><span style="color:rgb(51,51,51)">&nbsp;</span><span
                        style="color:rgb(51,51,51);box-sizing:border-box;font-weight:700">Industry Partners</span><span
                        style="color:rgb(51,51,51)">&nbsp;</span><span style="color:rgb(51,51,51)">in the ratio of
                        50:35:15</span></font>.<span style="color:rgb(34,34,34)">&nbsp;Our campus is located
                    at&nbsp;</span>Sethurappatti<span style="color:rgb(34,34,34)">, Tiruchirappalli.</span></font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 0.0001pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">&nbsp;</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 8pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">Our undergraduate students graduated in the previous years
                with&nbsp;excellent track records. Our sixth batch of students&nbsp;<b><u>graduating in
                        2025</u></b>&nbsp;is ready for placements this year. The Batch profile for the current batch is
                as follows:</font>
        </p>
        <div id="m_4766314667824339457m_1141515213813004951m_989401897241482182m_4826805108592420475m_-6043100329379199540m_1010140240428729838m_-1069575930772762628m_-4767455898096336807gmail-:18s"
            aria-label="Message Body" role="textbox" aria-multiline="true" style="direction:ltr;min-height:43px"
            aria-controls=":1be" aria-expanded="false">
            <table border="0" cellpadding="0" cellspacing="0" width="488" style="border-collapse:collapse;width:366pt">

                <colgroup>
                    <col width="335" style="width:251pt">
                    <col width="153" style="width:115pt">
                </colgroup>
                <tbody>
                    <tr height="20" style="height:15pt">
                        <td height="20" width="335"
                            style="height:15pt;width:251pt;font-size:11pt;color:white;font-weight:700;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:none;border-bottom:0.5pt solid rgb(169,208,142);border-left:0.5pt solid rgb(169,208,142);background:rgb(112,173,71);padding:0px;vertical-align:bottom">
                            Course</td>
                        <td width="153"
                            style="width:115pt;font-size:11pt;color:white;font-weight:700;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:0.5pt solid rgb(169,208,142);border-bottom:0.5pt solid rgb(169,208,142);border-left:none;background:rgb(112,173,71);text-align:center;vertical-align:middle;padding:0px">
                            Number of Students</td>
                    </tr>
                    <tr height="20" style="height:15pt">
                        <td height="20"
                            style="height:15pt;font-size:11pt;color:black;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:none;border-bottom:0.5pt solid rgb(169,208,142);border-left:0.5pt solid rgb(169,208,142);background:rgb(226,239,218);padding:0px;vertical-align:bottom">
                            B.Tech. in Computer Science and
                            Engineering</td>
                        <td
                            style="font-size:11pt;color:black;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:0.5pt solid rgb(169,208,142);border-bottom:0.5pt solid rgb(169,208,142);border-left:none;background:rgb(226,239,218);text-align:center;vertical-align:middle;padding:0px">
                            37 (34 boys and 3 girls)</td>
                    </tr>
                    <tr height="20" style="height:15pt">
                        <td height="20"
                            style="height:15pt;font-size:11pt;color:black;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:none;border-bottom:0.5pt solid rgb(169,208,142);border-left:0.5pt solid rgb(169,208,142);padding:0px;vertical-align:bottom">
                            B.Tech.
                            in Electronics and Communication Engineering</td>
                        <td
                            style="font-size:11pt;color:black;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:0.5pt solid rgb(169,208,142);border-bottom:0.5pt solid rgb(169,208,142);border-left:none;text-align:center;vertical-align:middle;padding:0px">
                            37 (33
                            boys and 4 girls)</td>
                    </tr>
                    <tr height="20" style="height:15pt">
                        <td height="20"
                            style="height:15pt;font-size:11pt;color:black;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:none;border-bottom:0.5pt solid rgb(169,208,142);border-left:0.5pt solid rgb(169,208,142);background:rgb(226,239,218);padding:0px;vertical-align:bottom">
                            M.Tech. in Computer Science and
                            Engineering</td>
                        <td
                            style="font-size:11pt;color:black;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:0.5pt solid rgb(169,208,142);border-bottom:0.5pt solid rgb(169,208,142);border-left:none;background:rgb(226,239,218);text-align:center;vertical-align:middle;padding:0px">
                            4 (3 boys and 1 girl)</td>
                    </tr>
                    <tr height="20" style="height:15pt">
                        <td height="20"
                            style="height:15pt;font-size:11pt;color:black;font-weight:700;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:none;border-bottom:0.5pt solid rgb(169,208,142);border-left:0.5pt solid rgb(169,208,142);padding:0px;vertical-align:bottom">
                            Total</td>
                        <td
                            style="font-size:11pt;color:black;font-weight:700;font-family:Calibri,sans-serif;border-top:0.5pt solid rgb(169,208,142);border-right:0.5pt solid rgb(169,208,142);border-bottom:0.5pt solid rgb(169,208,142);border-left:none;text-align:center;vertical-align:middle;padding:0px">
                            78</td>
                    </tr>

                </tbody>
            </table>
        </div><br>
        <p class="MsoNormal"
            style="margin:0cm 0cm 8pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">We have trained them to become best-in-class engineering professionals by
                training them in multidimensional facets of&nbsp;<b>Information and Communication Technology (ICT</b>).
                To enhance their real-time knowledge and to give them hands-on experience, they are encouraged to
                undergo&nbsp;<b><u>Six-months Internship</u></b>&nbsp;in the eighth semester.</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 8pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">We invite your company for the Placements 2025 of IIIT Trichy!</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 8pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">We would also like to invite you to offer&nbsp;<b>Internships</b>&nbsp;to our
                talented&nbsp;<b><u>Pre-Final</u></b><u>&nbsp;</u>Students who are interested in
                pursuing&nbsp;their&nbsp;<b><u>2-month Summer Internship</u>&nbsp;<u>in 2025</u></b>&nbsp;at your
                esteemed organization.<br></font>
        </p>
        <div id="m_4766314667824339457m_1141515213813004951m_989401897241482182m_4826805108592420475m_-6043100329379199540m_1010140240428729838m_-1069575930772762628m_-4767455898096336807gmail-:18s"
            aria-label="Message Body" role="textbox" aria-multiline="true" style="direction:ltr;min-height:43px"
            aria-controls=":1be" aria-expanded="false">
            <table border="0" cellpadding="0" cellspacing="0" width="523" style="border-collapse: collapse; width: 392pt;">

 <colgroup><col width="368" style="width: 276pt;">
 <col width="155" style="width: 116pt;">
 </colgroup><tbody><tr height="20" style="height: 15pt;">
  <td height="20" class="gmail-xl63" width="368" style="height: 15pt; width: 276pt; color: white; font-weight: 700; border-top: 0.5pt solid rgb(169, 208, 142); border-right: none; border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: 0.5pt solid rgb(169, 208, 142); background: rgb(112, 173, 71); padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; vertical-align: bottom; border-image: initial;">Course</td>
  <td class="gmail-xl67" width="155" style="width: 116pt; color: white; font-weight: 700; text-align: center; vertical-align: middle; border-top: 0.5pt solid rgb(169, 208, 142); border-right: 0.5pt solid rgb(169, 208, 142); border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: none; background: rgb(112, 173, 71); padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; border-image: initial; text-wrap: nowrap;">Number of Students</td>
 </tr>
 <tr height="20" style="height: 15pt;">
  <td height="20" class="gmail-xl64" width="368" style="height: 15pt; border-top: none; width: 276pt; color: black; border-right: none; border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: 0.5pt solid rgb(169, 208, 142); background: rgb(226, 239, 218); padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; vertical-align: bottom; border-image: initial;">B.Tech. in Computer Science and Engineering</td>
  <td class="gmail-xl68" style="border-top: none; color: black; text-align: center; vertical-align: middle; border-right: 0.5pt solid rgb(169, 208, 142); border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: none; background: rgb(226, 239, 218); padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; border-image: initial; text-wrap: nowrap;">66 (43 boys and 23 girls)</td>
 </tr>
 <tr height="20" style="height: 15pt;">
  <td height="20" class="gmail-xl65" width="368" style="height: 15pt; border-top: none; width: 276pt; color: black; border-right: none; border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: 0.5pt solid rgb(169, 208, 142); background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; vertical-align: bottom; border-image: initial;">B.Tech. in Electronics and Communication Engineering</td>
  <td class="gmail-xl69" style="border-top: none; color: black; text-align: center; vertical-align: middle; border-right: 0.5pt solid rgb(169, 208, 142); border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: none; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; border-image: initial; text-wrap: nowrap;">59 (36 boys and 23 girls)</td>
 </tr>
 <tr height="20" style="height: 15pt;">
  <td height="20" class="gmail-xl64" width="368" style="height: 15pt; border-top: none; width: 276pt; color: black; border-right: none; border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: 0.5pt solid rgb(169, 208, 142); background: rgb(226, 239, 218); padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; vertical-align: bottom; border-image: initial;">M.Tech. in Computer Science and Engineering</td>
  <td class="gmail-xl68" style="border-top: none; color: black; text-align: center; vertical-align: middle; border-right: 0.5pt solid rgb(169, 208, 142); border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: none; background: rgb(226, 239, 218); padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; border-image: initial; text-wrap: nowrap;">5 (4 boys and 1 girl)</td>
 </tr>
 <tr height="20" style="height: 15pt;">
  <td height="20" class="gmail-xl64" width="368" style="height: 15pt; border-top: none; width: 276pt; color: black; border-right: none; border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: 0.5pt solid rgb(169, 208, 142); background: rgb(226, 239, 218); padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; vertical-align: bottom; border-image: initial;">M.Tech. in VLSI</td>
  <td class="gmail-xl68" style="border-top: none; color: black; text-align: center; vertical-align: middle; border-right: 0.5pt solid rgb(169, 208, 142); border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: none; background: rgb(226, 239, 218); padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; border-image: initial; text-wrap: nowrap;">3 (2 boys and 1 girl)</td>
 </tr>
 <tr height="20" style="height: 15pt;">
  <td height="20" class="gmail-xl66" width="368" style="height: 15pt; border-top: none; width: 276pt; color: black; font-weight: 700; border-right: none; border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: 0.5pt solid rgb(169, 208, 142); background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; vertical-align: bottom; border-image: initial;">Total</td>
  <td class="gmail-xl70" style="border-top: none; color: black; font-weight: 700; text-align: center; vertical-align: middle; border-right: 0.5pt solid rgb(169, 208, 142); border-bottom: 0.5pt solid rgb(169, 208, 142); border-left: none; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-family: Calibri, sans-serif; border-image: initial; text-wrap: nowrap;">133</td>
 </tr>

</tbody>
</table>
        </div><br>
        <p class="MsoNormal"
            style="margin:0cm 0cm 8pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">Kindly find the detailed information about the institution in the brochure
                attached with this mail and also available at&nbsp;<a href="http://placement.iiitt.ac.in/"
                    target="_blank"
                    data-saferedirecturl="https://www.google.com/url?q=http://placement.iiitt.ac.in/&amp;source=gmail&amp;ust=1727169923220000&amp;usg=AOvVaw1kQYE7of_sj8ejw4SBAhQu">placement.iiitt.ac.in</a>
            </font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 8pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">Please&nbsp;find below the Placement Participation and Internship Details
                forms,<b>&nbsp;</b>which we request you kindly fill in.</font>
        </p>
        <p class="MsoNormal"
            style="margin:0cm 0cm 8pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
            <font face="arial, sans-serif">Looking forward to collaborating with your esteemed organization.</font>
        </p>
        <font color="#888888">
            <p class="MsoNormal"
                style="margin:0cm 0cm 8pt;text-align:justify;line-height:normal;background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial">
                <font face="arial, sans-serif">&nbsp;</font><span style="color:rgb(34,34,34)"></span>
            </p>
        </font>
        <div contenteditable="false" class="gmail_chip gmail_drive_chip"
            style=" width: 386px; height: 20px; max-height: 20px; background-color: #f5f5f5; margin: 6px 0; padding: 10px; color: #222; font: normal 400 14px/20px 'Google Sans', sans-serif; cursor: default; border: 1px solid #ddd; ">
            <a href="https://docs.google.com/document/d/1Qa-2cgEbBW0MoDpL0ir0yVfNUWKMDHdlwwf4SJbEYVk/edit?usp=drive_web"
                target="_blank"
                style=" color: #202124; display: inline-block; max-width: 356px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-decoration: none; cursor: pointer; border: none; "
                aria-label="'25 PLACEMENT PARTICIPATION FORM-IIITT">
                <img style="vertical-align: text-bottom; border: none; padding-right: 10px; height: 20px;" alt=""
                    src="https://ci3.googleusercontent.com/meips/ADKq_NafpOCmjZTzmvv0p5oA762Cgxg-2YU9mOJyBqgJEAj2TuIwIYI-1VlbUYEFyDc6E0smU716T9oSCttTJ-osDqrvaF4qoe4ohMJDIMSEhAiSKZOpABCE-0JrZdGZVyoA0XpyQ-6L76OL_RkFVft7BNWa=s0-d-e1-ft#https://drive-thirdparty.googleusercontent.com/16/type/application/vnd.google-apps.document">
                &nbsp;
                <span dir="ltr" style="vertical-align: bottom">'25 PLACEMENT PARTICIPATION FORM-IIITT
                </span>
            </a>
            <img src="//ssl.gstatic.com/ui/v1/icons/mail/gm3/1x/close_baseline_nv700_20dp.png" class="gmail_chip_remove"
                aria-label="Remove attachment"
                style="display:none; padding-left: 10px; cursor: pointer; width: 20px; height: 20px; float: right; ">
        </div>
        <div contenteditable="false" class="gmail_chip gmail_drive_chip"
            style="width: 386px; height: 20px; background-color: rgb(245, 245, 245); margin: 6px 0px; padding: 10px; color: rgb(34, 34, 34); font: 400 14px / 20px 'Google Sans', sans-serif; cursor: default; border: 1px solid rgb(221, 221, 221);">
            <a href="https://docs.google.com/document/d/11_TASwhLKCKHwOrOd4LqI-umzKcQpgi6Pj6ZbpSiIEs/edit?usp=drive_web"
                target="_blank"
                style=" color: #202124; display: inline-block; max-width: 356px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-decoration: none; cursor: pointer; border: none; "
                aria-label="'25 INTERNSHIP DETAILS FORM-IIITT">
                <img style="vertical-align: text-bottom; border: none; padding-right: 10px; height: 20px;" alt=""
                    src="https://ci3.googleusercontent.com/meips/ADKq_NafpOCmjZTzmvv0p5oA762Cgxg-2YU9mOJyBqgJEAj2TuIwIYI-1VlbUYEFyDc6E0smU716T9oSCttTJ-osDqrvaF4qoe4ohMJDIMSEhAiSKZOpABCE-0JrZdGZVyoA0XpyQ-6L76OL_RkFVft7BNWa=s0-d-e1-ft#https://drive-thirdparty.googleusercontent.com/16/type/application/vnd.google-apps.document">
                &nbsp;
                <span dir="ltr" style="vertical-align: bottom; text-decoration: none;">'25 INTERNSHIP DETAILS FORM-IIITT
                </span>
            </a>
            <img src="//ssl.gstatic.com/ui/v1/icons/mail/gm3/1x/close_baseline_nv700_20dp.png" class="gmail_chip_remove"
                aria-label="Remove attachment"
                style="padding-left: 10px; cursor: pointer; width: 20px; height: 20px; float: right; display: none;">
        </div>
        <div contenteditable="false" class="gmail_chip gmail_drive_chip"
            style=" width: 386px; height: 20px; max-height: 20px; background-color: #f5f5f5; margin: 6px 0; padding: 10px; color: #222; font: normal 400 14px/20px 'Google Sans', sans-serif; cursor: default; border: 1px solid #ddd; ">
            <a href="https://drive.google.com/file/d/1Mr48QkaNUhVav1vLzW625vrLgm8SqogC/view?usp=drive_web"
                target="_blank"
                style=" color: #202124; display: inline-block; max-width: 356px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-decoration: none; cursor: pointer; border: none; "
                aria-label="Placement Brochure-IIITT.pdf"><img
                    style="vertical-align: text-bottom; border: none; padding-right: 10px; height: 20px;" alt=""
                    src="https://ci3.googleusercontent.com/meips/ADKq_Nbd4tXvDxMLE26nqb_K4OWalTaeFUFy2Zv_cXvJjuOdmJD8_MaThQeoW0IvWuuRjW55SByr0FM2oIYdfNhTWT9nqKFr5HjFz9mirJB9OFKeuMXD4kOGqirlW5jt=s0-d-e1-ft#https://drive-thirdparty.googleusercontent.com/16/type/application/pdf">&nbsp;<span
                    dir="ltr" style="vertical-align: bottom">Placement Brochure-IIITT.pdf</span></a><img
                src="//ssl.gstatic.com/ui/v1/icons/mail/gm3/1x/close_baseline_nv700_20dp.png" class="gmail_chip_remove"
                aria-label="Remove attachment"
                style="display:none; padding-left: 10px; cursor: pointer; width: 20px; height: 20px; float: right; ">
        </div>
        <font color="#888888">
            <font face="arial, sans-serif"><span class="gmail_signature_prefix">--</span><br></font>
            <div dir="ltr" class="gmail_signature">
                <div dir="ltr">
                    <font face="arial, sans-serif">Thanks and Regards,</font>
                    <div>
                        <font face="arial, sans-serif">Dr. G. Devasena</font>
                    </div>
                    <div>
                        <font face="arial, sans-serif">Training and Placement Officer</font>
                    </div>
                    <div>
                        <font face="arial, sans-serif"><i>Indian Institute of Information Technology&nbsp;
                                Tiruchirappalli</i></font>
                    </div>
                    <div style="text-align:justify">
                        <font color="#333333" face="arial, sans-serif">Sethurapatti,</font>
                    </div>
                    <div style="text-align:justify">
                        <font color="#333333" face="arial, sans-serif">Trichy-Madurai Highway</font>
                    </div>
                    <div style="text-align:justify">
                        <font color="#333333" face="arial, sans-serif">Tiruchirappalli-620012.</font>
                    </div>
                    <div><span style="color:rgb(51,51,51);text-align:justify">
                            <font face="arial, sans-serif">Ph.: 9042473621 / 9080572205</font>
                        </span></div>
                </div>
            </div>
        </font>
    </div>
</body>

</html>
"""

"""
# Open Excel workbook
excel_file = 'Book2.xlsx'  
wb = openpyxl.load_workbook(excel_file)
sheet = wb.active
"""

email_column = [
    "thivya.pu.1112@gmail.com",
    ]

smtp = smtplib.SMTP(smtp_server, smtp_port)
smtp.starttls()


smtp.login(sender_email, password)


for num, i in enumerate(email_column):
    # if skip_first_row:
    #     skip_first_row = False
    #     continue
    print(num)
    recipient_email = i

    if recipient_email:

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        body_message = MIMEText(body, "html")
        msg.attach(body_message)

        print(f"Sending email to: {recipient_email}")

        try:
            # Send the email
            smtp.sendmail(sender_email, recipient_email, msg.as_string())
        except Exception as e:
            print(f"Error sending email to {recipient_email}: {str(e)}")

        if (num + 1) % batch_size == 0:
            print(f"Pausing for {pause_interval} seconds...")
            smtp.quit()
            time.sleep(pause_interval)
            smtp = smtplib.SMTP(smtp_server, smtp_port)
            smtp.starttls()
            smtp.login(sender_email, password)


smtp.quit()

print("Emails sent individually to each recipient successfully")
