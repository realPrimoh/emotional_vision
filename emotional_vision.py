from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw
from color_temps import convert_temp
from valence_arousal import VAdict


'''
Valence (like/dislike) determines the brightness of the image.
Arousal (excitement/boredom) determines the contrast and saturation of the image.

A happier image will have bright, popping colors.
A sadder image will have dimmer, blurrier colors.
'''


original = Image.open("sample1.jpg")
original.save("original.jpg")

def enhancer(im, va_list, key):
    assert type(va_list) is list

    arousal = va_list[0]
    valence = va_list[1]

    im = ImageEnhance.Brightness(im).enhance(1+(valence/3))

    im = ImageEnhance.Sharpness(im).enhance(1+(valence/3))

    if arousal > 0:
        im = ImageEnhance.Contrast(im).enhance(1+(arousal/3))
    if arousal < 0:
        im = ImageEnhance.Contrast(im).enhance(1-(arousal/3))

    im = ImageEnhance.Color(im).enhance(1+(arousal/2))

    temperature = min(((abs((valence + arousal)-2) * 1750) + 4000), 10000) #min handles any KeyErrors
    im = convert_temp(im, temperature)
    print(temperature)

    w, h = im.size
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('OpenSans-Bold.ttf', size = 100)
    title = 'arousal: '+str(arousal)
    title2 = 'valence: '+str(valence)
    text_w, text_h = draw.textsize(title, font)
    title3 = key

    #draw.text(((w - text_w) // 2, h - text_h), title, (0, 0, 0), font=font)
    draw.text((50, 20), title3, fill=(0,0,0, 255), font=font)
    draw.text((50, 150), title, fill = (0,0,0, 255), font=font)
    draw.text((50, 250), title2, fill=(0,0,0, 255), font=font)

    im.save('collage/arousal'+str(arousal)+'valence'+str(valence)+'.jpg')

for key, value in VAdict.items():
    print(value)
    enhancer(original, value, key)
