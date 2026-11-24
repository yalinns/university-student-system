# University Student System - Class Diagram to Python

Maps a UML class diagram of a student registration system to Python 3.9+ code.

## 1. Class diagram

```mermaid
classDiagram
    direction TB
    class Person {
        <<abstract>>
        -person_id: str
        +first_name: str
        +last_name: str
        +email: str
        +role()* str
        +set_contact(phone, street, city, country)
    }
    class ContactInfo {
        <<value object>>
        +phone: str
        +street: str
        +city: str
        +country: str
    }
    class Student {
        +student_no: str
        +enrollment_year: int
        +MAX_CREDITS_PER_TERM: int
        +join_program(program)
        +assign_advisor(lecturer)
        +register(section) Registration
        +withdraw(section) bool
        +gpa() float
        +earned_credits() int
        +can_graduate() bool
    }
    class Lecturer {
        +academic_title: str
        +office: str
        +submit_mark(registration, score)
    }
    class Faculty {
        +name: str
        +open_program(name, level, credits) Program
    }
    class Program {
        +name: str
        +level: DegreeLevel
        +required_credits: int
        +add_course(course)
    }
    class Course {
        +code: str
        +title: str
        +credits: int
        +add_prerequisite(course)
    }
    class Section {
        +term: str
        +capacity: int
        +is_full: bool
        +assign_lecturer(lecturer)
    }
    class Registration {
        <<association class>>
        +registered_on: date
        +status: RegistrationStatus
        +score: float
        +grade: LetterGrade
    }
    class LetterGrade { <<enumeration>> A B C D F }
    class RegistrationStatus { <<enumeration>> ACTIVE COMPLETED WITHDRAWN }
    class DegreeLevel { <<enumeration>> BACHELOR MASTER DOCTORATE }

    Person <|-- Student
    Person <|-- Lecturer
    Person *-- "0..1" ContactInfo
    Faculty *-- "0..*" Program
    Program o-- "0..*" Course
    Program "0..1" -- "0..*" Student : enrolled in
    Lecturer "0..1" -- "0..*" Student : advises
    Course "0..*" --> "0..*" Course : prerequisites
    Course "1" -- "0..*" Section : offered as
    Lecturer "0..1" -- "0..*" Section : teaches
    Student "1" -- "0..*" Registration
    Section "1" -- "0..*" Registration
    Registration --> LetterGrade
    Registration --> RegistrationStatus
    Program --> DegreeLevel
```

## 2. Mapping rules (design -> code)

| UML element | Python mapping | Where |
|---|---|---|
| Class | `class` | all modules |
| Abstract class / operation | `ABC` + `@abstractmethod` | `Person`, `Person.role()` |
| Generalization | inheritance | `Student(Person)`, `Lecturer(Person)` |
| Enumeration | `enum.Enum` | `LetterGrade`, `RegistrationStatus`, `DegreeLevel` |
| Private attribute (`-`) | `_name` + read-only `@property` | `Person.person_id`, `Registration.score` |
| Static / constant | class attribute | `Student.MAX_CREDITS_PER_TERM` |
| Value object | frozen `@dataclass` | `ContactInfo` |
| Composition | owner creates the part | `Person.set_contact`, `Faculty.open_program` |
| Aggregation | whole stores references passed in | `Program.add_course` |
| Association 0..1 / 1 | single reference attribute | `Student.program`, `Section.lecturer` |
| Association 0..* | `list` exposed as a copy | `Program.students`, `Lecturer.sections` |
| Bidirectional association | one method updates both ends | `Student.join_program`, `Section.assign_lecturer` |
| Self-association | list of the same type | `Course.prerequisites` |
| Association class | separate class holding both ends + link data | `Registration` |
| Business rules | custom exception | `RegistrationError` |

## 3. Business rules implemented
- no duplicate registration, and no re-taking a course already passed
- prerequisites must be passed
- section capacity and a 24-credit limit per term
- only the section's lecturer can submit marks (0-100 -> letter grade)
- GPA = sum(points x credits) / sum(credits); graduation needs the credits and all program courses

## 4. Structure
```
university-student-system/
├── main.py                 # demo
├── university/
│   ├── people.py           # Person, Student, Lecturer, ContactInfo
│   ├── academics.py        # Faculty, Program, Course, Section
│   └── registration.py     # Registration, grades, status, errors
└── tests/test_university.py
```

## 5. Run
```
python main.py
python -m unittest discover -s tests
```
