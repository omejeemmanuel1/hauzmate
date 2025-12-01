# HauzMate — Telegram Housing Marketplace Bot

Simple Telegram bot + FastAPI webhook that lets space owners post listings and seekers submit requests. Built with aiogram (Telegram FSM) and FastAPI for webhook handling.

## Features
- Owner and Seeker flows (FSM) to collect listing/request data
- Posts listings to a group chat
- Manual payment info command
- Reply keyboards for better UX

## Requirements
- Python 3.10+
- Packages (example):
  - fastapi
  - uvicorn
  - aiogram
  - python-dotenv
  - aiohttp