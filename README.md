# 🏢 HRFlow

**Application desktop de gestion des ressources humaines** — Python · PyQt6 · PostgreSQL

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-41CD52?logo=qt&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Fonctionnalités

| Module | Description |
|--------|-------------|
| 👥 **Employés** | CRUD complet, photo, matricule auto-généré, badge PDF avec QR code |
| ⏰ **Présences** | Pointage intelligent (entrée/sortie auto), détection retard, historique filtrable |
| 📅 **Congés** | Demande, approbation/refus par le manager, types multiples |
| 📋 **Tâches** | Attribution, workflow de statuts (assigné → en cours → terminé → livré), notification SMS |
| 📊 **KPI** | Score pondéré automatique : tâches (40%) + présence (30%) + ponctualité (30%) |
| 💰 **Salaires** | Génération bulk/individuelle, prime KPI automatique, fiche de paie PDF |
| 📈 **Dashboard** | Statistiques temps réel, graphiques matplotlib (tâches, présence) |
| ⚙️ **Paramètres** | Thème dark/light, config SMS, pondération KPI, horaires, connexion DB |

### Bonus
- 🌗 **Thème sombre / clair** switchable
- 🚀 **Onboarding wizard** au premier lancement
- 📱 **SMS automatique** via API Onbuka lors d'attribution de tâche
- 🔐 **Système de rôles** (admin, manager) avec authentification bcrypt

---

## 🛠️ Stack technique

- **Langage** : Python 3.10+
- **Interface** : PyQt6
- **Base de données** : PostgreSQL + SQLAlchemy (ORM)
- **PDF** : ReportLab
- **QR Code** : qrcode + Pillow
- **Graphiques** : Matplotlib
- **SMS** : API Onbuka
- **Auth** : bcrypt

---

## 🏗️ Architecture

```
HRFlow/
├── main.py              # Point d'entrée
├── config.py            # Configuration JSON persistante
├── models/              # Modèles SQLAlchemy
│   ├── employee.py
│   ├── attendance.py
│   ├── leave.py
│   ├── task.py
│   ├── salary.py
│   ├── kpi.py
│   └── user.py
├── services/            # Logique métier
│   ├── employee_service.py
│   ├── attendance_service.py
│   ├── leave_service.py
│   ├── task_service.py
│   ├── kpi_service.py
│   ├── salary_service.py
│   ├── sms_service.py
│   └── user_service.py
├── ui/                  # Interface PyQt6
│   ├── main_window.py
│   ├── onboarding.py
│   ├── dashboard_page.py
│   ├── employee_page.py
│   ├── attendance_page.py
│   ├── leave_page.py
│   ├── task_page.py
│   ├── salary_page.py
│   ├── settings_page.py
│   └── themes.py
└── utils/
    └── pdf_utils.py     # Génération badge & fiche de paie
```

---

## 🚀 Installation

### Prérequis
- Python 3.10+
- PostgreSQL installé et en cours d'exécution

### Étapes

```bash
# 1. Cloner le projet
git clone https://github.com/mxcore7/HRFlow.git
cd HRFlow

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer la base de données PostgreSQL
psql -U postgres -c "CREATE DATABASE hrflow;"

# 4. Lancer l'application
python main.py
```

Au premier lancement, le **wizard d'onboarding** vous guidera pour :
1. Configurer la connexion PostgreSQL
2. Renseigner les informations de votre entreprise
3. Choisir votre thème (sombre ou clair)

> **Compte admin par défaut** : `admin` / `admin123`

---

## 📱 Configuration SMS

Pour activer les notifications SMS (tâches attribuées) :

1. Aller dans **Paramètres → SMS**
2. Activer les notifications
3. Renseigner vos identifiants API Onbuka :
   - API Key
   - API Password
   - App ID
4. Tester avec le bouton **"Tester l'envoi SMS"**

---

## 📸 Aperçu

L'application inclut :
- **Sidebar** de navigation avec icônes
- **Tableaux dynamiques** avec recherche et filtres
- **Formulaires modaux** pour ajout/modification
- **Graphiques interactifs** sur le dashboard
- **Export PDF** pour badges et fiches de paie

---

## 📄 License

MIT License — libre d'utilisation et de modification.

---

<p align="center">
  Développé avec ❤️ par <a href="https://github.com/mxcore7">mxcore7</a>
</p>
