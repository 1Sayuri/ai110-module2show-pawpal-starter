from __future__ import annotations

from typing import List, Optional


class Owner:
    """Represents a pet owner and the pets they care for."""

    def __init__(
        self,
        owner_id: str,
        name: str,
        contact: str = "",
        available_time: int = 0,
        preferences: Optional[dict] = None,
    ) -> None:
        self.owner_id = owner_id
        self.name = name
        self.contact = contact
        self.available_time = available_time
        self.preferences = preferences or {}
        self.pets: List["Pet"] = []

    def add_pet(self, pet: "Pet") -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def get_pets(self) -> List["Pet"]:
        return self.pets

    def get_pet_by_id(self, pet_id: str) -> Optional["Pet"]:
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def display_info(self) -> str:
        return f"Owner: {self.name} ({self.owner_id})"


class Pet:
    """Represents a pet belonging to an owner."""

    def __init__(
        self,
        pet_id: str,
        owner_id: str,
        name: str,
        species: str,
        breed: str = "",
        age: Optional[int] = None,
    ) -> None:
        self.pet_id = pet_id
        self.owner_id = owner_id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.tasks: List["Task"] = []

    def add_task(self, task: "Task") -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def get_tasks(self) -> List["Task"]:
        return self.tasks

    def display_info(self) -> str:
        return f"Pet: {self.name} ({self.species})"


class Task:
    """Represents a single pet care task."""

    def __init__(
        self,
        task_id: str,
        pet_id: str,
        title: str,
        category: str,
        duration: int,
        priority: str = "medium",
        recurring: bool = False,
        time_preference: Optional[str] = None,
        notes: str = "",
    ) -> None:
        self.task_id = task_id
        self.pet_id = pet_id
        self.title = title
        self.category = category
        self.duration = duration
        self.priority = priority.lower()
        self.recurring = recurring
        self.time_preference = time_preference
        self.notes = notes

    def get_priority_weight(self) -> int:
        weights = {"low": 1, "medium": 2, "high": 3}
        return weights.get(self.priority, 2)

    def display_info(self) -> str:
        return f"Task: {self.title} ({self.category}) - {self.duration} mins"


class Schedule:
    """Builds and stores a daily care schedule for an owner."""

    def __init__(
        self,
        owner: Owner,
        tasks: Optional[List[Task]] = None,
        day_start_time: str = "08:00",
        day_end_time: str = "20:00",
    ) -> None:
        self.owner = owner
        self.tasks = tasks or []
        self.daily_schedule: List[dict] = []
        self.day_start_time = day_start_time
        self.day_end_time = day_end_time

    def generate_schedule(self) -> List[dict]:
        self.daily_schedule = []
        sorted_tasks = self.sort_tasks_by_priority()
        for task in sorted_tasks:
            self.daily_schedule.append(
                {
                    "title": task.title,
                    "priority": task.priority,
                    "duration": task.duration,
                }
            )
        return self.daily_schedule

    def sort_tasks_by_priority(self) -> List[Task]:
        return sorted(self.tasks, key=lambda task: task.get_priority_weight(), reverse=True)

    def filter_tasks_by_duration(self, available_time: int) -> List[Task]:
        return [task for task in self.tasks if task.duration <= available_time]

    def check_conflicts(self) -> List[Task]:
        return []

    def assign_time_slots(self) -> List[dict]:
        return self.daily_schedule

    def get_schedule(self) -> List[dict]:
        return self.daily_schedule

    def explain_reasoning(self) -> str:
        return "Tasks are ordered by priority and basic time constraints."

    def display_plan(self) -> str:
        if not self.daily_schedule:
            return "No schedule generated yet."
        lines = [f"Daily plan for {self.owner.name}:"]
        for item in self.daily_schedule:
            lines.append(
                f"- {item['title']} ({item['duration']} mins, priority: {item['priority']})"
            )
        return "\n".join(lines)
