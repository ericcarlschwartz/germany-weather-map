# Vercel Deployment Setup Guide

This guide explains how to deploy the Germany Weather Map API to Vercel from scratch, including the persistent Redis cache setup.

## 1. Initial Deployment
1.  **Import Project:** Go to the [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** -> **"Project"**.
2.  **Select Repo:** Import `germany-weather-map`.
3.  **Framework Preset:** Select **"Other"**.
4.  **Root Directory:** `./`
5.  **Deploy:** Click **"Deploy"**. (The first deploy might fail or have 429 errors until the KV database is connected).

## 2. Setup Persistent Cache (Vercel KV)
To prevent API rate limiting, you must connect a Redis database:
1.  Go to your project dashboard on Vercel.
2.  Click the **"Storage"** tab.
3.  Click **"Create Database"** and select **"KV"**.
4.  Follow the prompts to create the database (default settings are fine).
5.  **Connect:** Ensure the KV database is "Connected" to your project. This automatically injects the `KV_URL` environment variable.

## 3. Environment Variables
The application automatically detects the following:
- `KV_URL`: (Injected by Vercel KV). Used for the persistent shared cache.
- `REDIS_URL`: (Optional). An alternative if not using Vercel KV.

## 4. Verifying the Deployment
Once deployed and connected to KV, verify these endpoints:

### HTML Previews (Defaults to Precipitation)
- `https://your-project.vercel.app/`
- `https://your-project.vercel.app/api/preview/temp`
- `https://your-project.vercel.app/api/preview/cloud`

### Binary Data for Hardware
- `https://your-project.vercel.app/api/weather`
- `https://your-project.vercel.app/api/weather/temp`

## 5. Local Development
To test the Vercel environment locally:
1.  Install Vercel CLI: `npm i -g vercel`
2.  Run `vercel dev`.
3.  The API will be available at `http://localhost:3000`.
