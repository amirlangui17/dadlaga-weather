from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)

# Нууц түлхүүр
app.secret_key = "weather-secret-key-2026"

# =========================
# АДМИН НУУЦ ҮГ
# =========================

ADMIN_PASSWORD = "1234"

# =========================
# МЭДЭЭЛЭЛ ХАДГАЛАХ ФАЙЛ
# =========================

DATA_FILE = "weather.json"


# =========================
# Анхны мэдээлэл
# =========================

default_weather = {
    "year": "2026",
    "month": "8",
    "day": "18",
    "start_time": "08:00",
    "end_day": "18",
    "end_time": "20:00",

    "province": "СЭЛЭНГЭ АЙМГИЙН НУТГААР",
    "province_condition": "Солигдмол үүлтэй. Зарим сумдын нутгаар бага зэргийн бороо орно.",
    "province_wind": "Салхи баруунаас секундэд 5-10 метр хүрнэ.",
    "province_night": "+10...+12 ",
    "province_day": "+22...+27",

    "city": "СҮХБААТАР ХОТ ОРЧМООР",
    "city_condition": "Солигдмол үүлтэй. Бороо орохгүй",
    "city_wind": "Салхи баруунаас секундэд 5-10 метр хүрнэ.",
    "city_night": "+10...+12 ",
    "city_day": "+24...+26",

    "detail": " 18-нд зарим сумдын нутгаар, 21-нд ихэнх сумдын нутгаар  бороо, дуу цахилгаантай орно. Бусад хугацаанд бороо орохгүй. Салхи ихэнх хугацаанд баруунаас секундэд 5-10 метр, борооны өмнө түр зуур ширүүснэ. Агаарын температур шөнөдөө +9...+14  градус, өдөртөө +22...+27 градус дулаан байна.",
    "forecaster": "Мэдээ бичсэн инженер: ........."
}


# =========================
# МЭДЭЭЛЭЛ УНШИХ
# =========================

def load_weather():

    if not os.path.exists(DATA_FILE):

        save_weather(default_weather)

        return default_weather

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as file:

            return json.load(file)

    except:

        return default_weather


# =========================
# МЭДЭЭЛЭЛ ХАДГАЛАХ
# =========================

def save_weather(weather):

    with open(DATA_FILE, "w", encoding="utf-8") as file:

        json.dump(
            weather,
            file,
            ensure_ascii=False,
            indent=4
        )


# =========================
# НҮҮР ХУУДАС
# =========================

@app.route("/")
def home():

    weather = load_weather()

    return render_template(
        "index.html",
        weather=weather
    )


# =========================
# АДМИН НЭВТРЭХ
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    # Нэвтрээгүй бол login харуулна

    if not session.get("admin"):

        if request.method == "POST":

            password = request.form.get("password")

            if password == ADMIN_PASSWORD:

                session["admin"] = True

                return redirect(
                    url_for("admin")
                )

            else:

                return render_template(
                    "admin_login.html",
                    error="Нууц үг буруу байна."
                )

        return render_template(
            "admin_login.html"
        )

    # =========================
    # МЭДЭЭЛЭЛ ШИНЭЧЛЭХ
    # =========================

    if request.method == "POST":

        weather = {

            "year":
                request.form.get("year"),

            "month":
                request.form.get("month"),

            "day":
                request.form.get("day"),

            "start_time":
                request.form.get("start_time"),

            "end_day":
                request.form.get("end_day"),

            "end_time":
                request.form.get("end_time"),

            "province":
                request.form.get("province"),

            "province_condition":
                request.form.get("province_condition"),

            "province_wind":
                request.form.get("province_wind"),

            "province_night":
                request.form.get("province_night"),

            "province_day":
                request.form.get("province_day"),

            "city":
                request.form.get("city"),

            "city_condition":
                request.form.get("city_condition"),

            "city_wind":
                request.form.get("city_wind"),

            "city_night":
                request.form.get("city_night"),

            "city_day":
                request.form.get("city_day"),

            "detail":
                request.form.get("detail"),

            "forecaster":
                request.form.get("forecaster")
        }

        save_weather(weather)

        return redirect(
            url_for("admin", saved="1")
        )


    weather = load_weather()

    return render_template(
        "admin.html",
        weather=weather,
        saved=request.args.get("saved")
    )


# =========================
# ГАРАХ
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================
# АЖИЛЛУУЛАХ
# =========================

if __name__ == "__main__":
    import os

    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
