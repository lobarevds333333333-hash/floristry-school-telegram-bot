import os
import shutil
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw

def register_cyrillic_font() -> str:
    """
    Registers a TrueType Cyrillic font in ReportLab from standard Windows system fonts.
    """
    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\times.ttf"
    ]
    for font_path in candidates:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont("CyrillicFont", font_path))
                print(f"[Assets] Successfully registered Cyrillic font from: {font_path}")
                return "CyrillicFont"
            except Exception as e:
                print(f"[Assets Warning] Failed to register {font_path}: {e}")
    
    return "Helvetica"

def ensure_assets(assets_dir: Path, force_recreate_pdf: bool = False):
    assets_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = assets_dir / "catalog.pdf"
    img_path = assets_dir / "founder.jpg"

    # Always recreate PDF if requested or if missing
    if force_recreate_pdf or not pdf_path.exists():
        generate_pdf_catalog(pdf_path)

    if not img_path.exists():
        generate_founder_photo(img_path)


def generate_pdf_catalog(output_path: Path):
    font_name = register_cyrillic_font()
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CatalogTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#8B3A62'),
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CatalogSubtitle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceAfter=25
    )

    h2_style = ParagraphStyle(
        'CourseHeading',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#4A7023'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'CourseBody',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#222222'),
        spaceAfter=8
    )

    story = [
        Paragraph("Онлайн-школа флористики «Цветочные Истории»", title_style),
        Paragraph("КАТАЛОГ ОБУЧАЮЩИХ ПРОГРАММ И КУРСОВ", subtitle_style),
        Spacer(1, 10),
        
        Paragraph("1. Флористика для начинающих", h2_style),
        Paragraph("<b>Стоимость:</b> 15 000 руб. | <b>Длительность:</b> 4 недели (16 уроков)", body_style),
        Paragraph("Базовый курс для тех, кто делает первые шаги во флористике. Вы научитесь правильно подготавливать цветы к сборке, освоите спиральную технику, основы колористики и узнаете обо всех тонкостях ухода за растениями.", body_style),
        Spacer(1, 10),

        Paragraph("2. Свадебная флористика", h2_style),
        Paragraph("<b>Стоимость:</b> 28 000 руб. | <b>Длительность:</b> 6 недель (24 урока)", body_style),
        Paragraph("Глубокое погружение в мир свадебных оформлений: создание растрепанных букетов невесты, бутоньерок, декорирование президиума, столов гостей, арки для выездной регистрации и монтажные секреты.", body_style),
        Spacer(1, 10),

        Paragraph("3. Коммерческий букет и декор", h2_style),
        Paragraph("<b>Стоимость:</b> 22 000 руб. | <b>Длительность:</b> 5 недель (20 уроков)", body_style),
        Paragraph("Курс для флористов, желающих увеличить продажи. Техники сборки трендовых и объёмных букетов, современная корейская и авторская упаковка, ценообразование, закупки и маркетинг.", body_style),
        Spacer(1, 20),
        
        Paragraph("<b>Контакты для записи:</b> +7 (999) 000-11-22 | Telegram: @flower_ZEROCODE_bot", subtitle_style)
    ]
    
    doc.build(story)
    print(f"[Assets] Successfully generated Cyrillic PDF catalog at {output_path}")


def generate_founder_photo(output_path: Path):
    # Check if AI generated photo exists in artifact directory
    artifacts_dir = Path(r"C:\Users\Val19\.gemini\antigravity-ide\brain\c6cd2ee4-1d44-43e6-8a85-2c88450d95d0")
    generated_photos = list(artifacts_dir.glob("founder_photo*.png"))
    
    if generated_photos:
        latest_photo = sorted(generated_photos, key=lambda p: p.stat().st_mtime)[-1]
        try:
            img = Image.open(latest_photo)
            img.convert('RGB').save(str(output_path))
            print(f"[Assets] Copied AI founder photo from {latest_photo} to {output_path}")
            return
        except Exception as e:
            print(f"[Assets Warning] Failed copying AI photo: {e}")

    # Fallback graphic generator
    img = Image.new('RGB', (600, 600), color='#FDF0F5')
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 50, 550, 550), fill='#F8D7E3', outline='#E899B9', width=4)
    draw.ellipse((120, 120, 480, 480), fill='#E899B9')
    draw.text((300, 260), "Анна Цветочная", fill='#5A1827', anchor="mm")
    draw.text((300, 310), "Основатель школы", fill='#8B3A62', anchor="mm")
    draw.text((300, 350), "«Цветочные Истории»", fill='#5A1827', anchor="mm")
    img.save(str(output_path))
    print(f"[Assets] Generated fallback founder image at {output_path}")

if __name__ == "__main__":
    assets = Path(__file__).parent.parent / "assets"
    ensure_assets(assets, force_recreate_pdf=True)
