from judge import run_judge
from database import get_problem,create_submission,update_submission
def main(): 
    problem_id = 1

    source_code ="a, b = map(int, input().split())\nprint(a + b)"

    problem_detail = get_problem(problem_id)

    print("Problem :",problem_detail[0])
    print("Description :", problem_detail[1])

    submission_id = create_submission(
        problem_id,
        source_code
    )

    result = run_judge(
        problem_id,
        source_code
    )

    update_submission(
        submission_id,
        result["Status"]
    )

    print(result)

if __name__ == "__main__":
    main()

