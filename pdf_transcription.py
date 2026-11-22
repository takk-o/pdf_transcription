"""フォルダ内の PDF からテキストを取り出し、ファイルごとにテキストファイルに保存する。"""

import argparse
from pathlib import Path

ENGINES = ('pdfminer', 'pypdf')


def pages_pypdf(pdf_path: Path) -> list[str]:
    """pypdf でページごとのテキストを取り出す。"""
    from pypdf import PdfReader

    return [page.extract_text() or '' for page in PdfReader(pdf_path).pages]


def pages_pdfminer(pdf_path: Path) -> list[str]:
    """pdfminer.six でページごとのテキストを取り出す（日本語のフォントに比較的強い）。"""
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer

    return [
        ''.join(el.get_text() for el in layout if isinstance(el, LTTextContainer))
        for layout in extract_pages(pdf_path)
    ]


def extract_text(pdf_path: Path, engine: str) -> str:
    """PDF の全ページのテキストを、ページ番号の見出しと区切り線を付けて 1 つの文字列にする。"""
    pages = pages_pdfminer(pdf_path) if engine == 'pdfminer' else pages_pypdf(pdf_path)
    return ''.join(f'【page:{i}】 ---\n{text}\n-------------\n' for i, text in enumerate(pages, start=1))


def main() -> None:
    parser = argparse.ArgumentParser(description='PDF からテキストを取り出す')
    parser.add_argument('--input', default='pdf', type=Path, help='PDF を置くフォルダ（既定は pdf）')
    parser.add_argument('--output', default='text', type=Path, help='テキストの出力先（既定は text）')
    parser.add_argument('--engine', default='pdfminer', choices=ENGINES,
                        help='取り出しに使う方法（既定は pdfminer）')
    args = parser.parse_args()

    pdf_files = sorted(args.input.glob('*.pdf'))
    if not pdf_files:
        print(f'{args.input}/ に PDF がありません')
        return

    args.output.mkdir(exist_ok=True)
    for pdf_path in pdf_files:
        try:
            text = extract_text(pdf_path, args.engine)
        except Exception as e:  # 壊れた PDF やパスワード付きの PDF は飛ばして続ける
            print(f'スキップ：{pdf_path.name}（{e}）')
            continue
        output_path = args.output / f'{pdf_path.stem}.txt'
        output_path.write_text(text, encoding='utf-8')
        print(f'{pdf_path.name} → {output_path}')


if __name__ == '__main__':
    main()
