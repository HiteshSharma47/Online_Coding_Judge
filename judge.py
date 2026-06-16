import subprocess as sp
from database import get_testcases
import time
import os


def run_judge(problem_id,source_code):

    testcases=get_testcases(problem_id)

    try:

        with open("temp_submission.py","w") as f:
            f.write(source_code)

        total_testcases = len(testcases)

        start_time = time.time()

        for index, testcase in enumerate(testcases, start = 1):

            input_data = testcase[0]
            expected_output = testcase[1]

            try: 
                ans = sp.run(
                ['python', "temp_submission.py"],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=2
                )

            except sp.TimeoutExpired: 
                execution_time = round(time.time() - start_time, 3) 

                return {
                    "Status": "Time Limit Exceed",
                    "Execution Time": execution_time,
                    "Failed Testcase": index,
                    "Total": total_testcases
                }

            if ans.returncode != 0:
                error_msg = ans.stderr.strip().split("\n")[-1]

                execution_time = round(time.time() - start_time, 3) 

                return {
                    "Status": "Runtime Error!",
                    "Execution Time": execution_time,
                    "Error": error_msg,
                    "Failed Testcase": index,
                    "Total": total_testcases
                }

            actual_output = ans.stdout.strip()

            if actual_output != expected_output:
                execution_time = round(time.time() - start_time, 3) 
                return {
                    "Status": "Wrong Answer!",
                    "Execution Time": execution_time,
                    "Input": input_data,
                    "Your Output": actual_output,
                    "Expected Output": expected_output,
                    "Passed": index - 1,
                    "Total":total_testcases,
                    "Failed Testcase": index
                }

        execution_time = round(time.time() - start_time, 3) 

        return {
        "Status": "Accepted!",
        "Execution Time": execution_time,
        "Passed": total_testcases,
        "Total": total_testcases
        }
    
    finally:
        if os.path.exists("temp_submission.py"):
            os.remove("temp_submission.py")

def run_sample(source_code, sample_input):

    try:
        with open("temp_submission.py", "w") as f:
            f.write(source_code)

        start_time = time.time()

        try:
            ans = sp.run(
                ['python', 'temp_submission.py'],
                input=sample_input,
                capture_output=True,
                text=True,
                timeout=2
            )

        except sp.TimeoutExpired:
            execution_time = round(time.time() - start_time, 3) 

            return {
                "Status": "Time Limit Exceed",
                "Execution Time": execution_time
            }

        if ans.returncode != 0:
            error_msg = ans.stderr.strip().split("\n")[-1]

            execution_time = round(time.time() - start_time, 3) 

            return {
                "Status": "Runtime Error!",
                "Execution Time": execution_time,
                "Error": error_msg
            }

        actual_output = ans.stdout.strip()

        execution_time = round(time.time() - start_time, 3) 

        return {
            "Status": "Success",
            "Execution Time": execution_time,
            "Output": actual_output
        }
    
    finally:
        if os.path.exists("temp_submission.py"):
            os.remove("temp_submission.py")
