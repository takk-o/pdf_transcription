from pathlib import Path
from pypdf import PdfReader

# 出力フォルダの準備
out_fd = Path('text')
out_fd.mkdir(exist_ok=True)

# ./pdfフォルダ内のpdfファイル全てを対象にする
input = Path('pdf')
for file in input.glob('*.pdf'):
    out_fl = out_fd.joinpath(file.stem + '.txt')
    with open(out_fl, mode='w') as f:
        text = ''
        reader = PdfReader(file)
        for i, page in enumerate(reader.pages):
            text += '【page:' + str(i+1) + '】 ---\n'   # ページ数を表示
            text += page.extract_text()                # pdfファイルの文字起こし 
            text += '\n-------------\n'
        f.write(text)
