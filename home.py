import streamlit as st

# Add RTL CSS styling
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    /* Reverse radio button alignment */
    [data-testid=stVerticalBlock] > div > label > div {
        flex-direction: row-reverse;
        justify-content: flex-end;
    }
    
    /* Radio button label alignment */
    [data-testid=stVerticalBlock] > div > label {
        text-align: right;
        padding-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("الاختبار النهائي لمهارات الحاسب الآلي (102 تقن)")

# Instructions
st.markdown("""
## التعليمات:
- يتكون الاختبار من ثلاثة أقسام
- اقرأ الأسئلة بعناية وأجب عن جميع الأقسام
""")

# Reset button at the top-right
col1, col2, col3 = st.columns([4, 2, 2])
with col3:
    if st.button("إعادة البدء"):
        # Clear all relevant session state keys
        for key in list(st.session_state.keys()):
            if key in ['score'] or isinstance(key, int) or key.startswith('btn_'):
                del st.session_state[key]

# Initialize score in session state
if 'score' not in st.session_state:
    st.session_state.score = 0

# Questions and Answers
def main():
    total_questions = 6

    questions = [
        {
            "question": "ما هو دور نظام التشغيل في إدارة المكونات المادية والبرمجية للحاسب الآلي؟",
            "options": ["يوفر واجهة للمستخدم", "ينظم عمل البرامج التطبيقية", "يدير الموارد", "جميع ما سبق"],
            "answer": "جميع ما سبق"
        },
        {
            "question": "حدد نوع الحاسب الآلي الأنسب للتنبؤ بالأحوال الجوية.",
            "options": ["الحاسب الآلي الشخصي", "الحاسب الآلي العملاق", "الحاسب الآلي المركزي", "الحاسب المحمول"],
            "answer": "الحاسب الآلي العملاق"
        },
        {
            "question": "ما هي وظيفة وحدة التخزين الثانوية في الحاسب الآلي؟",
            "options": ["معالجة البيانات", "تخزين البيانات بشكل دائم", "تنفيذ التعليمات البرمجية", "عرض البيانات"],
            "answer": "تخزين البيانات بشكل دائم"
        },
        {
            "question": "أي من التالي يُعد مثالًا على برمجيات النظام؟",
            "options": ["Microsoft Word", "Windows 10", "Adobe Photoshop", "Google Chrome"],
            "answer": "Windows 10"
        },
        {
            "question": "ما المقصود بالشبكات المحلية (LAN)؟",
            "options": ["شبكة تربط أجهزة في مساحة جغرافية صغيرة", "شبكة تربط أجهزة عبر العالم", "شبكة تعتمد على الأقمار الصناعية", "شبكة تربط أجهزة عبر الهاتف"],
            "answer": "شبكة تربط أجهزة في مساحة جغرافية صغيرة"
        },
        {
            "question": "كيف يمكن حماية الحاسب الآلي من البرمجيات الضارة؟",
            "options": ["تثبيت برامج مكافحة الفيروسات", "تحديث نظام التشغيل بانتظام", "تجنب تنزيل البرامج من مصادر غير موثوقة", "جميع ما سبق"],
            "answer": "جميع ما سبق"
        }
    ]

    for i, q in enumerate(questions):
        st.write(f"### السؤال {i + 1}: {q['question']}")
        user_answer = st.radio("اختر الإجابة:", q["options"], key=i)
        if st.button(f"إرسال الإجابة {i + 1}", key=f"btn_{i}"):
            if user_answer == q["answer"]:
                st.success("مبروك! إجابتك صحيحة.")
                st.session_state.score += 1
            else:
                st.error(f"إجابة خاطئة. الإجابة الصحيحة هي: {q['answer']}")

    # Final Score
    if st.button("عرض النتيجة النهائية"):
        st.write(f"## نتيجتك النهائية: {st.session_state.score}/{total_questions}")

if __name__ == "__main__":
    main()
