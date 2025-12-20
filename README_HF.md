---
title: TalimBot
emoji: 🎓
colorFrom: teal
colorTo: cyan
sdk: docker
pinned: false
license: mit
---

# TalimBot - AI-Powered Student Grouping System

An intelligent educational platform that uses advanced psychology principles and AI to create optimal learning groups for adolescent students (ages 15-16).

## Features

- **AI-Powered Grouping**: Automated group formation using OpenAI GPT-4o
- **Educational Psychology**: Based on ZPD theory, MBTI complementarity, VARK learning styles
- **Teacher Dashboard**: Monitor students and manage grouping
- **Student Dashboard**: Complete personality and learning assessments
- **Persian Language**: Full RTL support with Vazirmatn font

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Vanilla JavaScript, Tailwind CSS
- **AI**: OpenRouter API with GPT-4o
- **Deployment**: Hugging Face Spaces (Docker)

## Usage

1. **Teacher Login**: Use password to access teacher dashboard
2. **Student Login**: Enter national code (کد ملی) to access student dashboard
3. **Complete Profiles**: Students fill MBTI, VARK, AMS, and Cooperative assessments
4. **Create Groups**: Teacher runs AI grouping algorithm
5. **View Results**: Students see their assigned groups

## Demo Account

For demonstration purposes, login with:
- National Code: 0921111111
- Name: پریناز عاکف

This account is for demo only and won't be included in grouping.

## Configuration

This Space requires the `OPENROUTER_API_KEY` environment variable to be set in the Secrets section.

Get your free API key at: https://openrouter.ai/keys

## License

MIT License - For educational purposes
