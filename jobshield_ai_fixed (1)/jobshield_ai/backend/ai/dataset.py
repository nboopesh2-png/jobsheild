"""
Comprehensive authentic training dataset of genuine and scam job offers.
Includes diverse real-world recruitment fraud patterns, internships, MNC offers,
freelance/remote lures, and bilingual Tamil/English examples.
"""

TRAINING_DATA = [
    # ==================== SCAM SAMPLES (Label 1) ====================
    {
        "text": (
            "Congratulations! You have been selected for the position of Data Entry Specialist at Global Tech Solutions. "
            "Salary: Rs. 45,000 per month. Work from home 2 hours daily. "
            "To confirm your seat, you must deposit a refundable registration fee of Rs. 1,500 via UPI to hrdept@upi. "
            "Contact HR Manager Priya on Telegram @globaltech_hr immediately. Offer valid for 24 hours only."
        ),
        "label": 1
    },
    {
        "text": (
            "Dear Applicant, Amazon India HR is offering part-time online rating jobs. "
            "Earn Rs. 3,000 to Rs. 8,000 daily simply by reviewing products and liking YouTube videos. "
            "No interview needed, no experience required. Daily payout guaranteed. "
            "Message our coordinator on Telegram: https://t.me/amazon_parttime_jobs or WhatsApp +919876543210."
        ),
        "label": 1
    },
    {
        "text": (
            "Urgent Hiring! TCS Direct Placement Offer Letter. "
            "You are shortlisted for Software Engineer Trainee. Package 8.5 LPA. "
            "No exam or technical interview required. "
            "Please pay Rs. 3,500 towards document verification and employee ID card processing fee to account number 1092837465 IFSC SBIN0001234. "
            "Failure to pay within 3 hours will result in cancellation of offer."
        ),
        "label": 1
    },
    {
        "text": (
            "Dear Candidate, We found your resume on Job Portal. You are selected for International Remote Customer Support. "
            "Salary: $3,500/month. We will provide brand new Apple MacBook Pro and high speed internet. "
            "Before shipping laptop, candidate must pay courier insurance and customs clearance fee of $85 (Rs. 7,000) through Bitcoin or USDT wallet. "
            "This amount will be refunded in your first salary cheque."
        ),
        "label": 1
    },
    {
        "text": (
            "Infosys Off-Campus Direct Selection Letter 2025. "
            "Role: Junior System Engineer. CTC: Rs. 6,50,000 per annum. "
            "Kindly transfer Rs. 2,999 to Infosys HR Consultancy via Google Pay or PhonePe for medical test and background check kit. "
            "Send payment screenshot to infosys.recruitment.hr@gmail.com."
        ),
        "label": 1
    },
    {
        "text": (
            "Part-time typing work. Earn Rs. 1,000 per page. "
            "Convert scanned image files to MS Word. 100 pages project payout Rs. 1,00,000. "
            "Security deposit of Rs. 2,000 required before giving raw data files. "
            "If accuracy is 90%, deposit is 100% refundable. Contact WhatsApp +91 8899776655."
        ),
        "label": 1
    },
    {
        "text": (
            "Google India Recruitment. Direct appointment letter for Digital Marketing Executive. "
            "Stipend during 1 month training: Rs. 50,000. "
            "Candidate must purchase mandatory training software license key from authorized vendor for Rs. 4,200. "
            "Official email: google.careers.hr@zoho.com. Contact HR Rajesh on Telegram."
        ),
        "label": 1
    },
    {
        "text": (
            "Work from Home Opportunity! Simple mobile task. "
            "Follow Instagram accounts and get instant payout. Recharge Rs. 1,000 and get Rs. 1,800 return. "
            "VIP tasks earn up to Rs. 20,000 daily. Join official Telegram group t.me/fast_task_earning."
        ),
        "label": 1
    },
    {
        "text": (
            "Selected for Wipro Remote Internship 2025! "
            "Stipend: Rs. 30,000/month. Duration: 6 months. "
            "To confirm your internship certificate registration and ID allocation, pay refundable caution deposit of Rs. 1,999. "
            "Contact recruitment executive at wipro.campus.drive2025@outlook.com."
        ),
        "label": 1
    },
    {
        "text": (
            "Congratulations! Flipkart Logistics Executive Offer. "
            "Starting salary Rs. 38,000 per month + company bike allowance. "
            "Submit uniform stitching charges Rs. 1,200 and gate pass fee Rs. 800 to our official UPI: flipkart_hr@okaxis. "
            "Offer expires today at 6 PM. Hurry!"
        ),
        "label": 1
    },
    {
        "text": (
            "அவசர வேலைவாய்ப்பு! வீட்டில் இருந்தபடியே மொபைலில் வேலை செய்து மாதம் ரூ. 40,000 சம்பாதிக்கலாம். "
            "பதிவுக் கட்டணம் ரூ. 1,000 முன்பணம் செலுத்த வேண்டும். "
            "உடனடி வருமானம் பெற டெலிகிராம் குரூப்பில் இணையவும் t.me/tamil_job_earn. கல்வித்தகுதி தேவையில்லை."
        ),
        "label": 1
    },
    {
        "text": (
            "அரசு பதிவு பெற்ற நிறுவனத்தில் டேட்டா என்ட்ரி வேலை. முன்பணம் ரூ. 1,500 ஜிபே அல்லது போன்பே மூலம் செலுத்தவும். "
            "வாரம் ரூ. 15,000 வரை உத்தரவாத வருமானம். தொடர்புக்கு வாட்ஸ்அப் எண் 9840012345."
        ),
        "label": 1
    },
    {
        "text": (
            "Direct Interview Selection at Cognizant Technology Solutions. "
            "Designation: Associate Software Engineer. Salary: 5.5 LPA. "
            "You are exempt from written test due to profile score. "
            "To generate gate entry pass for campus interview at Siruseri, candidate must pay biometric processing fee of Rs. 1,750 to consultant."
        ),
        "label": 1
    },
    {
        "text": (
            "Dear Job Seeker, You have an urgent job offer from Reliance Retail. "
            "Store Assistant Manager position. Salary Rs. 35,000 + food & accommodation. "
            "Send Rs. 2,500 security deposit to recruiter UPI id reliance_hr@ybl. No interview required. Joining next Monday."
        ),
        "label": 1
    },
    {
        "text": (
            "Hotel Hilton Dubai Hiring Staff! Waiter, Cook, Front Desk, Security. "
            "Free Visa, Air Ticket, and Accommodation provided. Salary 4,500 AED. "
            "Candidate must pay visa stamping fee Rs. 12,000 to local agency bank account. Contact via WhatsApp only."
        ),
        "label": 1
    },
    {
        "text": (
            "Airlines Ground Staff Recruitment 2025. Indigo / Air India ground operations. "
            "12th Pass or Any Degree. Salary Rs. 28,000 - Rs. 42,000. "
            "Direct joining letter issued. Medical fitness certificate and airport security pass fee Rs. 3,200 required prior to interview."
        ),
        "label": 1
    },
    {
        "text": (
            "Exclusive Paid Internship: Machine Learning & AI Research Intern. "
            "Stipend: Rs. 25,000/month. "
            "Candidates must first pay Rs. 4,999 for mandatory Cloud GPU server access and training kit. "
            "Payment via QR code on WhatsApp. Limited seats!"
        ),
        "label": 1
    },
    {
        "text": (
            "Dear Job Aspirant, Selected for HDFC Bank Back Office Assistant. "
            "Fixed salary Rs. 32,000 per month. Direct joining without exam. "
            "Kindly pay verification charge Rs. 1,850 to bank consultant account. Send screenshot immediately."
        ),
        "label": 1
    },

    # ==================== GENUINE SAMPLES (Label 0) ====================
    {
        "text": (
            "Dear Candidate, Thank you for interviewing with Tata Consultancy Services (TCS). "
            "We are pleased to extend an offer of employment for the role of Assistant Systems Engineer. "
            "Your annual Cost to Company (CTC) will be INR 4,20,000 as detailed in the attached annexure. "
            "Please log in to our official career portal at https://nextstep.tcs.com to view your formal offer letter and complete your onboarding documentation. "
            "Please note that TCS never charges any registration, interview, or processing fees at any stage of recruitment."
        ),
        "label": 0
    },
    {
        "text": (
            "Subject: Offer of Employment - Software Development Engineer I (SDE 1) at Amazon Development Centre India. "
            "Dear Aditya, Following your recent technical and bar raiser interviews, we are thrilled to offer you the position of SDE 1 in our Bangalore office. "
            "Your base compensation will be INR 16,00,000 per annum with standard health insurance, provident fund, and restricted stock units (RSUs). "
            "Review your offer through your Amazon Jobs portal account. Amazon will never solicit payment or fees during recruitment."
        ),
        "label": 0
    },
    {
        "text": (
            "Infosys Limited - Offer of Employment. "
            "Dear Candidate, We have pleasure in offering you the position of Specialist Programmer with Infosys. "
            "Your gross compensation will be INR 9,50,000 per annum. "
            "Your reporting location will be Infosys Mysore Campus for foundation training. "
            "Please accept the offer on our recruitment portal https://career.infosys.com using your registered candidate ID within 7 business days."
        ),
        "label": 0
    },
    {
        "text": (
            "Dear Sneha, We are delighted to invite you for the Summer Internship Program 2025 at Microsoft India R&D Pvt Ltd. "
            "Role: Software Engineering Intern. Duration: May 2025 - July 2025 (8 weeks). "
            "Monthly stipend: INR 80,000 along with relocation assistance and mentorship. "
            "Please submit your accepted digital signature through Microsoft Action Center portal. Welcome to Microsoft!"
        ),
        "label": 0
    },
    {
        "text": (
            "Zoho Corporation Recruitment Invitation. "
            "Dear Candidate, Based on your performance in the Zoho Written Aptitude and Programming assessment, "
            "you are invited for the Round 2 Advanced Coding and Technical Interview on 18th March at Zoho Estancia Campus, Guduvanchery, Chennai. "
            "Please carry your government ID and college grade sheets. Zoho does not charge any application or interview fees."
        ),
        "label": 0
    },
    {
        "text": (
            "Wipro Elite National Talent Hunt (NTH) - Letter of Intent. "
            "Dear Candidate, Congratulations on clearing our online assessment and business discussion. "
            "We are glad to offer you the role of Project Engineer at Wipro. "
            "Your compensation package is INR 3,50,004 per annum. "
            "Access your onboarding workflow via https://careers.wipro.com/elite. All onboarding requirements are completely free of charge."
        ),
        "label": 0
    },
    {
        "text": (
            "Google LLC - Full-Time Software Engineer Offer. "
            "Dear Rahul, On behalf of Google India, we are excited to offer you the position of Software Engineer, Systems. "
            "Your work location will be Google Hyderabad Campus. "
            "Details regarding base salary, equity grants, annual bonus, and 401k/EPF are outlined in the official Google Careers Candidate Portal. "
            "Sign and return your acceptance via our secure portal."
        ),
        "label": 0
    },
    {
        "text": (
            "Cognizant GenC Next Placement Offer. "
            "Dear Applicant, We are excited to inform you that you have successfully cleared the technical evaluation for GenC Next Developer. "
            "Your CTC will be INR 6,75,000 per annum. "
            "Please refer to the attached offer letter and verify all terms on Cognizant 1C recruitment portal. "
            "Cognizant strictly prohibits recruitment agencies from collecting any payment from applicants."
        ),
        "label": 0
    },
    {
        "text": (
            "அன்புள்ள விண்ணப்பதாரரே, டாட்டா கன்சல்டன்சி சர்வீசஸ் (TCS) நிறுவனத்தில் சிஸ்டம் இன்ஜினியர் பணிக்கான உங்களின் நேர்முகத் தேர்வு முடிவுகள் "
            "வெற்றிகரமாக முடிந்துள்ளன. முறையான ஆவண சரிபார்ப்புக்கு அதிகாரப்பூர்வ இணையதளத்தை https://nextstep.tcs.com அணுகவும். "
            "எங்கள் நிறுவனம் எந்தவித கட்டணமும் வசூலிப்பதில்லை என்பதை நினைவில் கொள்ளவும்."
        ),
        "label": 0
    },
    {
        "text": (
            "Accenture India - Letter of Appointment. "
            "Dear Rohit, We are pleased to offer you employment as Associate Software Engineer. "
            "Total compensation: INR 4,50,000 per annum. "
            "Please upload your educational transcripts, degree certificates, and PAN card on Accenture Workday portal. "
            "Accenture does not charge fees at any phase of our hiring cycle."
        ),
        "label": 0
    },
    {
        "text": (
            "Qualcomm India Private Limited - Internship Offer. "
            "Dear Candidate, We are pleased to offer you an internship position as Hardware Systems Engineering Intern at our Bangalore office. "
            "Stipend: INR 55,000 per month. Duration: 6 months. "
            "Your mentor and HR business partner will connect with you via Qualcomm corporate email (@qualcomm.com) prior to your joining date."
        ),
        "label": 0
    },
    {
        "text": (
            "Flipkart Internet Pvt Ltd - Frontend Engineer Offer. "
            "Dear Priyanka, Congratulations on completing your interviews for Software Development Engineer - UI. "
            "We are excited to welcome you to our Flipkart Commerce team in Bangalore. "
            "Please review and electronically sign your employment agreement in the Flipkart Greenhouse portal."
        ),
        "label": 0
    }
]
