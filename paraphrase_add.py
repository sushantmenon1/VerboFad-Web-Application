# importing Flask and other modules
from flask import Flask, request, render_template
from transformers import *
 
# Flask constructor
app = Flask(__name__)  


def get_paraphrased_sentences(model, tokenizer, sentence, num_return_sequences=5, num_beams=5):
  # tokenize the text to be form of a list of token IDs
  inputs = tokenizer([sentence], truncation=True, padding="longest", return_tensors="pt")
  # generate the paraphrased sentences
  outputs = model.generate(
    **inputs,
    num_beams=num_beams,
    num_return_sequences=num_return_sequences,
  )
  # decode the generated sentences using the tokenizer to get them back to text
  return tokenizer.batch_decode(outputs, skip_special_tokens=True)
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def paraphrase():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       para_value_a = request.form.get("paraphrase_val")
       # getting input with name = lname in HTML form
       # value_b = request.form.get("b_val")
       model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
       tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")
       para_var = get_paraphrased_sentences(model, tokenizer, para_value_a, num_beams=10, num_return_sequences=1)
       return render_template("Text Paraphrase.html", paraphrase_result=para_var, paraphrase_val= para_value_a)
    return render_template("Text Paraphrase.html")
 
if __name__=='__main__':
   app.run(debug=True)