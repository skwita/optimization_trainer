def check_answer(user_input, correct, tol=0):
    try:
        user_val = float(user_input)
        return abs(user_val - correct) <= tol
    except:
        return str(user_input).strip().lower() == str(correct).lower()