from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8904219274:AAGP2PsmDw294sQXREekIpybGXcfi7qnmaE"

# ---------- CONTENT DATABASE ----------
CONTENT = {
    "NDA Math": {
        "Algebra": {
            "notes": (
                "📘 *Algebra*\n\n"
                "Quadratic equation: ax² + bx + c = 0\n"
                "Roots: x = (-b ± √(b²-4ac)) / 2a\n\n"
                "Discriminant D = b² - 4ac batata hai roots ka nature:\n"
                "D > 0 → 2 real roots\nD = 0 → 1 repeated root\nD < 0 → no real roots\n\n"
                "AP (Arithmetic Progression): a, a+d, a+2d...\n"
                "nth term = a + (n-1)d\n\n"
                "GP (Geometric Progression): a, ar, ar²...\n"
                "nth term = a·r^(n-1)\n\n"
                "🧠 *Trick:* Discriminant yaad rakho 'D Before Answer' — pehle D check karo, fir roots nikalo."
            ),
            "quiz": [
                {"q": "x² - 5x + 6 = 0 ke roots kya hain?", "options": ["2, 3", "1, 6", "-2, -3", "5, 6"], "answer": 0},
                {"q": "AP 3, 7, 11, 15... ka 10th term kya hoga?", "options": ["39", "40", "43", "35"], "answer": 0}
            ]
        },
        "Trigonometry": {
            "notes": (
                "📘 *Trigonometry*\n\n"
                "sin(θ) = Opposite/Hypotenuse\n"
                "cos(θ) = Adjacent/Hypotenuse\n"
                "tan(θ) = Opposite/Adjacent\n\n"
                "Important identity: sin²θ + cos²θ = 1\n\n"
                "Standard values:\n"
                "sin30°=1/2, sin45°=1/√2, sin60°=√3/2, sin90°=1\n\n"
                "🧠 *Trick:* 'Some People Have, Curly Black Hair, Turning Permanently Black' (SOH-CAH-TOA)"
            ),
            "quiz": [
                {"q": "sin(30°) ka value kya hai?", "options": ["1/2", "1", "√3/2", "0"], "answer": 0},
                {"q": "sin²θ + cos²θ ka value hamesha kya hota hai?", "options": ["1", "0", "2", "θ"], "answer": 0}
            ]
        },
        "Calculus": {
            "notes": (
                "📘 *Calculus (Differential + Integral)*\n\n"
                "Differentiation: d/dx(xⁿ) = n·xⁿ⁻¹\n"
                "d/dx(sin x) = cos x\n"
                "d/dx(cos x) = -sin x\n\n"
                "Integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n"
                "∫sin x dx = -cos x + C\n\n"
                "🧠 *Trick:* Power rule mein differentiation mein power 'ghatta' hai (n-1), integration mein power 'badhta' hai (n+1)."
            ),
            "quiz": [
                {"q": "d/dx(x³) kya hoga?", "options": ["3x²", "x²", "3x", "x³"], "answer": 0},
                {"q": "∫x dx kya hoga?", "options": ["x²/2 + C", "x + C", "2x + C", "x² + C"], "answer": 0}
            ]
        },
        "Matrices & Determinants": {
            "notes": (
                "📘 *Matrices & Determinants*\n\n"
                "2x2 matrix ka determinant: |a b; c d| = ad - bc\n\n"
                "Identity matrix (I): diagonal pe 1, baaki sab 0\n\n"
                "Matrix multiplication tabhi possible hai jab pehli matrix ke columns = doosri matrix ke rows.\n\n"
                "🧠 *Trick:* Determinant nikalne ke liye 'Cross Multiply, Minus karo' — (a×d) - (b×c)."
            ),
            "quiz": [
                {"q": "Matrix [2 3; 1 4] ka determinant kya hai?", "options": ["5", "8", "11", "-5"], "answer": 0}
            ]
        },
        "Vector Algebra": {
            "notes": (
                "📘 *Vector Algebra*\n\n"
                "Vector: magnitude + direction dono hote hain (jaise force, velocity)\n"
                "Scalar: sirf magnitude (jaise mass, speed)\n\n"
                "Dot product: a·b = |a||b|cosθ (result ek scalar hai)\n"
                "Cross product: a×b = |a||b|sinθ n̂ (result ek vector hai)\n\n"
                "🧠 *Trick:* Dot product = 'seedha number' milta hai. Cross product = 'naya vector' banta hai."
            ),
            "quiz": [
                {"q": "Dot product ka result kya hota hai?", "options": ["Scalar", "Vector", "Matrix", "Angle"], "answer": 0}
            ]
        },
        "Complex Numbers": {
            "notes": (
                "📘 *Complex Numbers*\n\n"
                "Complex number: z = a + ib, jaha i = √-1\n"
                "i² = -1, i³ = -i, i⁴ = 1 (fir cycle repeat hota hai)\n\n"
                "Modulus: |z| = √(a² + b²)\n\n"
                "🧠 *Trick:* i ki powers yaad rakho cycle mein: i, -1, -i, 1 — phir dobara repeat."
            ),
            "quiz": [
                {"q": "i² ka value kya hai?", "options": ["-1", "1", "0", "i"], "answer": 0}
            ]
        },
        "Statistics & Probability": {
            "notes": (
                "📘 *Statistics & Probability*\n\n"
                "Mean = (Sum of all values) / (Total number of values)\n"
                "Median = beech ki value jab data sorted ho\n"
                "Mode = jo value sabse zyada baar aaye\n\n"
                "Probability = (Favourable outcomes) / (Total outcomes)\n"
                "Range hamesha 0 se 1 ke beech hota hai.\n\n"
                "🧠 *Trick:* 'MMM' yaad rakho — Mean, Median, Mode teeno alag concept hain, confuse mat karo."
            ),
            "quiz": [
                {"q": "Ek sikke ko uchalne pe 'Heads' aane ki probability kya hai?", "options": ["1/2", "1", "0", "1/4"], "answer": 0}
            ]
        },
        "Analytical Geometry": {
            "notes": (
                "📘 *Analytical Geometry (2D)*\n\n"
                "Distance formula: d = √[(x2-x1)² + (y2-y1)²]\n\n"
                "Slope of line: m = (y2-y1)/(x2-x1)\n\n"
                "Circle equation: (x-h)² + (y-k)² = r² jaha (h,k) center hai, r radius hai.\n\n"
                "🧠 *Trick:* Distance formula Pythagoras theorem se hi aata hai — socho ek right triangle bana ke."
            ),
            "quiz": [
                {"q": "Points (0,0) aur (3,4) ke beech distance kya hai?", "options": ["5", "7", "4", "3"], "answer": 0}
            ]
        }
    },
    "NDA GAT": {
        "English": {
            "notes": (
                "📘 *English (Grammar + Vocabulary + Comprehension)*\n\n"
                "Common error-spotting rules:\n"
                "- Subject-Verb Agreement: singular subject → singular verb (He goes, not He go)\n"
                "- Articles: a/an consonant/vowel sound ke hisaab se, 'the' specific cheez ke liye\n"
                "- Tenses: past/present/future ka sahi use\n\n"
                "Synonym-Antonym roz 5 naye words yaad karo.\n\n"
                "🧠 *Trick:* Comprehension mein pehle questions padho, fir passage — isse time bachega aur focus sahi jagah rahega."
            ),
            "quiz": [
                {"q": "'He go to school daily' mein error kya hai?", "options": ["go should be goes", "school should be schools", "daily should be daily's", "No error"], "answer": 0},
                {"q": "'Happy' ka antonym kya hai?", "options": ["Sad", "Joyful", "Glad", "Cheerful"], "answer": 0}
            ]
        },
        "Physics": {
            "notes": (
                "📘 *Physics Basics*\n\n"
                "Newton's Laws of Motion:\n"
                "1st Law: Object rest/motion mein rahega jab tak external force na lage (Inertia)\n"
                "2nd Law: F = ma\n"
                "3rd Law: Har action ka equal-opposite reaction hota hai\n\n"
                "Units: Force → Newton, Work → Joule, Power → Watt\n\n"
                "🧠 *Trick:* F=ma yaad rakhne ke liye socho — 'Force lagega tabhi Mass Accelerate karega'."
            ),
            "quiz": [
                {"q": "F = ma mein 'a' kiske liye hai?", "options": ["Acceleration", "Area", "Angle", "Amplitude"], "answer": 0},
                {"q": "Work ka SI unit kya hai?", "options": ["Joule", "Newton", "Watt", "Pascal"], "answer": 0}
            ]
        },
        "Chemistry": {
            "notes": (
                "📘 *Chemistry Basics*\n\n"
                "Oxidation: electron lose karna (LEO — Lose Electron Oxidation)\n"
                "Reduction: electron gain karna (GER — Gain Electron Reduction)\n\n"
                "Common gases: O2 (Oxygen — combustion ke liye zaroori), CO2 (photosynthesis mein use), H2 (sabse halki gas)\n\n"
                "🧠 *Trick:* 'LEO the lion says GER' — Oxidation = Lose, Reduction = Gain."
            ),
            "quiz": [
                {"q": "Sabse halki gas kaunsi hai?", "options": ["Hydrogen", "Oxygen", "Nitrogen", "CO2"], "answer": 0}
            ]
        },
        "General Science": {
            "notes": (
                "📘 *General Science (Biology + Everyday Science)*\n\n"
                "Human body: 206 bones, heart 4 chambers wala hota hai (2 atria + 2 ventricles)\n\n"
                "Vitamins: A-eyes, C-immunity, D-bones (sunlight se milta hai), B12-blood\n\n"
                "🧠 *Trick:* Vitamin C ki kami se Scurvy hota hai — 'C se Scurvy' yaad rakho."
            ),
            "quiz": [
                {"q": "Insaan ke sharir mein kitni bones hoti hain?", "options": ["206", "196", "216", "186"], "answer": 0},
                {"q": "Vitamin D kaha se milta hai naturally?", "options": ["Sunlight", "Fruits", "Water", "Meat only"], "answer": 0}
            ]
        },
        "History": {
            "notes": (
                "📘 *History (Indian Freedom Movement + Culture)*\n\n"
                "1857 Revolt — pehla swatantrata sangram, Mangal Pandey se shuru hua\n"
                "1885 — Indian National Congress ki sthapna\n"
                "1942 — Quit India Movement\n"
                "1947 — Independence\n\n"
                "🧠 *Trick:* Important dates ek timeline banake yaad karo — 1857 → 1885 → 1942 → 1947."
            ),
            "quiz": [
                {"q": "Indian National Congress kab bani thi?", "options": ["1885", "1857", "1905", "1947"], "answer": 0}
            ]
        },
        "Geography": {
            "notes": (
                "📘 *Geography (Physical + Indian)*\n\n"
                "Earth ki layers: Crust (upar), Mantle (beech), Core (sabse andar)\n\n"
                "India ki longest river: Ganga\n"
                "Highest peak: Kanchenjunga (India mein), Everest (world mein, Nepal border)\n\n"
                "🧠 *Trick:* Earth layers yaad rakho 'CMC' — Crust, Mantle, Core (bahar se andar)."
            ),
            "quiz": [
                {"q": "India ki sabse lambi nadi kaunsi hai?", "options": ["Ganga", "Yamuna", "Godavari", "Brahmaputra"], "answer": 0}
            ]
        },
        "Current Affairs": {
            "notes": (
                "📘 *Current Affairs — Kaise Prepare Karein*\n\n"
                "⚠️ Ye section roz update hota hai, isliye bot mein fixed events nahi de sakte — purane ho jayenge.\n\n"
                "Kya follow karo:\n"
                "1. Roz ek newspaper padho (The Hindu / Indian Express)\n"
                "2. Sports, Defence news, Government schemes pe special focus rakho\n"
                "3. Monthly current affairs PDF/app use karo (jaise Vision IAS, Drishti)\n"
                "4. Important awards, appointments, summits note karte raho\n\n"
                "🧠 *Trick:* Ek notebook banao — 'is week ke 5 important events' likhte raho, revise karte raho."
            ),
            "quiz": [
                {"q": "Current Affairs ke liye sabse acha daily habit kya hai?", "options": ["Roz newspaper padhna", "Sirf exam se pehle padhna", "Kabhi na padhna", "Sirf sports dekhna"], "answer": 0}
            ]
        }
    },
    "Pharmacy": {
        "Pharmacokinetics": {
            "notes": (
                "📘 *Pharmacokinetics*\n\n"
                "Drug body mein 4 stages se guzarta hai: ADME\n"
                "A - Absorption\nD - Distribution\nM - Metabolism\nE - Excretion\n\n"
                "🧠 *Trick:* 'A Dog Must Eat' (ADME)"
            ),
            "quiz": [
                {"q": "ADME mein 'M' kiske liye hai?", "options": ["Metabolism", "Movement", "Mixing", "Measurement"], "answer": 0}
            ]
        }
    }
}

# ---------- HANDLERS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(sub, callback_data=f"SUB|{sub}")] for sub in CONTENT]
    await update.message.reply_text(
        "📚 Namaste! Main tumhara Exam Prep Bot hoon.\nSubject choose karo:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("|")

    if data[0] == "SUB":
        subject = data[1]
        topics = CONTENT[subject]
        keyboard = [[InlineKeyboardButton(t, callback_data=f"TOPIC|{subject}|{t}")] for t in topics]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="HOME")])
        await query.edit_message_text(f"📖 {subject} — Topic choose karo:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "TOPIC":
        subject, topic = data[1], data[2]
        keyboard = [
            [InlineKeyboardButton("📝 Notes padho", callback_data=f"NOTES|{subject}|{topic}")],
            [InlineKeyboardButton("❓ Quiz do", callback_data=f"QUIZ|{subject}|{topic}|0")],
            [InlineKeyboardButton("⬅️ Back", callback_data=f"SUB|{subject}")]
        ]
        await query.edit_message_text(f"📌 {topic}\n\nKya karna hai?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "NOTES":
        subject, topic = data[1], data[2]
        notes = CONTENT[subject][topic]["notes"]
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data=f"TOPIC|{subject}|{topic}")]]
        await query.edit_message_text(notes, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data[0] == "QUIZ":
        subject, topic, qnum = data[1], data[2], int(data[3])
        quiz_list = CONTENT[subject][topic]["quiz"]
        q = quiz_list[qnum]
        keyboard = [
            [InlineKeyboardButton(opt, callback_data=f"ANS|{subject}|{topic}|{qnum}|{i}")]
            for i, opt in enumerate(q["options"])
        ]
        await query.edit_message_text(f"❓ {q['q']}", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "ANS":
        subject, topic, qnum, chosen = data[1], data[2], int(data[3]), int(data[4])
        quiz_list = CONTENT[subject][topic]["quiz"]
        q = quiz_list[qnum]
        correct = q["answer"]
        if chosen == correct:
            result = "✅ Sahi jawab!\n\n"
        else:
            result = f"❌ Galat. Sahi jawab tha: {q['options'][correct]}\n\n"

        next_q = qnum + 1
        keyboard = []
        if next_q < len(quiz_list):
            keyboard.append([InlineKeyboardButton("➡️ Next Question", callback_data=f"QUIZ|{subject}|{topic}|{next_q}")])
        keyboard.append([InlineKeyboardButton("⬅️ Topic pe wapas", callback_data=f"TOPIC|{subject}|{topic}")])
        await query.edit_message_text(result, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "HOME":
        keyboard = [[InlineKeyboardButton(sub, callback_data=f"SUB|{sub}")] for sub in CONTENT]
        await query.edit_message_text("📚 Subject choose karo:", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot chalu ho gaya... Ctrl+C se rokna")
    app.run_polling()

if __name__ == "__main__":
    main()
