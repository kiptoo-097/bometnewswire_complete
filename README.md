# 📰 BometNewswire

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Django](https://img.shields.io/badge/Django-4.x-green.svg)
![Status](https://img.shields.io/badge/status-active-success)

**BometNewswire** is a modern digital news platform built with Django for the people of **Bomet County, Kenya**. It features the latest news, events, and community updates with a sleek and responsive design.

---

## 🚀 Features

- 🗞️ Real-time local news publishing
- 📸 Rich media support (images, video, audio)
- 🔍 Advanced search and category filters
- 🌓 Dark mode toggle
- 🧭 Responsive mobile-first design
- 📆 Live event countdowns and status labels (e.g., *Happening*, *Ended*)
- 🔐 Admin dashboard (Django admin)
- 🌐 SEO-friendly URLs and metadata

---

## 🛠️ Tech Stack

| Layer        | Tools Used                  |
|--------------|-----------------------------|
| Backend      | Django 4.x (Python)         |
| Frontend     | HTML5, Tailwind CSS, JavaScript |
| Database     | SQLite (dev) / PostgreSQL (prod) |
| Deployment   | Gunicorn, NGINX on Ubuntu VPS |
| Static Files | WhiteNoise / Django Storage |

---

## ⚙️ Setup Instructions


```bash
https://github.com/kiptoo-097/bometnewswire_complete.git
cd bometnewswire

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
