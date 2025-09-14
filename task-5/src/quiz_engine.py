import requests
import html
import threading
import time
import random
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

console = Console()

CATEGORY_URL = "https://opentdb.com/api_category.php"
QUESTION_URL = "https://opentdb.com/api.php"

class QuizEngine:
    def __init__(self, profile, num_questions, difficulty, time_limit, category_id):
        self.profile = profile
        self.num_questions = num_questions
        self.difficulty = difficulty
        self.time_limit = time_limit
        self.category_id = category_id
        self.questions = []
        self.score = profile.score
        self.user_answer = None

    def fetch_questions(self):
        params = {
            "amount": self.num_questions,
            "category": self.category_id,
            "difficulty": self.difficulty,
            "type": "multiple"
        }

        try:
            response = requests.get(QUESTION_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data["response_code"] == 0:
                self.questions = data["results"]
            else:
                console.print("[red]Failed to fetch questions from API.[/red]")
        except requests.RequestException as e:
            console.print(f"[red]Error fetching questions: {e}[/red]")

    def ask_question(self, question_data):
        question = html.unescape(question_data["question"])
        correct_answer = html.unescape(question_data["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in question_data["incorrect_answers"]]

        all_answers = incorrect_answers + [correct_answer]
        random.shuffle(all_answers)

        console.print("\n[bold blue]Q:[/bold blue]", question)

        for idx, option in enumerate(all_answers, 1):
            console.print(f"  {idx}. {option}")

        self.user_answer = None

        def get_input():
            try:
                choice = Prompt.ask(f"[grey]You have {self.time_limit} seconds. Enter your answer (1-{len(all_answers)}):[/grey]")
                self.user_answer = all_answers[int(choice) - 1]
            except (ValueError, IndexError):
                self.user_answer = None

        input_thread = threading.Thread(target=get_input)
        input_thread.daemon = True
        input_thread.start()
        input_thread.join(timeout=self.time_limit)

        if self.user_answer == correct_answer:
            console.print("[green]Correct![/green]")
            self.profile.increase_score()
            return True
        else:
            console.print(f"[red]Wrong![/red] The correct answer was: [bold]{correct_answer}[/bold]")
            return False

    def run(self):
        self.fetch_questions()
        if not self.questions:
            console.print("[red]No questions available. Try again later.[/red]")
            return

        correct_count = 0
        for i, question in enumerate(self.questions, 1):
            console.print(f"\n[bold]Question {i} of {self.num_questions}[/bold]")
            if self.ask_question(question):
                correct_count += 1

        console.rule("[bold green]Quiz Complete[/bold green]")
        console.print(f"\n[bold cyan]Final Score: {correct_count} / {self.num_questions}[/bold cyan]")
        console.print(f"[yellow]Total Points: {self.profile.score}[/yellow]")
        self.profile.save()
