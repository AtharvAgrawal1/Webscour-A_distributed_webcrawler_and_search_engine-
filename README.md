# Webscour-A_distributed_webcrawler_and_search_engine-
🕷️ Distributed Web Crawler
📌 About the Project

This project is a distributed web crawler built using Python and RabbitMQ.

It is designed to crawl web pages, download their HTML content, extract links, and continuously expand the crawl using multiple worker processes running in parallel.

The system demonstrates distributed task processing and horizontal scalability using message queues.

🚀 What This Project Does

Accepts seed URLs

Fetches web pages

Saves HTML files locally

Extracts hyperlinks from pages

Adds new discovered links back to the queue

Supports multiple workers running simultaneously

Distributes URLs across workers automatically

Shows real-time queue activity in RabbitMQ dashboard

✅ Working Features

Distributed crawling using multiple workers

Parallel URL processing

Automatic message distribution

Continuous crawling loop

HTML storage in pages/ directory

Real-time monitoring via RabbitMQ dashboard

Horizontal scalability (run more workers to increase speed)

📂 Output

Downloaded HTML files are stored inside the pages/ folder.

Each worker processes different URLs when multiple workers are running.

Queue activity can be monitored through the local RabbitMQ dashboard.