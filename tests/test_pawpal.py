from pawpal_system import Owner, Pet, Schedule, Task


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


def test_sorting_correctness_returns_tasks_in_chronological_order():
    owner = Owner(owner_id="owner-1", name="Jordan", available_time=120)
    morning_task = Task(
        task_id="task-1",
        pet_id="pet-1",
        title="Morning walk",
        category="walk",
        duration=20,
        priority="high",
        time="08:00",
    )
    evening_task = Task(
        task_id="task-2",
        pet_id="pet-1",
        title="Feed dinner",
        category="feeding",
        duration=10,
        priority="medium",
        time="18:00",
    )

    schedule = Schedule(owner=owner, tasks=[evening_task, morning_task])

    ordered_tasks = schedule.sort_tasks_by_time()

    assert [task.title for task in ordered_tasks] == ["Morning walk", "Feed dinner"]


def test_schedule_can_filter_tasks_by_completion_and_pet_name():
    owner = Owner(owner_id="owner-1", name="Jordan", available_time=120)
    mochi = Pet(pet_id="pet-1", owner_id=owner.owner_id, name="Mochi", species="dog")
    luna = Pet(pet_id="pet-2", owner_id=owner.owner_id, name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    completed_task = Task(
        task_id="task-1",
        pet_id=mochi.pet_id,
        title="Morning walk",
        category="walk",
        duration=20,
        priority="high",
    )
    completed_task.mark_complete()
    pending_task = Task(
        task_id="task-2",
        pet_id=luna.pet_id,
        title="Feed dinner",
        category="feeding",
        duration=10,
        priority="medium",
    )

    schedule = Schedule(owner=owner, tasks=[completed_task, pending_task])

    filtered_tasks = schedule.filter_tasks(completed=True, pet_name="Mochi")

    assert [task.title for task in filtered_tasks] == ["Morning walk"]


def test_recurrence_logic_creates_new_task_for_following_day():
    pet = Pet(pet_id="pet-1", owner_id="owner-1", name="Mochi", species="dog")
    task = Task(
        task_id="task-1",
        pet_id=pet.pet_id,
        title="Morning walk",
        category="walk",
        duration=20,
        priority="high",
        recurring=True,
        recurrence="daily",
        time="08:00",
    )
    pet.add_task(task)

    next_task = task.mark_complete(pet=pet)

    assert task.is_complete is True
    assert next_task is not None
    assert next_task.is_complete is False
    assert next_task.recurrence == "daily"
    assert len(pet.get_tasks()) == 2


def test_conflict_detection_flags_duplicate_times():
    owner = Owner(owner_id="owner-1", name="Jordan", available_time=120)
    mochi = Pet(pet_id="pet-1", owner_id=owner.owner_id, name="Mochi", species="dog")
    luna = Pet(pet_id="pet-2", owner_id=owner.owner_id, name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    first_task = Task(
        task_id="task-1",
        pet_id=mochi.pet_id,
        title="Morning walk",
        category="walk",
        duration=20,
        priority="high",
        time="08:00",
    )
    second_task = Task(
        task_id="task-2",
        pet_id=mochi.pet_id,
        title="Feed breakfast",
        category="feeding",
        duration=15,
        priority="medium",
        time="08:00",
    )
    third_task = Task(
        task_id="task-3",
        pet_id=luna.pet_id,
        title="Play session",
        category="play",
        duration=10,
        priority="medium",
        time="08:00",
    )

    schedule = Schedule(owner=owner, tasks=[first_task, second_task, third_task])

    warning_message = schedule.check_conflicts()

    assert warning_message.startswith("Warning:")
    assert "Morning walk" in warning_message
    assert "Feed breakfast" in warning_message
    assert "Play session" in warning_message
