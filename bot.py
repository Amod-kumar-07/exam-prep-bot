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

# ---------- DEEP NOTES: Algebra ----------
ALGEBRA_NOTES = """ALGEBRA - Poora Chapter

=== 1. LINEAR EQUATIONS ===
Ek variable wali equation: ax + b = 0
Solution: x = -b/a

Do variable wali equations (simultaneous):
a1x + b1y = c1
a2x + b2y = c2
Solve karne ke 3 tarike: Substitution, Elimination, Cross-multiplication.

=== 2. QUADRATIC EQUATIONS ===
Standard form: ax^2 + bx + c = 0 (a != 0)

Roots nikalne ka formula:
x = (-b +- sqrt(b^2 - 4ac)) / 2a

DISCRIMINANT (D = b^2 - 4ac) - ye roots ka "nature" batata hai:
- D > 0 -> 2 real aur alag roots
- D = 0 -> 1 repeated real root (dono roots barabar)
- D < 0 -> koi real root nahi (roots complex/imaginary hote hain)

Sum aur Product of roots (bina roots nikale hi pata chal jata hai):
- Sum of roots = -b/a
- Product of roots = c/a
Ye trick exam mein bahut kaam aati hai jab sirf sum/product poocha jaye.

Factorization method: agar ax^2+bx+c ko (x-p)(x-q) form mein tod saken, to p aur q hi roots hain.
Example: x^2 - 5x + 6 = 0 -> (x-2)(x-3) = 0 -> roots: 2, 3

=== 3. ARITHMETIC PROGRESSION (AP) ===
Sequence jisme consecutive terms ka difference constant ho ("common difference" d).
Series: a, a+d, a+2d, a+3d, ...

nth term: an = a + (n-1)d
Sum of first n terms: Sn = n/2 * [2a + (n-1)d]  ya  Sn = n/2 * (first term + last term)

Identify karna: agar terms ke beech ka farak (difference) hamesha same ho, to wo AP hai.
Example: 3, 7, 11, 15... yaha d = 4 hai.

=== 4. GEOMETRIC PROGRESSION (GP) ===
Sequence jisme consecutive terms ka ratio constant ho ("common ratio" r).
Series: a, ar, ar^2, ar^3, ...

nth term: an = a * r^(n-1)
Sum of first n terms (r != 1): Sn = a(r^n - 1)/(r-1)
Sum of infinite GP (jab |r| < 1): S(infinity) = a/(1-r)

Identify karna: agar consecutive terms ka ratio hamesha same ho, to wo GP hai.
Example: 5, 10, 20, 40... yaha r = 2 hai.

=== 5. COMMON MISTAKES (exam mein log yaha galti karte hain) ===
1. Discriminant ka sign galat le lena - hamesha D = b^2 - 4ac yaad rakho, b^2 - 4ca nahi.
2. AP aur GP confuse kar dena - AP mein DIFFERENCE constant, GP mein RATIO constant hota hai.
3. Sum of roots formula mein sign bhool jana - ye -b/a hai, b/a nahi.
4. nth term formula mein (n-1) ki jagah n likh dena - ye sabse common mistake hai.

Trick (yaad rakhne ke liye): 'D Before Answer' - roots nikalne se pehle hamesha Discriminant check karo, isse pata chal jayega real roots milenge ya nahi, time bachega."""

# ---------- CONTENT DATABASE ----------
CONTENT = {
    "NDA Math": {
        "Algebra": {
            "notes": ALGEBRA_NOTES,
            "quiz": [
            {"q": 'x^2 + 15x + 54 = 0 ke roots kya hain?', "options": ['-10, -7', '-9, -6', '-11, -8', '-10, -5'], "answer": 1},
            {"q": 'x^2 + 10x + 21 = 0 ke roots kya hain?', "options": ['-8, -1', '-6, -5', '-7, -3', '-8, -5'], "answer": 2},
            {"q": 'x^2 + 0x - 1 = 0 ke roots kya hain?', "options": ['-3, -1', '-2, 2', '-1, 1', '-3, 2'], "answer": 2},
            {"q": 'x^2 + 8x + 12 = 0 ke roots kya hain?', "options": ['-5, -3', '-6, -2', '-8, -1', '-7, -1'], "answer": 1},
            {"q": 'x^2 - 1x - 20 = 0 ke roots kya hain?', "options": ['-6, 4', '-2, 6', '-5, 6', '-4, 5'], "answer": 3},
            {"q": 'x^2 + 8x + 7 = 0 ke roots kya hain?', "options": ['-5, 1', '-6, -2', '-5, -2', '-7, -1'], "answer": 3},
            {"q": 'x^2 - 6x - 16 = 0 ke roots kya hain?', "options": ['-2, 8', '-1, 10', '-3, 7', '-4, 6'], "answer": 0},
            {"q": 'x^2 + 3x - 28 = 0 ke roots kya hain?', "options": ['-7, 4', '-9, 2', '-6, 6', '-5, 6'], "answer": 0},
            {"q": 'x^2 + 0x - 16 = 0 ke roots kya hain?', "options": ['-4, 4', '-5, 5', '-6, 6', '-3, 2'], "answer": 0},
            {"q": 'x^2 - 4x - 32 = 0 ke roots kya hain?', "options": ['-3, 7', '-2, 6', '-4, 8', '-6, 9'], "answer": 2},
            {"q": 'x^2 + 1x - 42 = 0 ke roots kya hain?', "options": ['-9, 5', '-7, 6', '-8, 7', '-8, 8'], "answer": 1},
            {"q": 'x^2 - 7x + 10 = 0 ke roots kya hain?', "options": ['2, 5', '1, 4', '1, 3', '3, 4'], "answer": 0},
            {"q": 'x^2 + 9x + 14 = 0 ke roots kya hain?', "options": ['-6, -4', '-7, -2', '-5, -1', '-8, -4'], "answer": 1},
            {"q": 'x^2 - 4x - 12 = 0 ke roots kya hain?', "options": ['-4, 7', '-4, 4', '-4, 5', '-2, 6'], "answer": 3},
            {"q": 'x^2 - 13x + 40 = 0 ke roots kya hain?', "options": ['4, 10', '7, 7', '6, 7', '5, 8'], "answer": 3},
            {"q": 'x^2 + 0x - 64 = 0 ke roots kya hain?', "options": ['-9, 7', '-8, 8', '-10, 6', '-6, 10'], "answer": 1},
            {"q": 'x^2 + 12x + 32 = 0 ke roots kya hain?', "options": ['-6, -2', '-8, -4', '-6, -3', '-6, -6'], "answer": 1},
            {"q": 'x^2 + 11x + 24 = 0 ke roots kya hain?', "options": ['-8, -3', '-10, -5', '-9, -1', '-7, -5'], "answer": 0},
            {"q": 'x^2 + 11x + 28 = 0 ke roots kya hain?', "options": ['-8, -6', '-9, -2', '-7, -4', '-9, -5'], "answer": 2},
            {"q": 'x^2 + 4x + 3 = 0 ke roots kya hain?', "options": ['-5, -3', '-2, 1', '-3, -1', '-2, -2'], "answer": 2},
            {"q": 'x^2 - 1x - 56 = 0 ke roots kya hain?', "options": ['-6, 9', '-8, 9', '-7, 8', '-9, 7'], "answer": 2},
            {"q": 'x^2 + 2x - 63 = 0 ke roots kya hain?', "options": ['-8, 6', '-9, 7', '-11, 5', '-11, 8'], "answer": 1},
            {"q": 'x^2 + 2x - 3 = 0 ke roots kya hain?', "options": ['-4, 2', '-5, -1', '-1, 2', '-3, 1'], "answer": 3},
            {"q": 'x^2 + 8x - 9 = 0 ke roots kya hain?', "options": ['-10, 3', '-9, 1', '-10, 2', '-7, -1'], "answer": 1},
            {"q": 'x^2 - 11x + 18 = 0 ke roots kya hain?', "options": ['3, 10', '2, 9', '1, 7', '1, 11'], "answer": 1},
            {"q": '2x^2 - 7x + 1 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '5x^2 + 3x + 9 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 2},
            {"q": '2x^2 - 3x - 5 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '2x^2 + 3x - 10 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '2x^2 + 0x + 3 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 2},
            {"q": '2x^2 - 2x - 5 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '1x^2 + 2x - 9 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '4x^2 - 3x - 4 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '4x^2 + 1x - 1 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '2x^2 - 3x - 10 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '2x^2 + 2x + 0 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '3x^2 - 8x - 2 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '3x^2 + 10x + 6 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '4x^2 + 7x + 0 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '1x^2 - 7x - 2 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '2x^2 + 8x - 2 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '1x^2 - 7x + 9 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '4x^2 + 1x + 0 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '4x^2 + 9x + 6 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 2},
            {"q": '1x^2 + 2x + 8 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 2},
            {"q": '2x^2 - 2x - 9 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '4x^2 - 10x + 6 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '5x^2 - 4x + 1 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 2},
            {"q": '4x^2 - 8x + 0 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": '5x^2 + 0x - 7 = 0 ka discriminant check karo - roots ka nature kya hoga?', "options": ['2 real aur alag roots', '1 repeated real root', 'Koi real root nahi', 'Anant roots'], "answer": 0},
            {"q": 'AP 12, 16, 20... ka 14th term kya hoga?', "options": ['64', '56', '66', '62'], "answer": 0},
            {"q": 'AP 11, 16, 21... ka 8th term kya hoga?', "options": ['48', '36', '44', '46'], "answer": 3},
            {"q": 'AP 4, 9, 14... ka 15th term kya hoga?', "options": ['64', '76', '74', '72'], "answer": 2},
            {"q": 'AP 9, 14, 19... ka 8th term kya hoga?', "options": ['44', '34', '39', '42'], "answer": 0},
            {"q": 'AP 11, 15, 19... ka 9th term kya hoga?', "options": ['47', '45', '43', '39'], "answer": 2},
            {"q": 'AP 15, 22, 29... ka 15th term kya hoga?', "options": ['113', '120', '106', '115'], "answer": 0},
            {"q": 'AP 3, 11, 19... ka 14th term kya hoga?', "options": ['105', '107', '109', '99'], "answer": 1},
            {"q": 'AP 3, 11, 19... ka 13th term kya hoga?', "options": ['83', '97', '101', '99'], "answer": 3},
            {"q": 'AP 15, 18, 21... ka 13th term kya hoga?', "options": ['53', '51', '54', '45'], "answer": 1},
            {"q": 'AP 11, 14, 17... ka 10th term kya hoga?', "options": ['40', '38', '32', '35'], "answer": 1},
            {"q": 'AP 6, 12, 18... ka 7th term kya hoga?', "options": ['44', '42', '36', '48'], "answer": 1},
            {"q": 'AP 9, 14, 19... ka 12th term kya hoga?', "options": ['59', '69', '66', '64'], "answer": 3},
            {"q": 'AP 14, 22, 30... ka 15th term kya hoga?', "options": ['110', '118', '128', '126'], "answer": 3},
            {"q": 'AP 9, 16, 23... ka 14th term kya hoga?', "options": ['98', '100', '107', '102'], "answer": 1},
            {"q": 'AP 8, 10, 12... ka 12th term kya hoga?', "options": ['30', '32', '26', '28'], "answer": 0},
            {"q": 'AP 2, 9, 16... ka 12th term kya hoga?', "options": ['79', '86', '72', '81'], "answer": 0},
            {"q": 'AP 4, 9, 14... ka 11th term kya hoga?', "options": ['44', '49', '54', '56'], "answer": 2},
            {"q": 'AP 6, 9, 12... ka 7th term kya hoga?', "options": ['24', '27', '22', '21'], "answer": 0},
            {"q": 'AP 8, 15, 22... ka 7th term kya hoga?', "options": ['48', '52', '57', '50'], "answer": 3},
            {"q": 'AP 10, 16, 22... ka 7th term kya hoga?', "options": ['40', '52', '34', '46'], "answer": 3},
            {"q": 'AP 7, 14, 21... ka 9th term kya hoga?', "options": ['63', '56', '70', '61'], "answer": 0},
            {"q": 'AP 14, 21, 28... ka 15th term kya hoga?', "options": ['110', '98', '105', '112'], "answer": 3},
            {"q": 'AP 2, 8, 14... ka 11th term kya hoga?', "options": ['50', '62', '64', '56'], "answer": 1},
            {"q": 'AP 7, 10, 13... ka 14th term kya hoga?', "options": ['46', '40', '44', '48'], "answer": 0},
            {"q": 'AP 6, 14, 22... ka 9th term kya hoga?', "options": ['70', '72', '54', '62'], "answer": 0},
            {"q": 'GP 3, 6, 12... ka 6th term kya hoga?', "options": ['98', '96', '93', '102'], "answer": 1},
            {"q": 'GP 3, 9, 27... ka 5th term kya hoga?', "options": ['249', '243', '246', '240'], "answer": 1},
            {"q": 'GP 4, 16, 64... ka 6th term kya hoga?', "options": ['4092', '4096', '4100', '4104'], "answer": 1},
            {"q": 'GP 3, 12, 48... ka 5th term kya hoga?', "options": ['768', '765', '772', '774'], "answer": 0},
            {"q": 'GP 3, 6, 12... ka 4th term kya hoga?', "options": ['30', '24', '26', '21'], "answer": 1},
            {"q": 'GP 3, 6, 12... ka 5th term kya hoga?', "options": ['45', '46', '48', '50'], "answer": 2},
            {"q": 'GP 1, 4, 16... ka 5th term kya hoga?', "options": ['256', '252', '260', '258'], "answer": 0},
            {"q": 'GP 4, 12, 36... ka 6th term kya hoga?', "options": ['968', '969', '972', '975'], "answer": 2},
            {"q": 'GP 1, 3, 9... ka 6th term kya hoga?', "options": ['246', '240', '242', '243'], "answer": 3},
            {"q": 'GP 5, 15, 45... ka 4th term kya hoga?', "options": ['130', '132', '145', '135'], "answer": 3},
            {"q": 'GP 3, 12, 48... ka 3rd term kya hoga?', "options": ['54', '44', '52', '48'], "answer": 3},
            {"q": 'GP 4, 8, 16... ka 4th term kya hoga?', "options": ['34', '32', '40', '28'], "answer": 1},
            {"q": 'GP 2, 6, 18... ka 4th term kya hoga?', "options": ['52', '54', '51', '57'], "answer": 1},
            {"q": 'GP 4, 16, 64... ka 5th term kya hoga?', "options": ['1032', '1020', '1028', '1024'], "answer": 3},
            {"q": 'GP 5, 10, 20... ka 4th term kya hoga?', "options": ['50', '35', '42', '40'], "answer": 3},
            {"q": 'GP 1, 3, 9... ka 5th term kya hoga?', "options": ['83', '78', '81', '80'], "answer": 2},
            {"q": 'GP 5, 10, 20... ka 6th term kya hoga?', "options": ['158', '160', '155', '170'], "answer": 1},
            {"q": 'GP 5, 15, 45... ka 6th term kya hoga?', "options": ['1212', '1215', '1225', '1218'], "answer": 1},
            {"q": 'GP 3, 9, 27... ka 6th term kya hoga?', "options": ['729', '726', '732', '735'], "answer": 0},
            {"q": 'GP 5, 20, 80... ka 5th term kya hoga?', "options": ['1284', '1280', '1290', '1276'], "answer": 1},
            {"q": 'GP 5, 15, 45... ka 3rd term kya hoga?', "options": ['45', '55', '40', '48'], "answer": 0},
            {"q": 'GP 4, 12, 36... ka 4th term kya hoga?', "options": ['111', '105', '116', '108'], "answer": 3},
            {"q": 'GP 1, 3, 9... ka 3rd term kya hoga?', "options": ['11', '6', '9', '12'], "answer": 2},
            {"q": 'GP 3, 12, 48... ka 6th term kya hoga?', "options": ['3078', '3069', '3072', '3068'], "answer": 2},
            {"q": 'GP 5, 10, 20... ka 3rd term kya hoga?', "options": ['20', '22', '15', '18'], "answer": 0},
            ]
        },
        "Trigonometry": {
            "notes": (
                "Trigonometry\n\n"
                "sin(theta) = Opposite/Hypotenuse\n"
                "cos(theta) = Adjacent/Hypotenuse\n"
                "tan(theta) = Opposite/Adjacent\n\n"
                "Important identity: sin^2(theta) + cos^2(theta) = 1\n\n"
                "Standard values:\n"
                "sin30=1/2, sin45=1/sqrt2, sin60=sqrt3/2, sin90=1\n\n"
                "Trick: 'Some People Have, Curly Black Hair, Turning Permanently Black' (SOH-CAH-TOA)"
            ),
            "quiz": [
                {"q": "sin(30 deg) ka value kya hai?", "options": ["1/2", "1", "sqrt3/2", "0"], "answer": 0},
                {"q": "sin^2 + cos^2 ka value hamesha kya hota hai?", "options": ["1", "0", "2", "theta"], "answer": 0}
            ]
        },
        "Calculus": {
            "notes": (
                "Calculus (Differential + Integral)\n\n"
                "Differentiation: d/dx(x^n) = n * x^(n-1)\n"
                "d/dx(sin x) = cos x\n"
                "d/dx(cos x) = -sin x\n\n"
                "Integration: Integral of x^n dx = x^(n+1)/(n+1) + C\n"
                "Integral of sin x dx = -cos x + C\n\n"
                "Trick: Power rule mein differentiation mein power ghatta hai (n-1), integration mein power badhta hai (n+1)."
            ),
            "quiz": [
                {"q": "d/dx(x^3) kya hoga?", "options": ["3x^2", "x^2", "3x", "x^3"], "answer": 0},
                {"q": "Integral of x dx kya hoga?", "options": ["x^2/2 + C", "x + C", "2x + C", "x^2 + C"], "answer": 0}
            ]
        },
        "Matrices and Determinants": {
            "notes": (
                "Matrices and Determinants\n\n"
                "2x2 matrix ka determinant: |a b; c d| = ad - bc\n\n"
                "Identity matrix (I): diagonal pe 1, baaki sab 0\n\n"
                "Matrix multiplication tabhi possible hai jab pehli matrix ke columns = doosri matrix ke rows.\n\n"
                "Trick: Determinant nikalne ke liye Cross Multiply, Minus karo - (a x d) - (b x c)."
            ),
            "quiz": [
                {"q": "Matrix [2 3; 1 4] ka determinant kya hai?", "options": ["5", "8", "11", "-5"], "answer": 0}
            ]
        },
        "Vector Algebra": {
            "notes": (
                "Vector Algebra\n\n"
                "Vector: magnitude + direction dono hote hain (jaise force, velocity)\n"
                "Scalar: sirf magnitude (jaise mass, speed)\n\n"
                "Dot product: a.b = |a||b|cos(theta) (result ek scalar hai)\n"
                "Cross product: a x b = |a||b|sin(theta) n-hat (result ek vector hai)\n\n"
                "Trick: Dot product = seedha number milta hai. Cross product = naya vector banta hai."
            ),
            "quiz": [
                {"q": "Dot product ka result kya hota hai?", "options": ["Scalar", "Vector", "Matrix", "Angle"], "answer": 0}
            ]
        },
        "Complex Numbers": {
            "notes": (
                "Complex Numbers\n\n"
                "Complex number: z = a + ib, jaha i = sqrt(-1)\n"
                "i^2 = -1, i^3 = -i, i^4 = 1 (fir cycle repeat hota hai)\n\n"
                "Modulus: |z| = sqrt(a^2 + b^2)\n\n"
                "Trick: i ki powers yaad rakho cycle mein: i, -1, -i, 1 - phir dobara repeat."
            ),
            "quiz": [
                {"q": "i^2 ka value kya hai?", "options": ["-1", "1", "0", "i"], "answer": 0}
            ]
        },
        "Statistics and Probability": {
            "notes": (
                "Statistics and Probability\n\n"
                "Mean = (Sum of all values) / (Total number of values)\n"
                "Median = beech ki value jab data sorted ho\n"
                "Mode = jo value sabse zyada baar aaye\n\n"
                "Probability = (Favourable outcomes) / (Total outcomes)\n"
                "Range hamesha 0 se 1 ke beech hota hai.\n\n"
                "Trick: MMM yaad rakho - Mean, Median, Mode teeno alag concept hain, confuse mat karo."
            ),
            "quiz": [
                {"q": "Ek sikke ko uchalne pe Heads aane ki probability kya hai?", "options": ["1/2", "1", "0", "1/4"], "answer": 0}
            ]
        },
        "Analytical Geometry": {
            "notes": (
                "Analytical Geometry (2D)\n\n"
                "Distance formula: d = sqrt[(x2-x1)^2 + (y2-y1)^2]\n\n"
                "Slope of line: m = (y2-y1)/(x2-x1)\n\n"
                "Circle equation: (x-h)^2 + (y-k)^2 = r^2 jaha (h,k) center hai, r radius hai.\n\n"
                "Trick: Distance formula Pythagoras theorem se hi aata hai - socho ek right triangle bana ke."
            ),
            "quiz": [
                {"q": "Points (0,0) aur (3,4) ke beech distance kya hai?", "options": ["5", "7", "4", "3"], "answer": 0}
            ]
        }
    },
    "NDA GAT": {
        "English": {
            "notes": (
                "English (Grammar + Vocabulary + Comprehension)\n\n"
                "Common error-spotting rules:\n"
                "- Subject-Verb Agreement: singular subject -> singular verb (He goes, not He go)\n"
                "- Articles: a/an consonant/vowel sound ke hisaab se, 'the' specific cheez ke liye\n"
                "- Tenses: past/present/future ka sahi use\n\n"
                "Synonym-Antonym roz 5 naye words yaad karo.\n\n"
                "Trick: Comprehension mein pehle questions padho, fir passage - isse time bachega."
            ),
            "quiz": [
                {"q": "'He go to school daily' mein error kya hai?", "options": ["go should be goes", "school should be schools", "daily should be daily's", "No error"], "answer": 0},
                {"q": "'Happy' ka antonym kya hai?", "options": ["Sad", "Joyful", "Glad", "Cheerful"], "answer": 0}
            ]
        },
        "Physics": {
            "notes": (
                "Physics Basics\n\n"
                "Newton's Laws of Motion:\n"
                "1st Law: Object rest/motion mein rahega jab tak external force na lage (Inertia)\n"
                "2nd Law: F = ma\n"
                "3rd Law: Har action ka equal-opposite reaction hota hai\n\n"
                "Units: Force -> Newton, Work -> Joule, Power -> Watt\n\n"
                "Trick: F=ma yaad rakhne ke liye socho - Force lagega tabhi Mass Accelerate karega."
            ),
            "quiz": [
                {"q": "F = ma mein 'a' kiske liye hai?", "options": ["Acceleration", "Area", "Angle", "Amplitude"], "answer": 0},
                {"q": "Work ka SI unit kya hai?", "options": ["Joule", "Newton", "Watt", "Pascal"], "answer": 0}
            ]
        },
        "Chemistry": {
            "notes": (
                "Chemistry Basics\n\n"
                "Oxidation: electron lose karna (LEO - Lose Electron Oxidation)\n"
                "Reduction: electron gain karna (GER - Gain Electron Reduction)\n\n"
                "Common gases: O2 (Oxygen - combustion ke liye zaroori), CO2 (photosynthesis mein use), H2 (sabse halki gas)\n\n"
                "Trick: 'LEO the lion says GER' - Oxidation = Lose, Reduction = Gain."
            ),
            "quiz": [
                {"q": "Sabse halki gas kaunsi hai?", "options": ["Hydrogen", "Oxygen", "Nitrogen", "CO2"], "answer": 0}
            ]
        },
        "General Science": {
            "notes": (
                "General Science (Biology + Everyday Science)\n\n"
                "Human body: 206 bones, heart 4 chambers wala hota hai (2 atria + 2 ventricles)\n\n"
                "Vitamins: A-eyes, C-immunity, D-bones (sunlight se milta hai), B12-blood\n\n"
                "Trick: Vitamin C ki kami se Scurvy hota hai - 'C se Scurvy' yaad rakho."
            ),
            "quiz": [
                {"q": "Insaan ke sharir mein kitni bones hoti hain?", "options": ["206", "196", "216", "186"], "answer": 0},
                {"q": "Vitamin D kaha se milta hai naturally?", "options": ["Sunlight", "Fruits", "Water", "Meat only"], "answer": 0}
            ]
        },
        "History": {
            "notes": (
                "History (Indian Freedom Movement + Culture)\n\n"
                "1857 Revolt - pehla swatantrata sangram, Mangal Pandey se shuru hua\n"
                "1885 - Indian National Congress ki sthapna\n"
                "1942 - Quit India Movement\n"
                "1947 - Independence\n\n"
                "Trick: Important dates ek timeline banake yaad karo - 1857 -> 1885 -> 1942 -> 1947."
            ),
            "quiz": [
                {"q": "Indian National Congress kab bani thi?", "options": ["1885", "1857", "1905", "1947"], "answer": 0}
            ]
        },
        "Geography": {
            "notes": (
                "Geography (Physical + Indian)\n\n"
                "Earth ki layers: Crust (upar), Mantle (beech), Core (sabse andar)\n\n"
                "India ki longest river: Ganga\n"
                "Highest peak: Kanchenjunga (India mein), Everest (world mein, Nepal border)\n\n"
                "Trick: Earth layers yaad rakho 'CMC' - Crust, Mantle, Core (bahar se andar)."
            ),
            "quiz": [
                {"q": "India ki sabse lambi nadi kaunsi hai?", "options": ["Ganga", "Yamuna", "Godavari", "Brahmaputra"], "answer": 0}
            ]
        },
        "Current Affairs": {
            "notes": (
                "Current Affairs - Kaise Prepare Karein\n\n"
                "Ye section roz update hota hai, isliye bot mein fixed events nahi de sakte - purane ho jayenge.\n\n"
                "Kya follow karo:\n"
                "1. Roz ek newspaper padho (The Hindu / Indian Express)\n"
                "2. Sports, Defence news, Government schemes pe special focus rakho\n"
                "3. Monthly current affairs PDF/app use karo (jaise Vision IAS, Drishti)\n"
                "4. Important awards, appointments, summits note karte raho\n\n"
                "Trick: Ek notebook banao - is week ke 5 important events likhte raho, revise karte raho."
            ),
            "quiz": [
                {"q": "Current Affairs ke liye sabse acha daily habit kya hai?", "options": ["Roz newspaper padhna", "Sirf exam se pehle padhna", "Kabhi na padhna", "Sirf sports dekhna"], "answer": 0}
            ]
        }
    },
    "Pharmacy": {
        "Pharmacokinetics": {
            "notes": (
                "Pharmacokinetics\n\n"
                "Drug body mein 4 stages se guzarta hai: ADME\n"
                "A - Absorption\nD - Distribution\nM - Metabolism\nE - Excretion\n\n"
                "Trick: 'A Dog Must Eat' (ADME)"
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
        "Namaste! Main tumhara Exam Prep Bot hoon.\nSubject choose karo:",
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
        keyboard.append([InlineKeyboardButton("Back", callback_data="HOME")])
        await query.edit_message_text(f"{subject} - Topic choose karo:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "TOPIC":
        subject, topic = data[1], data[2]
        keyboard = [
            [InlineKeyboardButton("Notes padho", callback_data=f"NOTES|{subject}|{topic}")],
            [InlineKeyboardButton("Quiz do", callback_data=f"QUIZ|{subject}|{topic}|0")],
            [InlineKeyboardButton("Back", callback_data=f"SUB|{subject}")]
        ]
        await query.edit_message_text(f"{topic}\n\nKya karna hai?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "NOTES":
        subject, topic = data[1], data[2]
        notes = CONTENT[subject][topic]["notes"]
        keyboard = [[InlineKeyboardButton("Back", callback_data=f"TOPIC|{subject}|{topic}")]]
        if len(notes) <= 4000:
            await query.edit_message_text(notes, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            chunks = [notes[i:i+4000] for i in range(0, len(notes), 4000)]
            await query.edit_message_text(chunks[0])
            for chunk in chunks[1:-1]:
                await query.message.reply_text(chunk)
            await query.message.reply_text(chunks[-1], reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "QUIZ":
        subject, topic, qnum = data[1], data[2], int(data[3])
        quiz_list = CONTENT[subject][topic]["quiz"]
        q = quiz_list[qnum]
        keyboard = [
            [InlineKeyboardButton(opt, callback_data=f"ANS|{subject}|{topic}|{qnum}|{i}")]
            for i, opt in enumerate(q["options"])
        ]
        progress = f"({qnum+1}/{len(quiz_list)})"
        await query.edit_message_text(f"Q {progress}: {q['q']}", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "ANS":
        subject, topic, qnum, chosen = data[1], data[2], int(data[3]), int(data[4])
        quiz_list = CONTENT[subject][topic]["quiz"]
        q = quiz_list[qnum]
        correct = q["answer"]
        if chosen == correct:
            result = "Sahi jawab!\n\n"
        else:
            result = f"Galat. Sahi jawab tha: {q['options'][correct]}\n\n"

        next_q = qnum + 1
        keyboard = []
        if next_q < len(quiz_list):
            keyboard.append([InlineKeyboardButton("Next Question", callback_data=f"QUIZ|{subject}|{topic}|{next_q}")])
        keyboard.append([InlineKeyboardButton("Topic pe wapas", callback_data=f"TOPIC|{subject}|{topic}")])
        await query.edit_message_text(result, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "HOME":
        keyboard = [[InlineKeyboardButton(sub, callback_data=f"SUB|{sub}")] for sub in CONTENT]
        await query.edit_message_text("Subject choose karo:", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot chalu ho gaya... Ctrl+C se rokna")
    app.run_polling()

if __name__ == "__main__":
    keep_alive()
    main()
