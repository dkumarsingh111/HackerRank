"""
This program is build with Flan-T5-XL LLM to be able to answer the final question using the output from the previous questions as in-context learning/few-shot learning. 

Consider three related questions from a search session: Question 1, Question 2, Question 3
1. Answer to Question 1 needs to be generated. 
2. Answer to Question 2 needs to be generated with the answer to Question 1 as one-shot example / context. 
3. Answer to Question 3 needs to be generated with the answer to Question 2 as one-shot example / context.
4. Answer to Question 3 will be either YES or NO and nothing else.


> The program accepts three parameters provided as a command line input. 
> The three inputs represent the questions.
> The output of the first two question is Generation based whereas the last question output is deterministic i.e. its either YES or NO.
> Output should be in upper-case: YES or NO
> There should be no additional output including any warning messages in the terminal.
> Remember that your output will be tested against test cases, therefore any deviation from the test cases will be considered incorrect during evaluation.


Syntax: python template.py <string> <string> <string> 

The following example is given for your reference:

 Terminal Input: python template.py "Who is Rabindranath Tagore?" "Where was he born?" "Is it in America?"
Terminal Output: NO

 Terminal Input: python template.py "Who is Rabindranath Tagore?" "Where was he born?" "Is it in India?"
Terminal Output: YES

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

##### You may comment this section to see verbose -- but you must un-comment this before final submission. ######
transformers.logging.set_verbosity_error()
transformers.utils.logging.disable_progress_bar()
#################################################################################################################

"""
* * * Changes allowed from here  * * * 
"""

def llm_function(model,tokenizer,questions):
    '''
    The steps are given for your reference:

    1. Generate answer for the first question.
    2. Generate answer for the second question use the answer for first question as context.
    3. Generate a deterministic output either 'YES' or 'NO' for the third question using the context from second question.  
    5. Clean output and return.
    6. Output is case-sensative: YES or NO
    Note: The model (Flan-T5-XL) and tokenizer is already initialized. Do not modify that section.
    '''

    # Unpack the three related questions.
    question_1, question_2, question_3 = questions

    # Use deterministic generation throughout for reproducible evaluation.
    device = next(model.parameters()).device

    def generate_answer(prompt, max_new_tokens):
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        inputs = {key: value.to(device) for key, value in inputs.items()}

        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                num_beams=1
            )

        return tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True
        ).strip()

    # Step 1: Generate the answer to Question 1.
    answer_1 = generate_answer(
        "Answer the following question briefly and factually.\n"
        "Question: " + question_1 + "\n"
        "Answer:",
        64
    )

    # Step 2: Use Question 1 and its generated answer as the
    # one-shot/in-context example for Question 2.
    answer_2 = generate_answer(
        "Use the previous question and answer as context to answer the next "
        "related question. Resolve references such as he, she, it, there, "
        "this, and that from the context.\n\n"
        "Previous question: " + question_1 + "\n"
        "Previous answer: " + answer_1 + "\n\n"
        "Question: " + question_2 + "\n"
        "Answer:",
        64
    )

    # Step 3: Use Question 2 and its answer as the one-shot/in-context
    # example. Constrain generation to a single token so that the model
    # produces only the requested binary answer.
    final_answer = generate_answer(
        "Answer the final question using the previous questions and answers as context. "
        "Answer with exactly YES or NO and nothing else.\n\n"
        "Question 1: " + question_1 + "\n"
        "Answer 1: " + answer_1 + "\n\n"
        "Question 2: " + question_2 + "\n"
        "Answer 2: " + answer_2 + "\n\n"
        "Final question: " + question_3 + "\n"
        "Answer only YES or NO:",
        5
    )

    # Clean the generated text and guarantee the required output contract.
    cleaned = re.sub(r"[^A-Za-z]", " ", final_answer).upper()
    words = cleaned.split()

    if "YES" in words:
        final_output = "YES"
    elif "NO" in words:
        final_output = "NO"
    else:
        # A deterministic fallback prompt is used only if the first binary
        # generation did not contain an explicit YES/NO token.
        fallback = generate_answer(
            "Based on this context, answer the question with only YES or NO.\n"
            "Context: " + answer_2 + "\n"
            "Question: " + question_3 + "\n"
            "Answer:",
            3
        )
        fallback_words = re.sub(r"[^A-Za-z]", " ", fallback).upper().split()
        final_output = "YES" if "YES" in fallback_words else "NO"

    return final_output

"""
ALERT: * * * No changes are allowed below this comment  * * *
"""

if __name__ == '__main__':

    question_a = sys.argv[1].strip()
    question_b = sys.argv[2].strip()
    question_c = sys.argv[3].strip()

    questions = [question_a, question_b, question_c]
    ##################### Loading Model and Tokenizer ########################
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xl")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl")
    ##########################################################################

    """  Call to function that will perform the computation. """
    torch.manual_seed(42)
    out = llm_function(model,tokenizer,questions)
    print(out.strip())

    """ End to call """