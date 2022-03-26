from random import randint


def questses(level: int = 1):
    arg1 = randint(1, 9999)
    arg2 = randint(1, 9999)
    if arg1 > arg2:
        arg1, arg2 = arg2, arg1

    text = ""
    TrueVarable = 0

    if level == 1:
        TrueVarable = arg2 - arg1
        text = f"{arg2} - {arg1} = ?"
    elif level == 2:
        TrueVarable = arg2 + arg1
        text = f"{arg2} + {arg1} = ?"
    elif level == 3:
        TrueVarable = arg2 / arg1
        text = f"{arg2} : {arg1} = ?"
    elif level == 4:
        TrueVarable = arg1 - arg2
        text = f"{arg1} - {arg2} = ?"
    elif level == 5:
        TrueVarable = (0 - arg2) + arg1
        text = f"{0 - arg2} + {arg1} = ?"
    elif level == 6:
        TrueVarable = (0 - arg1) + arg2
        text = f"{0 - arg1} + {arg2} = ?"

    howToTrue = randint(1, 3)

    Button = f'{TrueVarable}' if howToTrue == 1 else f"{randint((TrueVarable - randint(1, 100)), (TrueVarable + randint(1, 100)))}"
    Button2 = f'{TrueVarable}' if howToTrue == 2 else f"{randint((TrueVarable - randint(1, 100)), (TrueVarable + randint(1, 100)))}"
    Button3 = f'{TrueVarable}' if howToTrue == 3 else f"{randint((TrueVarable - randint(1, 100)), (TrueVarable + randint(1, 100)))}"

    return {"text": text, "B1": Button, "B2": Button2, "B3": Button3, "IsTrue": howToTrue}