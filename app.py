# Required imports
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from ctransformers import AutoModelForCausalLM

# Step 1: Load the GGML quantized Llama 2 model using ctransformers
model_path = "./llama-2-7b-chat.ggmlv3.q8_0.bin"  # Your GGML model file

# Use ctransformers to load the model
model = AutoModelForCausalLM.from_pretrained(model_path, model_type="llama")  # specify the correct model type

# Step 2: Create a prompt template
mytemplate = """
you are an expert Quiz maker 
Create a quiz with {num_quiz} {quiz_type} questions about following context: {quiz_context} 
"""

prompt_template = PromptTemplate.from_template(mytemplate)

# Create the LLM chain
chain = LLMChain(llm=model, prompt=prompt_template)

# Step 3: Run the chain with your inputs
response = chain.run(num_quiz=5, quiz_type="multiple-choice", quiz_context='data preprocessing')

# Print the result
print(response)
