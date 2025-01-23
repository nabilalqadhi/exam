import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# RTL CSS styling
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    [data-testid=stVerticalBlock] > div > label > div {
        flex-direction: row-reverse;
        justify-content: flex-end;
    }
    [data-testid=stVerticalBlock] > div > label {
        padding-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Email configuration (Update with your email settings)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"

# User credentials (In real application, use proper database)
USERS = {
    "student1": {"password": "pass123", "role": "student", "email": "student1@example.com"},
    "teacher1": {"password": "teach456", "role": "teacher", "email": "teacher@example.com"}
}

def send_email(recipient, subject, content):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(content, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"فشل إرسال البريد الإلكتروني: {str(e)}")
        return False

def login_page():
    """User login interface"""
    st.title("نظام الاختبارات الإلكترونية")
    
    with st.form("login_form"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        submit = st.form_submit_button("تسجيل الدخول")
        
        if submit:
            if username in USERS and USERS[username]['password'] == password:
                st.session_state.logged_in = True
                st.session_state.user_info = USERS[username]
                st.session_state.user_info['username'] = username
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")

def generate_report(score, total, questions):
    """Generate exam report content"""
    report = f"النتيجة النهائية: {score}/{total}\n\n"
    report += "تفاصيل الإجابات:\n"
    for i, q in enumerate(questions):
        report += f"\nالسؤال {i+1}: {q['question']}\n"
        report += f"- الإجابة الصحيحة: {q['answer']}\n"
        if i in st.session_state:
            report += f"- إجابتك: {st.session_state[i]}\n"
    return report

def exam_page():
    """Main exam interface"""
    st.title("الاختبار النهائي لمهارات الحاسب الآلي (102 تقن)")
    
    # Reset button
    if st.button("إعادة البدء"):
        for key in list(st.session_state.keys()):
            if key in ['score'] or isinstance(key, int) or key.startswith('btn_'):
                del st.session_state[key]
    
    # Initialize exam
    if 'score' not in st.session_state:
        st.session_state.score = 0
    
    questions = [
        # ... (same questions as previous version)
    ]

    # Display questions
    for i, q in enumerate(questions):
        st.write(f"### السؤال {i + 1}: {q['question']}")
        user_answer = st.radio("اختر الإجابة:", q["options"], key=i)
        if st.button(f"إرسال الإجابة {i + 1}", key=f"btn_{i}"):
            if user_answer == q["answer"]:
                st.success("مبروك! إجابتك صحيحة.")
                st.session_state.score += 1
            else:
                st.error(f"إجابة خاطئة. الإجابة الصحيحة هي: {q['answer']}")

    # Final submission
    if st.button("إنهاء الاختبار وإرسال النتائج"):
        report_content = generate_report(st.session_state.score, len(questions), questions)
        
        # Send to student
        student_email = st.session_state.user_info['email']
        if send_email(student_email, "نتيجة الاختبار", report_content):
            st.success("تم إرسال النتيجة إلى بريدك الإلكتروني")
        
        # Send to all teachers
        for user in USERS.values():
            if user['role'] == 'teacher':
                teacher_email = user['email']
                send_email(teacher_email, f"نتيجة الطالب {st.session_state.user_info['username']}", report_content)
        
        # Store results (In real application, use database)
        if 'results' not in st.session_state:
            st.session_state.results = {}
        st.session_state.results[st.session_state.user_info['username']] = {
            'score': st.session_state.score,
            'total': len(questions)
        }

def teacher_dashboard():
    """Teacher's results dashboard"""
    st.title("لوحة المدرس")
    
    if 'results' in st.session_state:
        st.subheader("النتائج المطلعة:")
        for username, result in st.session_state.results.items():
            st.write(f"الطالب: {username} - النتيجة: {result['score']}/{result['total']}")
    else:
        st.write("لا توجد نتائج متاحة حتى الآن")

def main():
    """Main app controller"""
    if not st.session_state.get('logged_in'):
        login_page()
    else:
        if st.session_state.user_info['role'] == 'student':
            exam_page()
        else:
            teacher_dashboard()

if __name__ == "__main__":
    main()
