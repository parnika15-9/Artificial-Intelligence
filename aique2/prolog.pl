:- use_module(library(csv)).

% Load the CSV file
load_students :-
    csv_read_file("data.csv", Rows, [functor(student), arity(4)]),
    maplist(assert, Rows).

% Ensure the data is loaded on startup
:- load_students.
% Rule to check scholarship eligibility
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, _, Attendance_percentage, CGPA),
    Attendance_percentage >= 75,
    CGPA >= 9.0.

% Rule to check exam permission
permitted_for_exam(Student_ID) :-
    student(Student_ID, _, Attendance_percentage, _),
    Attendance_percentage >= 75.
:- use_module(library(http/http_server)).
:- use_module(library(http/json)).

% API to check scholarship eligibility
handle_scholarship(Request) :-
    http_parameters(Request, [id(Student_ID, [integer])]),
    (eligible_for_scholarship(Student_ID) ->
        Reply = json{status: "eligible", message: "Student is eligible for scholarship"};
        Reply = json{status: "ineligible", message: "Student is not eligible for scholarship"}
    ),
    reply_json(Reply).

% API to check exam permission
handle_exam_permission(Request) :-
    http_parameters(Request, [id(Student_ID, [integer])]),
    (permitted_for_exam(Student_ID) ->
        Reply = json{status: "permitted", message: "Student is permitted for the exam"};
        Reply = json{status: "not_permitted", message: "Student is not permitted for the exam"}
    ),
    reply_json(Reply).

% Start the HTTP server
:- http_server([port(8080)]).
