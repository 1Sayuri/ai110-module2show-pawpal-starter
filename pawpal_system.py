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
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from the owner's list by ID."""
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def get_pets(self) -> List["Pet"]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_pet_by_id(self, pet_id: str) -> Optional["Pet"]:
        """Return a pet by its unique ID if it exists."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def display_info(self) -> str:
        """Return a short summary of the owner."""
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
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the pet by its ID."""
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def get_tasks(self) -> List["Task"]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def display_info(self) -> str:
        """Return a short summary of the pet."""
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
        recurrence: Optional[str] = None,
        time_preference: Optional[str] = None,
        time: Optional[str] = None,
        notes: str = "",
    ) -> None:
        self.task_id = task_id
        self.pet_id = pet_id
        self.title = title
        self.category = category
        self.duration = duration
        self.priority = priority.lower()
        self.recurring = recurring
        self.recurrence = recurrence.lower() if recurrence else None
        self.time_preference = time_preference or time
        self.time = time or time_preference
        self.notes = notes
        self.is_complete = False

    def get_priority_weight(self) -> int:
        """Return a numeric value for the task's priority."""
        weights = {"low": 1, "medium": 2, "high": 3}
        return weights.get(self.priority, 2)

    def mark_complete(self, pet: Optional["Pet"] = None) -> Optional["Task"]:
        """Mark the task as completed and create a follow-up task for recurring daily/weekly items."""
        self.is_complete = True
        if not self.recurring or self.recurrence not in {"daily", "weekly"}:
            return None

        if pet is None:
            return None

        next_task = Task(
            task_id=f"{self.task_id}-next",
            pet_id=self.pet_id,
            title=self.title,
            category=self.category,
            duration=self.duration,
            priority=self.priority,
            recurring=True,
            recurrence=self.recurrence,
            time_preference=self.time_preference,
            time=self.time,
            notes=self.notes,
        )
        pet.add_task(next_task)
        return next_task

    def display_info(self) -> str:
        """Return a short summary of the task."""
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
        """Create a simple ordered daily schedule from current tasks."""
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
        """Sort tasks from highest to lowest priority."""
        return sorted(self.tasks, key=lambda task: task.get_priority_weight(), reverse=True)

    def sort_tasks_by_time(self) -> List[Task]:
        """Sort tasks chronologically by their assigned time attribute."""
        return sorted(self.tasks, key=self._task_time_value)

    def _task_time_value(self, task: Task) -> int:
        """Convert a task's time string into a comparable minute value."""
        time_value = getattr(task, "time", None) or getattr(task, "time_preference", None)
        if not time_value:
            return 24 * 60
        if isinstance(time_value, str):
            try:
                hours_text, minutes_text = time_value.split(":", 1)
                hours = int(hours_text)
                minutes = int(minutes_text)
            except ValueError:
                return 24 * 60
            return hours * 60 + minutes
        return int(time_value)

    def filter_tasks_by_duration(self, available_time: int) -> List[Task]:
        """Return tasks that fit within the available time."""
        return [task for task in self.tasks if task.duration <= available_time]

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        filtered_tasks = self.tasks
        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.is_complete is completed]
        if pet_name is not None:
            pet_name_lower = pet_name.lower()
            filtered_tasks = [
                task for task in filtered_tasks if self._task_matches_pet_name(task, pet_name_lower)
            ]
        return filtered_tasks

    def _task_matches_pet_name(self, task: Task, pet_name_lower: str) -> bool:
        """Return True when the task belongs to a pet with the given name."""
        for pet in self.owner.get_pets():
            if pet.pet_id == task.pet_id and pet.name.lower() == pet_name_lower:
                return True
        return False

    def check_conflicts(self) -> str:
        """Return a warning message when tasks overlap at the same time."""
        seen: set[str] = set()
        conflict_titles: List[str] = []

        for index, task in enumerate(self.tasks):
            task_time = self._task_time_value(task)
            for other_task in self.tasks[index + 1 :]:
                if other_task.task_id in seen:
                    continue
                if self._task_time_value(other_task) == task_time:
                    conflict_pair = sorted({task.task_id, other_task.task_id})
                    if conflict_pair[0] == task.task_id:
                        conflict_titles.append(f"{task.title} and {other_task.title}")
                    seen.add(task.task_id)
                    seen.add(other_task.task_id)

        if not conflict_titles:
            return "No conflicts detected."

        return "Warning: overlapping tasks detected at the same time: " + "; ".join(conflict_titles)

    def assign_time_slots(self) -> List[dict]:
        """Assign the current tasks to time slots in the schedule."""
        return self.daily_schedule

    def get_schedule(self) -> List[dict]:
        """Return the current daily schedule."""
        return self.daily_schedule

    def explain_reasoning(self) -> str:
        """Explain why the schedule was built in this order."""
        return "Tasks are ordered by priority and basic time constraints."

    def display_plan(self) -> str:
        """Return the schedule as a readable string."""
        if not self.daily_schedule:
            return "No schedule generated yet."
        lines = [f"Daily plan for {self.owner.name}:"]
        for item in self.daily_schedule:
            lines.append(
                f"- {item['title']} ({item['duration']} mins, priority: {item['priority']})"
            )
        return "\n".join(lines)

