def store_feedback(feedback):
    with open("data/feedback.txt", "a", encoding="utf-8") as f:
        f.write(feedback + "\n")
