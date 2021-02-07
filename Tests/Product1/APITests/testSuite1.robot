*** Settings ***
Library  RequestsLibrary
Library  Collections

*** Variables ***
${url}  http://127.0.0.1:5000
${id}  44
${get_url}  /api/v1/resources/employees/all
${get_employee}  /api/v1/resources/employees/?id=${id}
${get_highest_url}  /api/v1/resources/employees/get_highest_salary_employee
${post_url}  /api/v1/resources/employees/
${put_url}  /api/v1/resources/employees/?id=${id}

&{post_data}  _id=${id}  name=Arwad  age=21  salary=1000
&{put_data}   name=Arwad  age=22  salary=1500

*** Test Cases ***

GET All Employees
  [documentation]  This will test GET request on fetching all employees
  [tags]  ApiTesting

  create session  GetRequest  ${url}
  ${response}  GET On Session  GetRequest  ${get_url}
  ${status_code}  convert to string  ${response.status_code}
  should be equal  ${status_code}  200
  ${body}  convert to string  ${response.content}
  should contain  ${body}  salary

GET Highest Salary Employee
  [documentation]  This will test if GET Reeqeust return empolyee with highest paid salary
  [tags]  ApiTesting

  create session  GetRequest  ${url}
  ${response}  GET On Session  GetRequest  ${get_highest_url}
  ${status_code}  convert to string  ${response.status_code}
  should be equal  ${status_code}  200
  ${body}  convert to string  ${response.content}
  should contain  ${body}  2372


ADD Employees
  [documentation]  This will test the process of adding employees using POST request
  [tags]  ApiTesting

  create session  PostRequest  ${url}
  ${response}  POST On Session  PostRequest  ${post_url}  json=&{post_data}
  ${status_code}  convert to string  ${response.status_code}
  should be equal  ${status_code}  200
  ${body}  convert to string  ${response.content}
  log to console  ${body}

  create session  GetRequest  ${url}
  ${response}  GET On Session  GetRequest  ${get_employee}
  ${status_code}  convert to string  ${response.status_code}
  should be equal  ${status_code}  200
  ${body}  convert to string  ${response.content}
  should contain  ${body}  ${id}


Update Employees
  [documentation]  This will test the process of Updating employees using PUT request
  [tags]  ApiTesting

  create session  PutRequest  ${url}
  ${response}  PUT On Session  PutRequest  ${put_url}  json=&{put_data}
  ${status_code}  convert to string  ${response.status_code}
  should be equal  ${status_code}  200
  ${body}  convert to string  ${response.content}
  log to console  ${body}

  create session  GetRequest  ${url}
  ${response}  GET On Session  GetRequest  ${get_employee}
  ${status_code}  convert to string  ${response.status_code}
  should be equal  ${status_code}  200
  ${body}  convert to string  ${response.content}
  should contain  ${body}  ${id}
  ${emp_id}  get from dictionary  ${response.json}  _id
  log to console  ${emp_id}



