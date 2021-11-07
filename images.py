from PIL import Image, ImageDraw, ImageFont
import main
import datetime


class Worker:
    def output_image(last_data, theme):
        # Opens icons
        if last_data is None:
            return None
        clr = "_black" if theme == main.windows["light"] else ""
        images = f"{main.directory}\\ui\\images\\highres"
        humidity = Image.open(
            f"{images}\\drop{clr}.png").resize((100, 100))
        barometer = Image.open(
            f"{images}\\barometer{clr}.png").resize((100, 100))
        wind = Image.open(f"{images}\\wind{clr}.png").resize((100, 100))
        ultraviolet = Image.open(
            f"{images}\\ultraviolet{clr}.png").resize((100, 100))
        day = Image.open(
            f"{images}\\sunny{clr}.png").resize((100, 100))
        night = Image.open(
            f"{images}\\night-mode{clr}.png").resize((100, 100))
        sunrise = Image.open(
            f"{images}\\sunrise{clr}.png").resize((100, 100))
        sunset = Image.open(
            f"{images}\\sunset{clr}.png").resize(
                (100, 100)).convert("RGBA")
        # Opens background
        background = Image.open(
            f"{main.directory}\\ui\\images\\"
            + f"{'' if theme == main.windows['dark'] else 'light/'}"
            + "share_background.jpeg").convert("RGBA")
        txt = Image.new("RGBA", background.size, (255, 255, 255, 0))
        font = ImageFont.truetype(
            f"{main.directory}\\ui\\Bahnschrift.ttf", 63)
        draw = ImageDraw.Draw(txt)
        textColor = (
            200, 200, 200, 255) if theme == main.windows["dark"] else (
                0, 0, 0, 200)
        # Humidity
        background.paste(humidity, (20, 20), humidity)
        draw.text(
            (150, 40), str(last_data["Humidity"]) + "%", font=font,
            fill=textColor)
        # Air pressure
        background.paste(barometer, (20, 175), barometer)
        draw.text(
            (150, 195), str(last_data["Pressure"]), font=font,
            fill=textColor)
        # Wind
        background.paste(wind, (20, 330), wind)
        draw.text(
            (150, 350), str(last_data["WindSpeed"]) + "", font=font,
            fill=textColor)
        # Ultraviolet
        background.paste(ultraviolet, (20, 485), ultraviolet)
        draw.text(
            (150, 505), str(last_data["UVIndex"]), font=font,
            fill=textColor)
        # Day temp
        background.paste(day, (330, 330), day)
        draw.text(
            (450, 350),
            f"{'+' if last_data['DayTemperature'] > 0 else ''}"
            + f"{last_data['DayTemperature']}°", font=font, fill=textColor)
        # Night temp
        background.paste(night, (630, 330), night)
        draw.text(
            (740, 350),
            f"{'+' if last_data['NightTemperature'] > 0 else ''}"
            + f"{last_data['NightTemperature']}°",
            font=font, fill=textColor)
        # Sunrise time
        background.paste(sunrise, (330, 485), sunrise)
        draw.text(
            (450, 505), last_data["SunriseTime"],
            font=font, fill=textColor)
        # Sunset time
        background.paste(sunset, (630, 485), sunset)
        draw.text(
            (740, 505), last_data["SunsetTime"],
            font=font, fill=textColor)
        # Current time
        time = datetime.datetime.now()
        font = ImageFont.truetype(
            f"{main.directory}\\ui\\Bahnschrift.ttf", 30)
        draw.text(
            (800, 20), time.time().strftime("%H:%M"),
            font=font, fill=textColor)
        font = ImageFont.truetype(
            f"{main.directory}\\ui\\Bahnschrift.ttf", 200)
        temp = last_data["Temperature"]
        temp = f"{'+' if temp > 0 else ''}{temp}°"
        draw.text(
            (550 - len(str(temp)) * 30, 75), temp,
            font=font, fill=textColor)

        out = Image.alpha_composite(background, txt)
        out.show()

        humidity.close()
        barometer.close()
        wind.close()
        ultraviolet.close()
        day.close()
        night.close()
        sunrise.close()
        sunset.close()
        background.close()
