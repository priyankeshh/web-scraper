# 🌐 Web Scraper

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Chrome](https://img.shields.io/badge/Chrome-132+-green.svg)](https://www.google.com/chrome/)

An advanced web scraping solution that combines the power of AI with automated data extraction. Built with a modern tech stack and featuring an intuitive Streamlit interface, this tool transforms complex web data into structured, analysis-ready formats.

## 🌟 Key Features

- 🤖 **AI-Powered Data Extraction** - Utilizes multiple LLM models for intelligent data parsing
- 🎯 **Custom Field Selection** - Define exactly what data you want to extract
- 📊 **Multi-Format Export** - Export to JSON, Excel, and Markdown
- ⚡ **Real-Time Processing** - Watch the scraping process in action
- 🎨 **Modern UI/UX** - Clean, responsive interface built with Streamlit
- 🔄 **Progress Tracking** - Live updates on scraping status

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Google Chrome 132+
- pip (Python package manager)

### Quick Install

1. Clone the repository:
```bash
git clone https://github.com/yourusername/intelligent-web-scraper.git
cd intelligent-web-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Launch the application:
```bash
streamlit run streamlit_app.py
```

## 📸 Usage Example

### 1. Select Target Website
![Target Website Selection](https://github.com/user-attachments/assets/8a94ce17-6ffc-4da1-9ce2-c43cbab3968c)

### 2. Configure Scraping Parameters
![Scraper Configuration](https://github.com/user-attachments/assets/748fa4a1-cb2e-486f-944a-798f0c534dfd)

### 3. View Results
![Scraping Results](https://github.com/user-attachments/assets/511460f8-31d6-4b0b-a9a1-30ab418080f9)

### 4. Access Exported Data
![Exported Data](https://github.com/user-attachments/assets/638d466b-ac71-4298-be5a-6f116944f2b9)

Example output format:
```json
{
  "listings": [
    {
      "train_number": "12345",
      "train_name": "Express",
      "departure": "10:00 AM",
      "arrival": "06:30 PM",
      "duration": "8h 30m"
    }
  ]
}
```

## 🛠️ Technology Stack

- **Web Automation**: Selenium WebDriver
- **AI Models**: OpenAI GPT-4, Google Gemini, Llama
- **Frontend**: Streamlit
- **Data Processing**: Pandas, BeautifulSoup4
- **Export Formats**: JSON, Excel, Markdown
- **Browser Driver**: ChromeDriver

## 📁 Project Structure

```
intelligent-web-scraper/
├── streamlit_app.py     # Main application interface
├── scraper.py          # Core scraping engine
├── assets.py          # Utility functions and constants
├── requirements.txt   # Project dependencies
├── output/           # Exported data directory
└── chromedriver/    # Chrome WebDriver files
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

If you encounter any issues or have questions:
- Open an issue in the GitHub repository
- Contact the maintainer at your.email@example.com

## 🙏 Acknowledgments

- Selenium Documentation Team
- Streamlit Community
- ChromeDriver Development Team
- All our contributors and users


Made by Priyankesh