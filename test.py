import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path_350M = "/mnt/e/CodeGenModel/codegen-350M-mono"
model_path = model_path_350M
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

input_text = """import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
sender='abc@163.com'    # 发件人邮箱账号
passtoken = 'PASSWORD'              # 发件人邮箱密码
receiver='123@qq.com'      # 收件人邮箱账号
def mail():
"""
input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
attention_mask = torch.ones_like(input_ids).to(device)

generated_ids = model.generate(
    input_ids=input_ids,
    attention_mask=attention_mask,
    max_length=1024,
    # num_beams=5,
    # num_return_sequences=3,
    # do_sample=True,
    # temperature=0.7,
    # top_k=50,
    # top_p=0.95,
    # repetition_penalty=1.2,
    # length_penalty=2.0,
    # no_repeat_ngram_size=3
)

generated_texts = [tokenizer.decode(g, skip_special_tokens=True) for g in generated_ids]
for idx, text in enumerate(generated_texts):
    print(f"Generated Text {idx + 1}: {text}")
