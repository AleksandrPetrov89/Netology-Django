import pytest
import pytest_django
import random
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


# def test_example():
#     assert False, "Just test example"


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make(Student, **kwargs)
    return factory


@pytest.mark.django_db
def test_receiving_1_course(client, course_factory):

    # Arrange
    course = course_factory(_quantity=1)
    url = f'/api/v1/courses/{course[0].id}/'

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == course[0].id
    assert data["name"] == course[0].name


@pytest.mark.django_db
def test_receiving_all_courses(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=10)
    url = f'/api/v1/courses/'

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    for count, element in enumerate(data):
        assert element["id"] == courses[count].id
        assert element["name"] == courses[count].name


@pytest.mark.django_db
def test_filtering_by_id(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=8)
    course = random.choice(courses)
    url = f'/api/v1/courses/?id={course.id}'

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == course.id
    assert data[0]["name"] == course.name


@pytest.mark.django_db
def test_filtering_by_name(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=12)
    course = random.choice(courses)
    url = f'/api/v1/courses/?name={course.name}'

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == course.id
    assert data[0]["name"] == course.name


@pytest.mark.django_db
def test_course_creation(client):

    # Arrange
    url = f'/api/v1/courses/'
    data = {'name': 'Курс № 1'}
    count = Course.objects.count()

    # Act
    response = client.post(url, data=data, format='json')  # Формат можно задать в settings.py

    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    resp_data = response.json()
    course = Course.objects.filter(name='Курс № 1')
    assert resp_data["id"] == course[0].id
    assert resp_data["name"] == course[0].name


@pytest.mark.django_db
def test_course_update(client, course_factory):

    # Arrange
    course = course_factory(_quantity=1)[0]
    url = f'/api/v1/courses/{course.id}/'
    data = {'name': 'Курс № 2'}
    count = Course.objects.count()

    # Act
    response = client.patch(url, data=data, format='json')  # Формат можно задать в settings.py

    # Assert
    assert response.status_code == 200
    assert Course.objects.count() == count
    course = Course.objects.filter(id=course.id)[0]
    resp_data = response.json()
    assert resp_data["id"] == course.id
    assert resp_data["name"] == course.name


@pytest.mark.django_db
def test_course_deletion(client, course_factory):

    # Arrange
    course = course_factory(_quantity=1)[0]
    url = f'/api/v1/courses/{course.id}/'
    count = Course.objects.count()

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 204
    assert Course.objects.count() == count - 1


@pytest.mark.parametrize(
    ['quantity', 'status_code'],
    (
        (3, 201),
        (20, 201),
        (21, 400)
    )
)
@pytest.mark.django_db
def test_course_create_validation(client, student_factory, course_factory,
                                  settings, quantity, status_code):

    # Arrange
    settings.MAX_STUDENTS_PER_COURSE = 2

    students = student_factory(_quantity=quantity)
    students_id = [student.id for student in students]
    url = f'/api/v1/courses/'
    data = {'name': 'Курс № 3', 'students': students_id}

    # Act
    response = client.post(url, data=data, format='json')  # Формат можно задать в settings.py

    # Assert
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ['quantity_1', 'status_code_1', 'quantity_2', 'status_code_2'],
    (
        (3, 200, 2, 200),
        (10, 200, 10, 200),
        (21, 400, 5, 200),
        (5, 200, 16, 400),
        (21, 400, 22, 400)
    )
)
@pytest.mark.django_db
def test_course_update_validation(client, course_factory, student_factory, settings,
                                  quantity_1, status_code_1, quantity_2, status_code_2):

    # Arrange
    settings.MAX_STUDENTS_PER_COURSE = 2

    students_1 = student_factory(_quantity=quantity_1)
    students_1_id = [student.id for student in students_1]
    data_1 = {'name': 'Курс № 4a', 'students': students_1_id}

    students_2 = student_factory(_quantity=quantity_2)
    students_2_id = [student.id for student in students_2]
    data_2 = {'name': 'Курс № 4b', 'students': students_2_id}

    course = course_factory(_quantity=1)[0]
    url = f'/api/v1/courses/{course.id}/'

    # Act
    response_1 = client.patch(url, data=data_1, format='json')  # Формат можно задать в settings.py
    response_2 = client.patch(url, data=data_2, format='json')  # Формат можно задать в settings.py

    # Assert
    assert response_1.status_code == status_code_1
    assert response_2.status_code == status_code_2
