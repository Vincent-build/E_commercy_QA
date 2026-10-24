from langchain_core.prompts import PromptTemplate
from pathlib import Path

def load_prompt(name:str)->PromptTemplate:

    path_ = Path(__file__).parents[2] / "qa_process" / "prompt_templates" / f"{name}.prompt"

    return PromptTemplate.from_file(path_)


