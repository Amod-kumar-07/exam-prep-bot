import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8904219274:AAGP2PsmDw294sQXREekIpybGXcfi7qnmaE")

# ---------- KEEP ALIVE (Flask web server for Render free tier) ----------
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

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
