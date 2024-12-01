import pytest
from stud_array import Student, StudentArray  # Замените на ваш файл с классами

@pytest.fixture
def sample_students():
    """Возвращает массив студентов с минимум 10 элементами для тестов."""
    sa = StudentArray()
    sa.add_student(Student("Браун Алексей Викторович", "201", 2, 21, 4.0))
    sa.add_student(Student("Панин Виктор Анатольевич", "202", 3, 20, 4.2))
    sa.add_student(Student("Головкин Артем Андреевич", "203", 1, 22, 3.8))
    sa.add_student(Student("Калинина Мария Сергеевна", "204", 4, 19, 4.5))
    sa.add_student(Student("Федосова Галина Петровна", "205", 1, 23, 3.6))
    sa.add_student(Student("Шаров Сергей Павлович", "206", 3, 20, 4.3))
    sa.add_student(Student("Смирнов Илья Станиславович", "207", 2, 24, 4.1))
    sa.add_student(Student("Тихонов Алексей Юрьевич", "208", 4, 22, 3.9))
    sa.add_student(Student("Левитина Ольга Александровна", "209", 2, 21, 4.4))
    sa.add_student(Student("Петрова Анастасия Владиславовна", "210", 1, 18, 3.7))
    return sa

def test_add_student(sample_students):
    """Проверяет, добавляется ли студент."""
    initial_count = len(sample_students.students)
    new_student = Student("Абрамович Григорий Петров", "211", 1, 18, 4.0)
    sample_students.add_student(new_student)
    assert len(sample_students.students) == initial_count + 1
    assert sample_students.find_student_by_fio("Абрамович Григорий Петров") is not None

def test_remove_student(sample_students):
    """Проверяет, удаляется ли студент по ФИО."""
    sample_students.remove_student("Панин Виктор Анатольевич")
    assert sample_students.find_student_by_fio("Панин Виктор Анатольевич") is None

def test_find_student_by_fio(sample_students):
    """Проверяет корректность поиска студента по ФИО."""
    student = sample_students.find_student_by_fio("Браун Алексей Викторович")
    assert student is not None
    assert student.fio == "Браун Алексей Викторович"
    assert sample_students.find_student_by_fio("Неизвестный") is None

def test_average_grade(sample_students):
    """Проверяет вычисление средней оценки студентов."""
    avg_grade = sample_students.average_grade()
    expected_avg = sum([4.0, 4.2, 3.8, 4.5, 3.6, 4.3, 4.1, 3.9, 4.4, 3.7]) / 10
    assert avg_grade == pytest.approx(expected_avg, 0.01)

def test_filter_by_course(sample_students):
    """Проверяет фильтрацию студентов по курсу."""
    students_on_course = sample_students.filter_by_course(2)
    assert all(student.course == 2 for student in students_on_course)
    assert len(students_on_course) > 0

def test_sort_fio(sample_students):
    """Проверяет сортировку студентов по ФИО (по возрастанию)."""
    sample_students.sort_fio()
    sorted_fios = [student.fio for student in sample_students.students]
    assert sorted_fios == sorted(sorted_fios)

def test_sort_course(sample_students):
    """Проверяет сортировку студентов по курсу (по убыванию)."""
    sample_students.sort_course()
    sorted_courses = [student.course for student in sample_students.students]
    assert sorted_courses == sorted(sorted_courses, reverse=True)

def test_get_student_with_highest_grade(sample_students):
    """Проверяет получение студента с самой высокой средней оценкой."""
    student = sample_students.get_student_with_highest_grade()
    assert student is not None
    assert student.average_grade == max(s.average_grade for s in sample_students.students)

def test_get_students_above_average_grade(sample_students):
    """Проверяет получение студентов с оценкой выше средней."""
    avg_grade = sample_students.average_grade()
    students_above_avg = sample_students.get_students_above_average_grade()
    assert all(student.average_grade > avg_grade for student in students_above_avg)

def test_count_students_by_course(sample_students):
    """Проверяет подсчет количества студентов по курсам."""
    course_counts = sample_students.count_students_by_course()
    assert sum(course_counts.values()) == len(sample_students.students)
    assert all(count > 0 for count in course_counts.values())

@pytest.fixture
def large_student_array():
    """Создает массив студентов с большим количеством элементов для тестов производительности."""
    sa = StudentArray()
    for i in range(1000):
        sa.add_student(Student(f"Студент {i}", str(i % 10), i % 4 + 1, 18 + i % 5, 3.5 + (i % 5) * 0.1))
    return sa

def test_sort_fio_benchmark(benchmark, large_student_array):
    """Бенчмарк для метода sort_fio."""
    benchmark(large_student_array.sort_fio)

def test_sort_course_benchmark(benchmark, large_student_array):
    """Бенчмарк для метода sort_course."""
    benchmark(large_student_array.sort_course)
