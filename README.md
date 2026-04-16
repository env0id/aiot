
# Telegram Bot Template

Minimal Telegram bot built with **aiogram** and **SQLAlchemy**.
Provides a clean base with structured startup, router registration, and database initialization.

## Overview

This project sets up a Telegram bot with:

* centralized dispatcher and bot instance
* router-based architecture
* async database engine and session factory
* automatic table creation on startup
* environment-based configuration

## Configuration

Environment variables:

* `BOT_TOKEN` – Telegram bot token
* `ADMIN_ID_LIST` – list of admin user IDs
* `DB_URL` – database connection string