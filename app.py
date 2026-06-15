import streamlit as st

# إعدادات الصفحة وشكلها على الموبايل
st.set_page_config(page_title="مستشار الألعاب الذكي", page_icon="🎮", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎮 مستشار الدمج الذكي 👑</h1>", unsafe_allow_html=True)
st.write("أهلاً بك يا بطل! اكتب أرقام الحيوانات في الرقعة (4×4) عشان تحسب أفضل نقلة:")

# دالة حساب النقلة (نفس الخوارزمية بتاعتك)
def calculate_best_move(board):
    return "RIGHT"  # كمثال مؤقت

# إنشاء رقعة الـ 4×4 على الموقع
board = []
for r in range(4):
    cols = st.columns(4)
    row_inputs = []
    for c in range(4):
        val = cols[c].number_input(f"صف {r+1} - عمود {c+1}", min_value=0, max_value=11, value=0, key=f"{r}_{c}", label_visibility="collapsed")
        row_inputs.append(val)
    board.append(row_inputs)

st.markdown("---")

# زرار الحساب
if st.button("🚀 احسب أفضل نقلة الآن", use_container_width=True):
    best_move = calculate_best_move(board)
    ar_moves = {'RIGHT': 'يمين ➡️', 'DOWN': 'تحت ⬇️', 'LEFT': 'شمال ⬅️', 'UP': 'فوق ⬆️'}
    st.success(f"💡 أفضل حركة تلعبها دلوقتي هي: **{ar_moves[best_move]}**")