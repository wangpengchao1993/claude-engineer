"""
Hugging Face Inference Example / Hugging Face 推理示例
=====================================================

This script shows how to use Hugging Face Transformers for common AI tasks.
All models used here are small enough to run on CPU (no GPU needed!).

本脚本展示如何使用 Hugging Face Transformers 完成常见 AI 任务。
所有模型都足够小，可以在 CPU 上运行（不需要 GPU！）。

Install / 安装:
    pip install transformers torch
"""

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# ============================================================
# 1. Pipeline -- The Easiest Way to Use AI Models
#    Pipeline -- 使用 AI 模型最简单的方式
# ============================================================

def sentiment_analysis_demo():
    """
    Sentiment analysis: Is this text positive or negative?
    情感分析：这段文字是积极的还是消极的？

    Uses distilbert -- a small, fast model perfect for beginners.
    使用 distilbert -- 一个小巧快速的模型，非常适合初学者。
    """
    # Create a sentiment analysis pipeline (downloads model automatically)
    # 创建情感分析管道（自动下载模型）
    classifier = pipeline("sentiment-analysis")

    # Analyze some text / 分析一些文本
    texts = [
        "I absolutely love this product!",
        "This is the worst experience ever.",
        "The weather is okay today.",
    ]

    print("=== Sentiment Analysis / 情感分析 ===")
    for text in texts:
        result = classifier(text)
        label = result[0]["label"]
        score = result[0]["score"]
        print(f"  Text: {text}")
        print(f"  Result / 结果: {label} (confidence / 置信度: {score:.4f})")
        print()


def text_generation_demo():
    """
    Text generation: Give the model a prompt, it writes the rest.
    文本生成：给模型一个开头，它会续写剩下的内容。

    Uses gpt2 -- a classic small model that runs on any computer.
    使用 gpt2 -- 经典的小模型，可以在任何电脑上运行。
    """
    # Create a text generation pipeline with gpt2 (124M parameters -- very small!)
    # 创建文本生成管道，使用 gpt2（1.24 亿参数 -- 非常小！）
    generator = pipeline("text-generation", model="gpt2")

    prompt = "The future of artificial intelligence is"

    print("=== Text Generation / 文本生成 ===")
    print(f"  Prompt / 提示: {prompt}")

    # Generate text with different settings / 用不同设置生成文本
    result = generator(
        prompt,
        max_length=50,        # Maximum total length / 最大总长度
        num_return_sequences=1,  # How many results / 返回几个结果
        temperature=0.7,      # Creativity (0=boring, 1=wild) / 创造性（0=保守, 1=狂野）
        top_p=0.9,            # Nucleus sampling threshold / 核采样阈值
        do_sample=True,       # Enable random sampling / 启用随机采样
    )

    print(f"  Generated / 生成: {result[0]['generated_text']}")
    print()


# ============================================================
# 2. Under the Hood -- Tokenizer + Model
#    深入了解 -- 分词器 + 模型
# ============================================================

def tokenization_demo():
    """
    See how text becomes numbers that the model can understand.
    看看文本是如何变成模型能理解的数字的。

    Tokenization is the first step in ALL language model tasks.
    分词是所有语言模型任务的第一步。
    """
    # Load the GPT-2 tokenizer / 加载 GPT-2 分词器
    tokenizer = AutoTokenizer.from_pretrained("gpt2")

    text = "Hello, world! AI is amazing."

    print("=== Tokenization Process / 分词过程 ===")
    print(f"  Original text / 原始文本: {text}")

    # Step 1: Text -> Token IDs (numbers) / 文本 -> Token ID（数字）
    token_ids = tokenizer.encode(text)
    print(f"  Token IDs / Token 编号: {token_ids}")

    # Step 2: See individual tokens / 查看单独的 token
    tokens = tokenizer.tokenize(text)
    print(f"  Tokens / 分词结果: {tokens}")

    # Step 3: Token IDs -> Back to text / Token ID -> 还原为文本
    decoded_text = tokenizer.decode(token_ids)
    print(f"  Decoded text / 解码文本: {decoded_text}")

    # Show vocabulary size / 显示词汇表大小
    print(f"  Vocabulary size / 词汇表大小: {len(tokenizer)}")
    print()


def manual_generation_demo():
    """
    Load a model manually and generate text step by step.
    手动加载模型并逐步生成文本。

    This gives you more control than pipeline().
    这比 pipeline() 给你更多控制权。
    """
    print("=== Manual Model Loading / 手动加载模型 ===")

    # Load tokenizer and model separately / 分别加载分词器和模型
    model_name = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Prepare input text / 准备输入文本
    prompt = "Python is a great programming language because"
    print(f"  Prompt / 提示: {prompt}")

    # Tokenize the input / 将输入分词
    inputs = tokenizer(prompt, return_tensors="pt")  # "pt" = PyTorch tensors
    print(f"  Input shape / 输入形状: {inputs['input_ids'].shape}")

    # Generate! / 生成！
    outputs = model.generate(
        **inputs,
        max_new_tokens=30,    # Generate up to 30 NEW tokens / 最多生成 30 个新 token
        temperature=0.8,      # A bit creative / 稍有创造性
        top_p=0.9,            # Use nucleus sampling / 使用核采样
        do_sample=True,       # Enable sampling / 启用采样
    )

    # Decode the output back to text / 将输出解码回文本
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"  Generated / 生成: {generated_text}")
    print()


# ============================================================
# Main -- Run All Demos / 运行所有示例
# ============================================================

if __name__ == "__main__":
    print("Hugging Face Transformers -- Beginner Examples")
    print("Hugging Face Transformers -- 初学者示例")
    print("=" * 50)
    print()

    # Each demo downloads its model on first run (cached afterward)
    # 每个示例首次运行时会下载模型（之后会缓存）

    sentiment_analysis_demo()
    text_generation_demo()
    tokenization_demo()
    manual_generation_demo()

    print("Done! All examples completed. / 完成！所有示例已运行。")
