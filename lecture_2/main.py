def generate_profile(age: int) -> str:
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"


def main():
    user_name = input("Welcome, enter your full name: ")
    birth_year_str = input("Enter your birth year: ")
    birth_year = int(birth_year_str)
    current_age = 2025 - birth_year

    hobbies = []
    ask_hobby_message = "Enter a favorite hobby or type 'stop' to finish: "

    while (hobby := input(ask_hobby_message)) and hobby.lower() != "stop":
        hobbies.append(hobby)

    life_stage = generate_profile(current_age)

    user_profile = {
        "name": user_name,
        "age": current_age,
        "stage": life_stage,
        "hobbies": hobbies
    }

    profile_summary = (
        "\n---\n"
        f"Profile Summary:\n"
        f"Name: {user_profile['name']}\n"
        f"Age: {user_profile['age']}\n"
        f"Life Stage: {user_profile['stage']}\n"
    )

    hobbies_count = len(hobbies)

    if hobbies_count == 0:
        profile_summary += "You didn't mention any hobbies.\n"
    else:
        profile_summary += f"Favorite Hobbies ({hobbies_count}):\n"
        for hobby in hobbies:
            profile_summary += f"- {hobby}\n"

    profile_summary += "---\n"

    print(profile_summary)


if __name__ == "__main__":
    main()
