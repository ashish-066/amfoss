from user_profile import UserProfile
from quiz_engine import QuizEngine
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from utils import get_categories

console = Console()

def main():
    console.print("[bold blue]Welcome to TimeTickQuiz Pro![/bold blue]\n")

    username = Prompt.ask("Enter your username").strip()
    user = UserProfile(username)
    
    console.print(f"Hello, [bold green]{username}[/bold green]! Your current score is [bold yellow]{user.score}[/bold yellow]. Difficulty: [bold magenta]{user.difficulty}[/bold magenta]\n")

    num_questions = IntPrompt.ask("How many questions do you want (1-20)?", default=5, choices=[str(i) for i in range(1, 21)])

    time_limit = IntPrompt.ask("Set time limit per question (seconds, 10-30)", default=15, choices=[str(i) for i in range(10, 31)])

    difficulty = Prompt.ask("Choose difficulty (easy, medium, hard)", choices=["easy", "medium", "hard"], default=user.difficulty)

    categories = get_categories()
    if not categories:
        console.print("[red]Failed to load categories, using default 'General Knowledge'[/red]")
        category_id = 9  
    else:
        console.print("\n[bold cyan]Available Categories:[/bold cyan]")
        for cat in categories:
            console.print(f"{cat['id']}: {cat['name']}")
        category_id = IntPrompt.ask("Pick a category by ID", choices=[str(cat['id']) for cat in categories], default="9")

    quiz = QuizEngine(
            profile=user,  
        num_questions=num_questions,
        category_id=category_id,
        difficulty=difficulty,
        time_limit=time_limit,
    )

    quiz.run()

    console.print(f"\n[bold green]Quiz over![/bold green] Your final score is: [bold yellow]{user.score}[/bold yellow]")

if __name__ == "__main__":
    main()
