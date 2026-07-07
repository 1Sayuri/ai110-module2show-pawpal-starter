from pawpal_system import Pet, Task


def test_task_completion_marks_task_as_complete():
    task = Task(
        task_id="task-1",
        pet_id="pet-1",
        title="Morning walk",
        category="walk",
        duration=20,
        priority="high",
    )

    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(
        pet_id="pet-1",
        owner_id="owner-1",
        name="Mochi",
        species="dog",
    )

    initial_count = len(pet.get_tasks())

    task = Task(
        task_id="task-2",
        pet_id=pet.pet_id,
        title="Feed dinner",
        category="feeding",
        duration=10,
        priority="medium",
    )

    pet.add_task(task)

    assert len(pet.get_tasks()) == initial_count + 1
