import streamlit as st
import copy

# إعدادات واجهة الموقع لتكون متناسقة وشيك
st.set_page_config(page_title="مستشار الألعاب الذكي", page_icon="🧠", layout="centered")

st.markdown("<h1 style='text-align: center; color: #b5823c;'>🧠 مستشار دمج الحيوانات الذكي 👑</h1>", unsafe_allow_html=True)
st.write("أهلاً بك يا بطل! اكتب أرقام الحيوانات في الرقعة (4×4) لحساب أفضل نقلة بخوارزمية Expectimax الحقيقية:")

# =========================================================
# 🧠 منطق الذكاء الاصطناعي والمحاكاة الأصلي بتاعك (Expectimax)
# =========================================================
SCORE_MATRIX = [
    [0,   2,   4,   8],
    [128, 64,  32,  16],
    [256, 512, 1024,2048],
    [32768,16384,8192,4096]
]

def merge_line(line, reverse=False):
    non_zeros = [x for x in line if x != 0]
    if reverse:
        non_zeros.reverse()
    new_line = []
    merges = 0
    highest = 0
    i = 0
    while i < len(non_zeros):
        if i + 1 < len(non_zeros) and non_zeros[i] == non_zeros[i+1]:
            combined = non_zeros[i] + 1
            new_line.append(combined)
            merges += 1
            highest = max(highest, combined)
            i += 2
        else:
            new_line.append(non_zeros[i])
            i += 1
    while len(new_line) < 4:
        new_line.append(0)
    if reverse:
        new_line.reverse()
    return new_line, merges, highest

def simulate_move(board, direction):
    sim_board = [row[:] for row in board]
    merges = 0
    highest_merge = 0
    for i in range(4):
        if direction in ['LEFT', 'RIGHT']:
            line = sim_board[i]
            new_line, m_count, h_level = merge_line(line, direction == 'RIGHT')
            sim_board[i] = new_line
            merges += m_count
            highest_merge = max(highest_merge, h_level)
        else:
            line = [sim_board[j][i] for j in range(4)]
            new_line, m_count, h_level = merge_line(line, direction == 'DOWN')
            for j in range(4):
                sim_board[j][i] = new_line[j]
            merges += m_count
            highest_merge = max(highest_merge, h_level)
    return sim_board, merges, highest_merge

def board_changed(b1, b2):
    for r in range(4):
        for c in range(4):
            if b1[r][c] != b2[r][c]:
                return True
    return False

def evaluate_board(board):
    score = 0
    empty_cells = 0
    for r in range(4):
        for c in range(4):
            val = board[r][c]
            if val == 0:
                empty_cells += 1
            else:
                score += val * SCORE_MATRIX[r][c]
    score += empty_cells * 50
    return score

def expectimax(board, depth, is_player_turn):
    if depth == 0:
        return evaluate_board(board)
    if is_player_turn:
        max_score = -float('inf')
        for direction in ['RIGHT', 'DOWN', 'UP', 'LEFT']:
            sim_board, _, _ = simulate_move(board, direction)
            if board_changed(board, sim_board):
                score = expectimax(sim_board, depth - 1, False)
                if score > max_score:
                    max_score = score
        return max_score if max_score != -float('inf') else evaluate_board(board)
    else:
        scores = []
        for r in range(4):
            for c in range(4):
                if board[r][c] == 0:
                    test_board = [row[:] for row in board]
                    test_board[r][c] = 1
                    scores.append(expectimax(test_board, depth - 1, True))
        return sum(scores) / len(scores) if scores else evaluate_board(board)

def calculate_best_move(board):
    best_move = None
    max_score = -float('inf')
    
    if all(sum(row) == 0 for row in board):
        return None

    directions = ['RIGHT', 'DOWN', 'LEFT', 'UP']
    
    for direction in directions:
        sim_board, merges_count, highest_level = simulate_move(board, direction)
        if not board_changed(board, sim_board):
            continue
        expected_score = expectimax(sim_board, 3, False)
        expected_score += merges_count * 50 + highest_level * 30
        if expected_score > max_score:
            max_score = expected_score
            best_move = direction
            
    return best_move

# =========================================================
# 🖥️ واجهة المستخدم على المتصفح (Streamlit UI)
# =========================================================

# بناء الرقعة الـ 4x4 لإدخال الأرقام في الموقع
board = []
for r in range(4):
    cols = st.columns(4)
    row_inputs = []
    for c in range(4):
        val = cols[c].number_input(
            f"R{r}C{c}", 
            min_value=0, 
            max_value=32768, 
            value=0, 
            step=1,
            key=f"cell_{r}_{c}", 
            label_visibility="collapsed"
        )
        row_inputs.append(val)
    board.append(row_inputs)

st.markdown("---")

# زر الحساب الرئيسي للموقع
if st.button("🔍 احسب أفضل نقلة الآن", use_container_width=True):
    best_move = calculate_best_move(board)
    
    if best_move:
        ar_moves = {'RIGHT': 'يمين ➡️', 'DOWN': 'تحت ⬇️', 'LEFT': 'شمال ⬅️', 'UP': 'فوق ⬆️'}
        st.success(f"💡 مستشارك الذكي يقول: أفضل حركة تلعبها دلوقتي هي: **[ {ar_moves[best_move]} ]** ✨")
    else:
        st.warning("⚠️ اكتب أرقام الحيوانات في المربعات أولاً عشان أحسبلك، أو مفيش حركات متاحة حالياً!")