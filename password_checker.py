import re

def check_password_strength(password):

    score = 0
    suggestions = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Password should be at least 8 characters.")

    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    # Number Check
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    # Special Character Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    # Final Strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, suggestions