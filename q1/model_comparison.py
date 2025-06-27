import os
import typer
import asyncio
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.prompt import Prompt, IntPrompt
from dotenv import load_dotenv
from typing import Optional
from enum import Enum
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from openai import OpenAI
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize console
console = Console()

# Validate API keys
def validate_api_keys():
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")
    
    if not openai_key:
        console.print("[bold red]Warning:[/] OPENAI_API_KEY not found in .env file")
    if not gemini_key:
        console.print("[bold red]Warning:[/] GOOGLE_API_KEY not found in .env file")
    
    return openai_key, gemini_key

# Initialize clients after validation
openai_key, gemini_key = validate_api_keys()
openai_client = OpenAI(api_key=openai_key) if openai_key else None

# Configure Gemini
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    gemini_model = None

class ModelType(str, Enum):
    BASE = "base"
    INSTRUCT = "instruct"
    FINE_TUNED = "fine-tuned"

class ModelProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"  # Changed from ANTHROPIC to GEMINI
    HUGGINGFACE = "huggingface"

# Model characteristics
MODEL_INFO = {
    "gpt-3.5-turbo": {
        "type": ModelType.INSTRUCT,
        "provider": ModelProvider.OPENAI,
        "description": "Instruction-tuned model optimized for dialogue",
        "context_window": 4096,
        "fine_tuning": "Trained on dialogue and instruction following"
    },
    "gemini-2.0-flash": {  # Updated to Gemini 2.0 Flash
        "type": ModelType.INSTRUCT,
        "provider": ModelProvider.GEMINI,
        "description": "Google's fastest Gemini model optimized for quick responses",
        "context_window": 32768,
        "fine_tuning": "Optimized for speed while maintaining high quality responses"
    },
    "TinyLlama-1.1B-Chat": {
        "type": ModelType.BASE,
        "provider": ModelProvider.HUGGINGFACE,
        "description": "Compact chat-oriented language model",
        "context_window": 2048,
        "fine_tuning": "Base model with chat fine-tuning"
    }
}

async def call_openai(prompt: str) -> tuple[str, int]:
    """Call OpenAI API and return response and token count."""
    if not openai_client:
        raise ValueError("OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file.")
    
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content, response.usage.total_tokens

async def call_gemini(prompt: str) -> tuple[str, int]:
    """Call Gemini API and return response and token count."""
    if not gemini_model:
        raise ValueError("Google API key not configured. Please add GOOGLE_API_KEY to your .env file.")
    
    try:
        response = gemini_model.generate_content(prompt)
        
        # Gemini doesn't provide token count directly, so we'll estimate
        # by counting words (rough approximation)
        token_estimate = len(prompt.split()) + len(response.text.split())
        
        return response.text, token_estimate
    except Exception as e:
        raise ValueError(f"Error calling Gemini API: {str(e)}")

def call_huggingface(prompt: str) -> tuple[str, int]:
    """Use local HuggingFace model and return response and token count."""
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Format the prompt in chat format
    chat_prompt = f"<|system|>You are a helpful AI assistant that provides accurate and concise answers.</s><|user|>{prompt}</s><|assistant|>"
    
    # Tokenize with proper attention mask
    inputs = tokenizer(chat_prompt, 
                      return_tensors="pt", 
                      padding=True,
                      add_special_tokens=True)
    
    # Create attention mask
    attention_mask = inputs['input_ids'].ne(tokenizer.pad_token_id)
    input_token_count = len(inputs.input_ids[0])
    
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=attention_mask,
            max_length=input_token_count + 100,  # Limit response length
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,  # Add some randomness but keep responses focused
            top_p=0.9,
            repetition_penalty=1.2  # Prevent repetitive outputs
        )
    
    # Decode only the new tokens (response)
    response = tokenizer.decode(outputs[0][input_token_count:], skip_special_tokens=True)
    output_token_count = len(outputs[0])
    
    return response.strip(), input_token_count + output_token_count

def display_model_info(model_name: str):
    """Display information about the selected model."""
    info = MODEL_INFO[model_name]
    table = Table(title=f"{model_name} Characteristics")
    table.add_column("Attribute", style="cyan")
    table.add_column("Value", style="magenta")
    
    for key, value in info.items():
        table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(table)

def display_available_models():
    """Display available models and their types."""
    table = Table(title="Available Models")
    table.add_column("Number", style="cyan")
    table.add_column("Model", style="green")
    table.add_column("Type", style="magenta")
    table.add_column("Provider", style="yellow")
    
    for i, (model, info) in enumerate(MODEL_INFO.items(), 1):
        table.add_row(
            str(i),
            model,
            info["type"],
            info["provider"]
        )
    
    console.print(table)
    return len(MODEL_INFO)

async def interactive_mode():
    """Run the model comparison tool in interactive mode."""
    console.print("\n[bold cyan]Welcome to the LLM Model Comparison Tool![/]\n")
    
    while True:
        # Display available models
        num_models = display_available_models()
        
        # Get user input
        try:
            model_num = IntPrompt.ask(
                "\nSelect a model number (or 0 to exit)",
                choices=[str(i) for i in range(num_models + 1)]
            )
            
            if model_num == 0:
                console.print("\n[bold green]Thank you for using the Model Comparison Tool![/]\n")
                break
            
            # Get the selected model
            model_name = list(MODEL_INFO.keys())[model_num - 1]
            provider = MODEL_INFO[model_name]["provider"]
            
            # Get the prompt
            prompt = Prompt.ask("\nEnter your prompt")
            
            console.print(f"\n[bold cyan]Processing prompt:[/] {prompt}\n")
            
            try:
                if provider == ModelProvider.OPENAI:
                    response, tokens = await call_openai(prompt)
                elif provider == ModelProvider.GEMINI:  # Changed from ANTHROPIC to GEMINI
                    response, tokens = await call_gemini(prompt)
                else:
                    response, tokens = call_huggingface(prompt)
                
                # Display model information
                display_model_info(model_name)
                
                # Display response
                console.print("\n[bold green]Response:[/]")
                console.print(response)
                
                # Display token usage
                console.print(f"\n[bold yellow]Token usage:[/] {tokens}")
                
            except Exception as e:
                console.print(f"[bold red]Error:[/] {str(e)}")
            
            # Ask if user wants to continue
            if not Prompt.ask("\nWould you like to try another prompt?", choices=["y", "n"]) == "y":
                console.print("\n[bold green]Thank you for using the Model Comparison Tool![/]\n")
                break
                
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold green]Thank you for using the Model Comparison Tool![/]\n")
            break

async def main(
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Run in interactive mode"),
    prompt: Optional[str] = typer.Option(None, help="Input prompt for the models"),
    model_type: Optional[ModelType] = typer.Option(None, help="Type of model to use"),
    provider: Optional[ModelProvider] = typer.Option(None, help="Model provider to use"),
    show_viz: bool = typer.Option(False, help="Show token usage visualization")
):
    """
    Compare different types of language models and their responses.
    """
    if interactive:
        await interactive_mode()
        return
        
    if not prompt or not provider:
        console.print("[bold red]Error:[/] Both --prompt and --provider are required in non-interactive mode.")
        raise typer.Exit(1)
    
    try:
        if provider == ModelProvider.OPENAI:
            response, tokens = await call_openai(prompt)
            model_name = "gpt-3.5-turbo"
        elif provider == ModelProvider.GEMINI:
            response, tokens = await call_gemini(prompt)
            model_name = "gemini-2.0-flash"  # Updated model name
        else:
            response, tokens = call_huggingface(prompt)
            model_name = "TinyLlama-1.1B-Chat"
        
        # Display model information
        display_model_info(model_name)
        
        # Display response
        console.print("\n[bold green]Response:[/]")
        console.print(response)
        
        # Display token usage
        console.print(f"\n[bold yellow]Token usage:[/] {tokens}")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

if __name__ == "__main__":
    app = typer.Typer()
    
    @app.command()
    def run(
        interactive: bool = typer.Option(False, "--interactive", "-i", help="Run in interactive mode"),
        prompt: Optional[str] = typer.Option(None, help="Input prompt for the models"),
        model_type: Optional[ModelType] = typer.Option(None, help="Type of model to use"),
        provider: Optional[ModelProvider] = typer.Option(None, help="Model provider to use"),
        show_viz: bool = typer.Option(False, help="Show token usage visualization")
    ):
        """
        Compare different types of language models and their responses.
        """
        asyncio.run(main(interactive, prompt, model_type, provider, show_viz))
    
    app() 