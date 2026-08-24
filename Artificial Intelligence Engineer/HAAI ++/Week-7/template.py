"""
This program is build with Flan-T5-XL LLM to be able to answer a question in YES/NO using the provided context as in-context learning. 

> The program accepts two parameters provided as a command line input. 
> The two inputs represent the context and the question.
> The question output is deterministic i.e. its either YES or NO. You are required to use logits to extract the output.
> Output should be in upper-case: YES or NO
> There should be no additional output including any warning messages in the terminal.
> Remember that your output will be tested against test cases, therefore any deviation from the test cases will be considered incorrect during evaluation.
> Note that the assignment and evaluation test cases are carefully sampled from the model itself, eliminating any chance of hallucination.

Syntax: python template.py <CONTEXT> <QUESTION>

The following example is given for your reference:

 Terminal Input: python assignment.py 'Albert has been working on his project all week. He finished the final report today and submitted it to his manager before the deadline.' 'Did Albert submit his project report on time?'
Terminal Output: YES

 Terminal Input: python assignment.py 'Albert has been working on his project all week. He finished the final report today and submitted it to his manager after the deadline.' 'Did Albert submit his project report on time?'
Terminal Output: NO

 Terminal Input: 'John started watered his plants every morning this week.' 'Did John water his plants yesterday morning?'
Terminal Output: YES

 Terminal Input: 'John started watered his plants every morning this week.' 'Did John water his plants last month?'
Terminal Output: NO

You are expected to create some examples of your own to test the correctness of your approach.

ALL THE BEST!!
"""

"""
ALERT: * * * No changes are allowed to import statements  * * *
"""
import sys
import torch
import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration
import re

#####
transformers.logging.set_verbosity_error()
transformers.utils.logging.disable_progress_bar()
"""
* * * Changes allowed from here  * * * 
"""

def llm_function(model,tokenizer,context,question): 

    # Generate a deterministic output either 'YES' or 'NO' answering the question using the provided context

    '''
    1. Engineer the prompt using the query and the context.
    2. Tokenize the prompt.
    3. Generate output for the prompt.
    4. Extract the logit values to determine the output
    5. Format the output to be exactly YES or NO. 
    
    Remember that there should be no additional output including any warning messages in the terminal.
    '''

     # In-context prompt
    prompt = (
        "Answer the question using only the given context.\n"
        "Respond with exactly YES or NO.\n\n"
        f"Context: {context}\n"
        f"Question: {question}\n"
        "Answer:"
    )

    # Tokenize
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    # Decoder starts with pad token for T5
    decoder_input_ids = torch.tensor([[model.config.decoder_start_token_id]])

    with torch.no_grad():
        outputs = model(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            decoder_input_ids=decoder_input_ids
        )

    # First-token logits
    logits = outputs.logits[0, -1]

    # Candidate token ids
    yes_ids = tokenizer.encode("YES", add_special_tokens=False)
    no_ids = tokenizer.encode("NO", add_special_tokens=False)

    # Compare logits of first token
    yes_score = logits[yes_ids[0]].item()
    no_score = logits[no_ids[0]].item()

    final_output = "YES" if yes_score >= no_score else "NO"

    return final_output


"""
ALERT: * * * No changes are allowed below this comment  * * *
"""
if __name__ == '__main__':

    context = sys.argv[1].strip().lower()
    question = sys.argv[2].strip().lower()

    ##################### Loading Model and Tokenizer ########################
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xl")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl")
    ##########################################################################

    """  Call to function that will perform the computation. """
    torch.manual_seed(42)
    out = llm_function(model,tokenizer,context,question)
    print(out.strip())

    """ End to call """