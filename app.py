from flask import Flask, request, jsonify, render_template
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import time

app = Flask(__name__)

model_path_350M = "/mnt/e/CodeGenModel/codegen-350M-mono"

model_path_2B = "/mnt/e/CodeGenModel/models--Salesforce--codegen-2B-mono/snapshots"

model_path = model_path_350M
model_name = "codegen-350M-mono"
#model_name = "codegen-2B-mono"
MAX_LENGTH = 2048

#print(bool(torch.cuda.is_available))
#print(torch.cuda.device_count())

# 指定GPU设备索引
if torch.cuda.is_available():
    device = torch.device("cuda:0")  # 设置设备为GPU如果可用，否则为CPU
    device_name = torch.cuda.get_device_name(0)
else:
    device = torch.device("cpu")
    device_name = torch.device('cpu')

start_load_time = time.time()
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).to(device)  # 将模型移到指定设备上

end_load_time = time.time()
load_duration = end_load_time - start_load_time
#print(f"Model loading time: {load_duration:.2f} seconds")

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)


@app.route('/')
def index():
    # 渲染前端模板
    return render_template('index.html', load_duration=f"{load_duration:.2f}", model_name=model_name, device_name=device_name)


@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.json.get('input_text')

    # Preprocess input text
    if input_text is None or len(input_text.strip()) == 0:
        return jsonify({'error': '输入不能为空'}), 400

    # Ensure input text length is within acceptable range
    if len(input_text) > MAX_LENGTH:
        return jsonify({'error': '输入文本过长'}), 400

    try:
        start_inference_time = time.time()
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
        attention_mask = torch.ones_like(input_ids)
        generated_ids = model.generate(input_ids, attention_mask=attention_mask, num_return_sequences=1, max_length=MAX_LENGTH)
        end_inference_time = time.time()

        generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        inference_duration = end_inference_time - start_inference_time
        

        response = {
            'input_text': input_text,
            'generated_text': generated_text,
            'inference_duration': inference_duration
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)