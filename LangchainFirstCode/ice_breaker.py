# llm_service.py
import logging
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Configuration
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    # Use logger for consistency
    logger = logging.getLogger(__name__)  # Define logger before potential early exit
    logger.critical("GOOGLE_API_KEY environment variable not set. Exiting.")
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

# Logging Setup
# Ensure logger is initialized *after* any potential early exit config/checks
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
# Basic config is done once, potentially in the main script or a config file.
# Just getting the logger instance here is sufficient if basicConfig is elsewhere.
# If running this script standalone, you might need basicConfig here too.
# Let's assume basicConfig is handled in the main script (`processor.py` will do it).
logger = logging.getLogger(__name__)


# --- LLM Setup ---
llm_model: Optional[ChatGoogleGenerativeAI] = None
try:
    llm_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key,
        temperature=0.1,
    )
    logger.info("Initialized ChatGoogleGenerativeAI model.")
except Exception as e:
    logger.critical(f"Failed to initialize Google AI LLM model: {e}", exc_info=True)
    # If the LLM is critical for the script, raise the exception
    raise


def invoke_llm_with_prompt(
    prompt_template: PromptTemplate, input_variables: Dict[str, Any]
) -> Optional[str]:
    """
    Invokes the LLM using a given prompt template and input variables.

    Args:
        prompt_template: The Langchain PromptTemplate to use.
        input_variables: A dictionary containing the variables required by the prompt_template.

    Returns:
        The raw string output from the model, or None if an error occurs or output is empty.
    """
    if llm_model is None:
        logger.error("LLM model not initialized. Cannot invoke.")
        return None

    try:
        # Format the prompt using the provided template and variables
        prompt_value = prompt_template.format_prompt(**input_variables)

        logger.debug(
            f"Invoking LLM with prompt for inputs: {list(input_variables.keys())}"
        )
        output = llm_model.invoke(prompt_value)
        raw_output = output.content.strip()

        if not raw_output:
            logger.warning(
                f"LLM returned empty content for inputs: {list(input_variables.keys())}"
            )
            return None

        logger.debug(f"LLM invocation successful. Output length: {len(raw_output)}")
        return raw_output

    except Exception as e:
        logger.error(
            f"Error during LLM invocation for inputs {list(input_variables.keys())}: {e}",
            exc_info=True,
        )
        return None
