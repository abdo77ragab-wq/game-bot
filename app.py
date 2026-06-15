import streamlit as st
import copy

# إعدادات الصفحة
st.set_page_config(page_title="مستشار الألعاب الذكي", page_icon="🎮", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎮 مستشار الدمج الذكي 👑</h1>", unsafe_allow_html=True)
st.write("أهلاً بك يا بطل! اكتب أرقام الحيوانات في الرقعة (4×4) عشان تحسب أفضل نقلة حقيقية:")

# --- منطق اللعبة الحقيقي وعمليات الدمج ---

def compress(grid):
    changed = False
    new_grid = [[0]*4 for _ in range(4)]
    for r in range(4):
        pos = 0
        for c in range(4):
            if grid[r][c] != 0:
                new_grid[r][pos] = grid[r][c]
                if pos != c:
                    changed = True
                pos += 1
    return new_grid, changed

def merge(grid):
    changed = False
    score = 0
    for r in range(4):
        for c in range(3):
            if grid[r][c] == grid[r][c+1] and grid[r][c] != 0:
                grid[r][c] *= 2
                score += grid[r][c]
                grid[r][c+1] = 0
                changed = True
    return grid, changed, score

def reverse(grid):
    new_grid = []
    for r in range(4):
        new_grid.append(grid[r][::-1])
    return new_grid

def transpose(grid):
    new_grid = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            new_grid[r][c] = grid[c][r]
    return new_grid

# دالة محاكاة الحركة وحساب النقط والصلاحية
def move_left(grid):
    stage1, change1 = compress(grid)
    stage2, change2, score = merge(stage1)
    stage3, change3 = compress(stage2)
    return stage3, (change1 or change2 or change3), score

def move_right(grid):
    rev = reverse(grid)
    res, changed, score = move_left(rev)
    return reverse(res), changed, score

def move_up(grid):
    trans = transpose(grid)
    res, changed, score = move_left(trans)
    return transpose(res), changed, score

def move_down(grid):
    trans = transpose(grid)
    res, changed, score = move_right(trans)
    return transpose(res), changed, score

# دالة اختيار الحركة الأفضل
def calculate_best_move(board):
    moves = {
        'LEFT': move_left(board),
        'RIGHT': move_right(board),
        'UP': move_up(board),
        'DOWN': move_down(board)
    }
    
    best_move = None
    max_score = -1
    
    # الترتيب المفضل في حالة تساوي النقط (مثلاً يفضل اليمين أو التحت لتثبيت الحيوانات الكبيرة)
    preferred_order = ['DOWN', 'RIGHT', 'LEFT', 'UP']
    
    for move in preferred_order:
        grid_res, is_valid, score = moves[move]
        if is_valid: # لو الحركة مسموحة وليها تأثير في الرقعة
            if score > max_score:
                max_score = score
                best_move = move
            elif best_move is None:
                best_move = move
                
    return best_move

# --- تصميم واجهة المستخدم ---

board = []
for r in range(4):
    cols = st.columns(4)
    row_inputs = []
    for c in range(4):
        val = cols[c].number_input(
            f"صف {r+1} - عمود {c+1}", 
            min_value=0, 
            max_value=2048, 
            value=0, 
            step=1,
            key=f"{r}_{c}", 
            label_visibility="collapsed"
        )
        row_inputs.append(val)
    board.append(row_inputs)

st.markdown("---")

if st.button("🚀 احسب أفضل نقلة الآن", use_container_width=True):
    # التأكد إن الرقعة مش فاضية تماماً
    total_sum = sum(sum(row) for row in board)
    if total_sum == 0:
        st.warning("⚠️ الرقعة فاضية تماماً يا بطل! حط أرقام الحيوانات الأول.")
    else:
        best_move = calculate_best_move(board)
        ar_moves = {'RIGHT': 'يمين ➡️', 'DOWN': 'تحت ⬇️', 'LEFT': 'شمال ⬅️', 'UP': 'فوق ⬆️'}
        
        if best_move:
            st.success(f"💡 أفضل حركة تلعبها دلوقتي هي: **{ar_moves[best_move]}**")
        else:
            st.error("😭 مفيش أي حركة متاحة! الجيم كدة قفل (Game Over).")