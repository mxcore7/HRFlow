import io
import qrcode
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image


def generate_qr_code(data, size=150):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def generate_badge_pdf(employee, output_path):
    c = canvas.Canvas(output_path, pagesize=(9*cm, 5.5*cm))

    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(0, 0, 9*cm, 5.5*cm, fill=1, stroke=0)

    c.setFillColor(HexColor("#0f3460"))
    c.rect(0, 4.2*cm, 9*cm, 1.3*cm, fill=1, stroke=0)

    c.setFillColor(HexColor("#e94560"))
    c.rect(0, 4.1*cm, 9*cm, 0.15*cm, fill=1, stroke=0)

    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(4.5*cm, 4.5*cm, "BADGE EMPLOYÉ")

    if employee.photo:
        try:
            photo_buffer = io.BytesIO(employee.photo)
            photo_img = Image.open(photo_buffer)
            photo_img = photo_img.resize((80, 80))
            photo_buf = io.BytesIO()
            photo_img.save(photo_buf, format="PNG")
            photo_buf.seek(0)
            c.drawImage(ImageReader(photo_buf), 0.5*cm, 1.5*cm, 2*cm, 2*cm)
        except Exception:
            pass

    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(3*cm, 3.5*cm, f"{employee.prenom} {employee.nom}")
    c.setFont("Helvetica", 7)
    c.setFillColor(HexColor("#a0a0a0"))
    c.drawString(3*cm, 3.0*cm, f"Matricule: {employee.matricule}")
    c.drawString(3*cm, 2.5*cm, f"Poste: {employee.poste or 'N/A'}")
    c.drawString(3*cm, 2.0*cm, f"Dept: {employee.departement or 'N/A'}")

    qr_data = f"HRFLOW|{employee.matricule}|{employee.nom}|{employee.prenom}"
    qr_buffer = generate_qr_code(qr_data, size=100)
    c.drawImage(ImageReader(qr_buffer), 6.5*cm, 0.3*cm, 2*cm, 2*cm)

    c.setFillColor(HexColor("#666666"))
    c.setFont("Helvetica", 5)
    c.drawCentredString(4.5*cm, 0.2*cm, "HRFlow - Système de Gestion RH")

    c.save()
    return output_path


def generate_payslip_pdf(employee, salary, kpi, output_path, company_config=None):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    company = company_config or {}

    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(0, height - 3*cm, width, 3*cm, fill=1, stroke=0)

    c.setFillColor(HexColor("#e94560"))
    c.rect(0, height - 3.1*cm, width, 0.15*cm, fill=1, stroke=0)

    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 1.5*cm, "FICHE DE PAIE")
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, height - 2.2*cm, company.get("name", "Mon Entreprise"))

    mois_noms = {1:"Janvier",2:"Février",3:"Mars",4:"Avril",5:"Mai",6:"Juin",
                 7:"Juillet",8:"Août",9:"Septembre",10:"Octobre",11:"Novembre",12:"Décembre"}

    y = height - 4.5*cm
    c.setFillColor(HexColor("#333333"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y, "Informations Employé")
    y -= 0.7*cm

    info = [
        ("Nom complet", f"{employee.prenom} {employee.nom}"),
        ("Matricule", employee.matricule),
        ("Poste", employee.poste or "N/A"),
        ("Période", f"{mois_noms.get(salary.mois, salary.mois)} {salary.annee}"),
    ]
    c.setFont("Helvetica", 9)
    for label, value in info:
        c.setFillColor(HexColor("#666666"))
        c.drawString(2*cm, y, f"{label}:")
        c.setFillColor(HexColor("#333333"))
        c.drawString(7*cm, y, str(value))
        y -= 0.5*cm

    y -= 0.5*cm
    c.setFillColor(HexColor("#0f3460"))
    c.rect(1.5*cm, y - 0.1*cm, width - 3*cm, 0.6*cm, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(2*cm, y + 0.05*cm, "DESCRIPTION")
    c.drawRightString(width - 2*cm, y + 0.05*cm, "MONTANT (FCFA)")
    y -= 0.8*cm

    lines = [
        ("Salaire de base", salary.salaire_base),
        ("Prime KPI", salary.prime_kpi),
        ("Bonus", salary.bonus),
        ("Déductions", -salary.deductions),
    ]
    c.setFont("Helvetica", 9)
    for label, amount in lines:
        c.setFillColor(HexColor("#333333"))
        c.drawString(2*cm, y, label)
        color = "#e94560" if amount < 0 else "#333333"
        c.setFillColor(HexColor(color))
        c.drawRightString(width - 2*cm, y, f"{amount:,.0f}")
        y -= 0.6*cm

    y -= 0.3*cm
    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(1.5*cm, y - 0.1*cm, width - 3*cm, 0.7*cm, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y + 0.05*cm, "SALAIRE NET")
    c.drawRightString(width - 2*cm, y + 0.05*cm, f"{salary.salaire_net:,.0f} FCFA")

    y -= 1.5*cm
    c.setFillColor(HexColor("#333333"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y, "Performance KPI")
    y -= 0.7*cm

    if kpi:
        kpi_lines = [
            ("Score Tâches", f"{kpi.score_taches:.1f}/100"),
            ("Score Présence", f"{kpi.score_presence:.1f}/100"),
            ("Score Ponctualité", f"{kpi.score_ponctualite:.1f}/100"),
            ("Score Global", f"{kpi.score_global:.1f}/100"),
        ]
        c.setFont("Helvetica", 9)
        for label, value in kpi_lines:
            c.setFillColor(HexColor("#666666"))
            c.drawString(2*cm, y, f"{label}:")
            c.setFillColor(HexColor("#333333"))
            c.drawString(7*cm, y, value)
            y -= 0.5*cm

    c.setFillColor(HexColor("#999999"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(width/2, 1*cm, "Document généré par HRFlow - Système de Gestion des Ressources Humaines")

    c.save()
    return output_path
