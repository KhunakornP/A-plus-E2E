# A-plus-E2E
End-To-End-Tests for A+ management.<br>
Link to A+ management: https://github.com/KhunakornP/A-plus-management

## Prerequisites
- python 3.11 or newer
- git
- Chrome browser

## How to test
1. clone the repository
```
git clone https://github.com/KhunakornP/A-plus-E2E.git
```
2. move to the directory
```
cd A-plus-E2E
```
3. install required libraries
```
pip install -r requirements.txt
```
4. create a .env with the following information

| Variable         | What you should put in                                             |
|------------------|--------------------------------------------------------------------|
| STUDENT_EMAIL    | email of a registered User that is a student                       |
| STUDENT_PASSWORD | password of the student                                            |
| PARENT_EMAIL     | email of a registered User that is a parent                        |
| PARENT_PASSWORD  | password of the parent                                             |
| HEADLESS         | True if you don't want to see a browser interface, False otherwise |


5. run the script
```
python scripts.py <test to run>
```

## Test suites

| command    | What it tests                                                                                         |
|------------|-------------------------------------------------------------------------------------------------------|
| present    | Test basic student actions as well as parent action.<br>Run with HEADLESS = False for best experience |
| basic      | Test taskboard creation and task creation.                                                            |
| calculator | Test calculator calculation                                                                           |
| burn       | Test for Burn-down charts                                                                             |
| profile    | Test updating user profile, A-level status, and adding parents for students                           |
| parent     | Test viewing the parent dashboard                                                                     |
