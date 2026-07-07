from pawpal_system import Owner, Pet, Task, Schedule


def main() -> None:
    # Create the owner
    owner1 = Owner(
        owner_id="owner-001",
        name="Avery",
        contact="avery@example.com",
        available_time=120,
        preferences={"preferred_time": "morning"},
    )
    owner2 = Owner(
        owner_id="owner-002",
        name="Sayuri",
        contact="sayuri@example.com",
        available_time=120,
        preferences={"preferred_time": "evening"},
    )
    

    # Create two pets
    dog = Pet(
        pet_id="pet-001",
        owner_id=owner1.owner_id,
        name="Mochi",
        species="dog",
        breed="Shiba Inu",
        age=3,
    )

    cat = Pet(
        pet_id="pet-002",
        owner_id=owner1.owner_id,
        name="Luna",
        species="cat",
        breed="Domestic Shorthair",
        age=2,
    )
    cat1 = Pet(
        pet_id="pet-003",
        owner_id=owner2.owner_id,
        name="Michi",
        species="cat",
        breed="British Shorthair",
        age=4,
    )

    owner1.add_pet(dog)
    owner1.add_pet(cat)
    owner2.add_pet(cat1)

    # Add tasks to the pets
    walk_task = Task(
        task_id="task-001",
        pet_id=dog.pet_id,
        title="Morning walk",
        category="walk",
        duration=30,
        priority="high",
        recurring=True,
        time_preference="morning",
    )

    feed_task = Task(
        task_id="task-002",
        pet_id=cat.pet_id,
        title="Evening feeding",
        category="feeding",
        duration=15,
        priority="medium",
        recurring=True,
        time_preference="evening",
    )

    grooming_task = Task(
        task_id="task-003",
        pet_id=dog.pet_id,
        title="Brush fur",
        category="grooming",
        duration=20,
        priority="low",
        recurring=False,
        notes="Brush more carefully around the collar area.",
    )

    grooming_task1 = Task(
        task_id="task-004",
        pet_id=cat1.pet_id,
        title="trim nails",
        category="grooming",
        duration=15,
        priority="low",
        recurring=False,
        notes="Trim nails carefully to avoid cutting too short.",
    )
    dog.add_task(walk_task)
    cat.add_task(feed_task)
    dog.add_task(grooming_task)
    cat1.add_task(grooming_task1)

    # Build the schedule from all pet tasks
    all_tasks = dog.get_tasks() + cat.get_tasks()
    schedule = Schedule(owner=owner1, tasks=all_tasks)
    schedule.generate_schedule()

    # Print today's schedule to the terminal
    print(owner1.display_info())
    print("Pets:")
    for pet in owner1.get_pets():
        print(f"  - {pet.display_info()}")
    print()
    print("Today's schedule:")
    print(schedule.display_plan())

    all_tasks = cat1.get_tasks()
    schedule = Schedule(owner=owner2, tasks=all_tasks)
    schedule.generate_schedule()


    print(owner2.display_info())
    print("Pets:")
    for pet in owner2.get_pets():
        print(f"  - {pet.display_info()}")
    print()
    print("Today's schedule:")
    print(schedule.display_plan())

if __name__ == "__main__":
    main()
