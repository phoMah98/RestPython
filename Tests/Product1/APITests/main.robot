*** Settings ***
Library  SeleniumLibrary
Test Setup  Start Browser
Test Teardown  End Test

*** Variables ***
${queue}  gpu
&{search_text}  gpu=rtx  pcs=dell  name=bobo
${ab}  hi
${url}
${browser}

*** Test Cases ***
This is an example
    [documentation]  example test of robot framework
    [tags]  functional

    Verify Results
    Log  ${AB}

*** Keywords ***

Start Browser
  [documentation]  starting google chrome
   Open Browser  ${url}  ${browser}
   Maximize Browser Window

Verify Results
  [documentation]  this will be the test body
   Input Text  //*[@id="twotabsearchtextbox"]  ${search_text.${queue}}
   Press Keys  id:nav-search-submit-button  [RETURN]
   Page Should Contain  results for "${search_text.${queue}}"

End Test
  Close Browser

