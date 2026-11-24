"""Demo: exercises every class and relationship of the student class diagram."""
from university import (Course, DegreeLevel, Faculty, Lecturer, RegistrationError,
                        Section, Student)


def main() -> None:
    faculty = Faculty("Engineering")
    program = faculty.open_program("Computer Engineering", DegreeLevel.BACHELOR, required_credits=12)

    prog1 = Course("CS101", "Programming I", 6)
    prog2 = Course("CS102", "Programming II", 6)
    prog2.add_prerequisite(prog1)
    program.add_course(prog1)
    program.add_course(prog2)

    lecturer = Lecturer("L-1", "Selin", "Aydin", "selin.aydin@uni.edu", "Dr.", office="B-204")
    sec1 = Section(prog1, "2026-Fall", capacity=2)
    sec2 = Section(prog2, "2027-Spring", capacity=30)
    sec1.assign_lecturer(lecturer)
    sec2.assign_lecturer(lecturer)

    can = Student("S-1", "Can", "Ozturk", "can@uni.edu", "20260001", 2026)
    deniz = Student("S-2", "Deniz", "Er", "deniz@uni.edu", "20260002", 2026)
    can.set_contact("+90 555 000 00 01", "Cumhuriyet Cd. 5", "Mersin", "Turkey")
    for s in (can, deniz):
        s.join_program(program)
        s.assign_advisor(lecturer)

    r_can = can.register(sec1)
    r_deniz = deniz.register(sec1)
    lecturer.submit_mark(r_can, 92)
    lecturer.submit_mark(r_deniz, 55)

    can.register(sec2)
    lecturer.submit_mark(can.registrations[-1], 84)

    print(faculty, "->", program)
    for s in program.students:
        print(f"\n{s} | advisor: {s.advisor.full_name} | contact: {s.contact or '-'}")
        for line in s.transcript():
            print("  ", line)
        print(f"   GPA: {s.gpa():.2f} | earned credits: {s.earned_credits()} | can graduate: {s.can_graduate()}")

    print("\n--- Business rules ---")
    for label, action in [
        ("prerequisite", lambda: deniz.register(sec2)),
        ("duplicate/passed", lambda: can.register(sec1)),
        ("wrong lecturer", lambda: Lecturer("L-2", "Ali", "Veli", "a@uni.edu", "Prof.").submit_mark(r_can, 70)),
    ]:
        try:
            action()
        except RegistrationError as exc:
            print(f"Blocked ({label}): {exc}")


if __name__ == "__main__":
    main()
