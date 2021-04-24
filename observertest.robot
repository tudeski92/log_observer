*** Settings ***
Library    log_observer.py


*** Variables ***
@{events}=    101
...           100
...           102
...           103
${path}=     "."
${filename}=    "logging.log"
${pattern}=     "*"
${ignore_pattern}=    ""
${log_pattern}=    r".*"


*** Test Cases ***
Check if observer works
    Log  ${events}
    ${observer}=    start observer process  ${pattern}  ${ignore_pattern}  ${filename}  ${log_pattern}
    ...  ${path}  ${events}
    save log
    wait until observer completed  ${observer}  30





*** Keywords ***