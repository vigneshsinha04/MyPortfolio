import mysql.connector
from difflib import get_close_matches

def dictionary():
    con = mysql.connector.connect(
    user = "ardit700_student",
    password = "ardit700_student",
    host = "108.167.140.122",
    database = "ardit700_pm1database"
    )
    cursor = con.cursor()
    word=input("Enter the word: ")
    query = f"SELECT Definition FROM Dictionary WHERE Expression = \'{word}\'"
    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        result = [i[0] for i in results]
        return "\n".join(result)
    else:
        exp_query = "SELECT Expression FROM Dictionary"
        cursor.execute(exp_query)
        exp_results = cursor.fetchall()
        ans = [j[0] for j in exp_results]

        similar = get_close_matches(word, ans)
        if len(similar) > 0:           
            closest_match = similar[0]
            user_input = input(f'Did you mean {closest_match} instead? Enter Y if yes, or N if no: ')
            if user_input == "Y":
                query = f"SELECT Definition FROM Dictionary WHERE Expression = \'{closest_match}\'"
                cursor.execute(query)
                closest_result = cursor.fetchall()
                if closest_result:
                    result = [i[0] for i in closest_result]
                    return result
            elif user_input == "N":
                return "The word doesn't exist. Please double check it."
            else:
                return "We didn't understand your entry."

print(dictionary())
