import os
import sys
from pathlib import Path
import subprocess
from typing import Union, List, Optional
import tempfile
from config import DATA_DIR


class FileToPDFConverter:
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = DATA_DIR
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def convert(self, input_path: str, output_path: Optional[str] = None) -> str:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        if output_path is None:
            filename = Path(input_path).stem
            output_path = os.path.join(self.output_dir, f"{filename}.pdf")

        file_ext = Path(input_path).suffix.lower()
        try:
            if file_ext == ".csv":
                self.csv_to_pdf(input_path, output_path)
                return output_path
            elif file_ext in [".doc", ".docx"]:
                self.word_to_pdf(input_path, output_path)
                return output_path
            elif file_ext in [".xls", ".xlsx"]:
                self.excel_to_pdf(input_path, output_path)
                return output_path
            elif file_ext in [".ppt", ".pptx"]:
                self.powerpoint_to_pdf(input_path, output_path)
                return output_path
            else:
                return input_path
        except:
            return input_path

    def csv_to_pdf(self, csv_path: str, pdf_path: str):
        try:
            import pandas as pd
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import (
                SimpleDocTemplate,
                Table,
                TableStyle,
                Paragraph,
                Spacer,
            )
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch

            df = pd.read_csv(csv_path)

            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()

            title = Paragraph(f"CSV文件: {Path(csv_path).name}", styles["Title"])
            story.append(title)
            story.append(Spacer(1, 0.25 * inch))

            data = [df.columns.tolist()] + df.values.tolist()

            table = Table(data)

            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(table)
            story.append(Spacer(1, 0.25 * inch))

            # 添加统计信息
            stats = f"""
            数据统计:
            - 总行数: {len(df)}
            - 总列数: {len(df.columns)}
            - 列名: {', '.join(df.columns.tolist())}
            """

            stats_para = Paragraph(stats, styles["Normal"])
            story.append(stats_para)

            # 生成PDF
            doc.build(story)
        except ImportError as e:
            print("请安装所需库: pip install pandas reportlab")
            raise

FileToPDFConverter = FileToPDFConverter()
