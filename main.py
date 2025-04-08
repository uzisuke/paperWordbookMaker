import fitz 
import re
import openai
from tqdm import tqdm
import os

# OpenAI APIキー
openai.api_key = "*************************************"

# PDFファイルパス
pdf_path = "data/pdf_name.pdf"
output_path = "output.txt"



# 見出し（章）を検出して章ごとに分割
def extract_chapters_from_pdf(pdf_path):
        #PDFにエラーが無いかを確認する
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
    
    try:
        doc = fitz.open(pdf_path)
        print(f"✅ PDF opened successfully: {pdf_path}")
    except Exception as e:
        raise RuntimeError(f"PDFの読み込みに失敗しました: {e}")
    
    full_text = ""
    for i, page in enumerate(doc):
        try:
            page_text = page.get_text()
            print(f"✅ ページ{i+1}読み込み成功（{len(page_text)}文字）")
            full_text += page_text
        except Exception as e:
            print(f"⚠️ ページ{i+1}の読み込みでエラー: {e}")

    if len(full_text.strip()) == 0:
        raise ValueError("❌ PDFからテキストが抽出できませんでした。画像PDFの可能性があります。")
    
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # 章の抽出（Chapter 1、CHAPTER 1、1.、1.1.、1.1.1.系列に対応）
    heading_pattern = r"(?:^|\n)(Chapter\s\d+|CHAPTER\s\d+|(\d\.+)*\s+[A-Z][^\n]*)(?=\n)"

    matches = list(re.finditer(heading_pattern, full_text, re.MULTILINE))
    chapters = []

    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        title = matches[i].group(1).strip()
        content = full_text[start:end].strip()
        chapters.append({"title": title, "content": content})

    return chapters

# GPTにプロンプトを送り、章ごとの単語帳を作成
def generate_vocab_lists(chapters, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("# Vocabulary List\n\n")

        print("\n📘 Generating vocabulary lists and saving to output.tex...\n")
        for chapter in tqdm(chapters, desc="Processing Chapters", unit="chapter"):
            prompt = f"""
                        Please analyze the following academic text titled "{chapter['title']}" and extract advanced English vocabulary, idiomatic expressions, specialized terms, and difficult-to-understand expressions (above Japanese high school level). Pay attention to the overall meaning of the text, and select words and expressions that are crucial for understanding the content. This includes not only nouns and verbs, but also idiomatic phrases and terms that are important in the context of the text. 

                        For each word or expression, provide a Japanese translation in the following format:

                        - English term (Japanese translation)

                        Only list words and expressions that are essential for understanding the text’s meaning. Avoid everyday, common words. Here’s the text:

                        \"\"\"
                        {chapter['content'][:3000]}
                        \"\"\"
                        """
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an assistant helping Japanese readers understand English academic papers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            vocab = response["choices"][0]["message"]["content"]

            f.write(f"## {chapter['title']}\n")
            f.write(vocab.strip())
            f.write("\n\n---\n\n")


if __name__ == "__main__":
    chapters = extract_chapters_from_pdf(pdf_path)
    generate_vocab_lists(chapters, output_path)
    print(f"\n✅ Vocabulary extraction complete! Output saved to: {output_path}\n")
